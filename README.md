# audiobooks

Some introduction:
I used programs in the past like Readarr and LazyLibrarian, to try and keep my library up to date with the audiobooks I like. These programs turned out to be notoriously unreliable (Readarr) or have a very steep learning curve (LL). So I decided to take matters in my own hands, and just create an Excel file with the books I would like to read (with a tab per author). After that,I wrote a script that organizes my downloaded books into a folder with a structure recognized by AudioBookShelf. What was important of course was that the directory structure in the download folder remained the same. So no monitoring, disappearing books, or things like that.
In short, this script:
- Loops through all directories in my downloadFolder.
- Checks one audiofile in every subdirectory, to see if it is already linked in my audiobookFolder.
- Continue with only the audiobooks that need processing, and ask user for input on those books.
- Hard link every file for those books to my audiobookFolder, in the correct directory structure.

The directory structure is the one documentedhere. So /Author/Series/1. Book Title/001.mp3
All the subdirectories that are used in the downloadFolder, are flattened in audiobookFolder (Part 1, Part 2, or things like that). Filenames are changed to 001, 002, and so on. Only audiofiles are linked. I have no need to link anything else (jpg, cue, etc), because AudioBookShelf takes care of that. I never cared for chapters, so I haven't done anything in the script to account for those.

Disclaimer: I am in no way a(Python) expert, I wrote this just for fun and it works for me. I'm not responsible for anything that happens to your files, or if your house catches fire or if you cat decides to leave you. I am however always open for suggestions to improve this script.
If it works for you: hurray! If not, bummer. Just leave a message here, maybe I can help.
