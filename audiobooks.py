#!/home/vincent/.venv/bin/python

#import sys
import os
from termcolor import colored

downloadFolder = "/media/hdd/data/torrents/audiobooks/personal"
audiobookFolder = "/media/hdd/data/media/audiobooks"
allowedFiles = ['mp3','m4b']

linkedInodes = []
chooseList = []
knownAuthors = []
bookCounter = 0

for author in next(os.walk(audiobookFolder))[1]: # Get list of known authors. These are all directories in audiobookFolder
    knownAuthors.append(author)

# Get inode numbers for all files in audiobook folder. Needed to check later on if files have already been hard linked
for root, subFolder, files in os.walk(audiobookFolder):
    for item in files:
        inode = os.stat(os.path.join(root,item)).st_ino
        linkedInodes.append(inode)

for rootDir in next(os.walk(downloadFolder))[1]: # Loop through all directories on level 0
    alreadyLinked = False
    toProcess = []
    for bookDir, subDirs, files in os.walk(os.path.join(downloadFolder,rootDir)): # os.walk through every directory
        if any(y in x for x in files for y in allowedFiles): # only continue if (sub)directory contains files in allowedFiles list
            filteredFiles = [f for f in files if f[-3:] in allowedFiles] # Make new list of files with only files in allowedFiles list
            if os.stat(os.path.join(bookDir, filteredFiles[0])).st_ino not in linkedInodes: # Only continue if files are not already linked in audiobookFolder. Checked against earlied made linkedInodes
                toProcess.append([bookDir,filteredFiles]) # Append current (sub)directory to list of directories to be processed, with file list attached
            else:
                alreadyLinked = True
    # If the book does not already exist in audiobookFolder, continue processing book
    if not alreadyLinked:
        os.system('clear')
        print(rootDir)
        print("-----------------")
        print("Known authors:") 
        # Show list of authors already in audiobookFolder, from list knownAuthors
        for knownAuthorIndex, knownAuthor in enumerate(knownAuthors):
            print(str(knownAuthorIndex+1) +': '+knownAuthor)
        chosenAuthor = input("Author: ")
        if chosenAuthor.isnumeric():
            chosenAuthor = knownAuthors[int(chosenAuthor)-1]
            print(colored("Chosen author (Press Enter to skip this book): "+chosenAuthor,'green',attrs=['bold']))
        if not chosenAuthor: # If not author is entered, skip this book entirely
            continue
        errorCounter = 0
        chosenTitle = ''
        while chosenTitle == '':
            if errorCounter > 0:
                print ('\033[1A' + '\033[K' + '\033[1A') # Clear input line on first error 
                if errorCounter > 1:
                    print ('\033[1A' + '\033[K' + '\033[1A')
                print(colored("Please enter a title!", 'red',attrs=['bold'])) # Clear input line as well as error line on subsequent errors
            errorCounter += 1
            chosenTitle = input("Title: ")
        print("-----------------")
        # Show list of already known series by author.
        # This contains a list of all directories in author directory, so the list also shows book(s) not belonging to a series
        knownSeries = next(os.walk(os.path.join(audiobookFolder,chosenAuthor)))[1] 
        if(len(knownSeries) != 0):
            print("Known series for author (attention: these can also be book not belonging to a series):")
            for knownSerieIndex, knownSerie in enumerate(knownSeries):
                print(str(knownSerieIndex+1) +': '+knownSerie)
        chosenSeries = input("Series (enter for none): ")
        if chosenSeries.isnumeric():
            chosenSeries = knownSeries[int(chosenSeries)-1]
            print(colored("Chosen series: "+chosenSeries,'green',attrs=['bold'])) 
        
        seriesPart = ''
        if chosenSeries: 
            print("-----------------")
            errorCounter = 0
            while seriesPart == '':
                if errorCounter > 0:
                    print ('\033[1A' + '\033[K' + '\033[1A') # Clear input line on first error
                    if errorCounter > 1:
                        print ('\033[1A' + '\033[K' + '\033[1A') # Clear input line as well as error line on subsequent errors
                    print(colored("Please enter a series part!", 'red',attrs=['bold']))
                errorCounter += 1
                seriesPart = input("Series part: ")
        # Add formatting for seriesPart
        if seriesPart:
            seriesPart = str(seriesPart) + ". "
        newDir = os.path.join(audiobookFolder,chosenAuthor,chosenSeries,seriesPart+chosenTitle)
        # Process all the (sub)directories for current book
        for currentProcessDir in toProcess:
            subDir = currentProcessDir[0].replace(downloadFolder,'').replace(rootDir,'').replace('/','') # Extract last part of directory to get subdirectory. This is used 1:1 in audiobookFolder
            newDir = os.path.join(audiobookFolder,chosenAuthor,chosenSeries,seriesPart+chosenTitle)
            if subDir != '':
                newDir = os.path.join(newDir,subDir) # Add subdir, if files were in subdir in downloadFolder
            try:
                os.makedirs(newDir)
            except FileExistsError:
                print("Deze directory bestaat al") # This should not happen, but just to make sure we're not overwriting anything
                exit()
            trackCounter = 1
            for newFile in sorted(currentProcessDir[1]): # Process all files in current (sub)dir
                fileExtension = os.path.splitext(newFile)[1]
                os.link(os.path.join(currentProcessDir[0],newFile), os.path.join(newDir,str("{:03d}".format(trackCounter))+fileExtension))
                trackCounter += 1
        bookCounter += 1
        print("-----------------")
        toContinue = input("Continue to next book (Enter)")
if bookCounter == 0:
    print("No books found for processing, exiting program")
else:
    print("No more books, exiting program")
exit()
