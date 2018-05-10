# wotd
A simple command-line word-of-the-day script.

This script manages word-of-the-day words in a sqlite database and reports them out to stdout on demand.

The basic functions are:
- print the word of the day
- print a random word from the database
- add a new word (taking input from a file)
- edit an existing word (essentially taking input from a file and overwriting the corresponding word in the database)

Words added to the database are tagged with the contributor's username, and future edits are only allowed by that user (or by the owner of the script).

TODO:
1. Finish the inline TODOs
2. Bulk load of new words.  Currently words are loaded one by one through text files for each word.
3. Users tag their favorite words and create their own subsets, composed of words from anyone.
4. IRC bot, featuring wotd, wotd r, wotd like [word], and word dislike [word] -- then, allow popularity charts and elimination of bad words
5. Allow anyone to make changes to any word, improving the definition, example, etc. And keep a revision history of changes.
