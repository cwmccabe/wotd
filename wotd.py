#!/usr/bin/python3
# -*- coding: utf-8 -*-

## UTF-8 is important; otherwise you cannot even have UTF-8 characters
## in comments like here: "mu·ta·tis mu·tan·dis"

import sys, getpass, sqlite3

## SOME WOTD'S AS FODDER:
## https://www.nytimes.com/column/learning-word-of-the-day
## https://www.merriam-webster.com/word-of-the-day/calendar
## https://en.oxforddictionaries.com/explore/weird-and-wonderful-words

## sqlite3 python guide/examples:
## https://docs.python.org/2/library/sqlite3.html

#CREATE TABLE wotd (
# word_lc text NOT NULL,
# word text NOT NULL,
# type text NOT NULL,
# pronunciation text NOT NULL,
# defintion text NOT NULL,
# example text DEFAULT NULL,
# interesting_fact text DEFAULT NULL,
# contributor_name text NOT NULL,
# wotd_date DATETIME,
# timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
#);

exe_name = "wotd.py"; ## IN CASE IT NEEDS TO BE REF'ED BELOW
wotd_db = "/home/cmccabe/bots.etc/wotd/wotd.db"

## CONNECT TO THE DB OR DIE TRYING
try:
  conn = sqlite3.connect(wotd_db);
  c = conn.cursor();
except Error as e:
  print(e);
  sys.exit();

def gentle_quit(str=""):
  if (str):
    print(str);
  conn.close();
  sys.exit();

def argerr():
  print("Invalid input arguments.  For proper usage, type '"+ exe_name +" --h'");
  gentle_quit();

def print_help():
  print("""usage: wotd [OPTION] [FILENAME]
  [OPTION] can be:
  (empty/blank)- just print today's wotd
  r            - print a random word from the wotd word bank.
  a [FILENAME] - add a new word from file.
  pf [FILENAME]- print a word from the db to a file, in the same format as an input file.
  --h / --help - get the help you're reading now.""");
  gentle_quit();

def print_word_file_format():
  print("""Input file for adding or editing a word must be exactly six lines in this order:
  1. word (the word itself, spelled correctly and in common casing)
  2. type (verb, adjective,  etc.)
  3. pronunciation (something like PRO-NUN-SEE-AY-SHUN)
  4. definition (the word's definition)
  5. example (an example of the word's usage)
  6. interesting fact (something interesting about the word; its etymology, etc.)""")

def print_random_word():
## PRINT RANDOM WORD
  sqlstr = "SELECT word, type, pronunciation, definition FROM wotd ORDER BY RANDOM() LIMIT 1;"
  c.execute(sqlstr);
  row = c.fetchone();

  print("Random Word from the WOTD database:");
  print(row[0] + " (" + row[1] + "), [" + row[2] + "], def: " + row[3]);

  gentle_quit();

def print_wotd():
## PRINT TODAY'S WORD (THE WOTD)
  sqlstr = "SELECT COUNT(*) FROM wotd WHERE wotd_date=DATE('now');"
  c.execute(sqlstr);
  row = c.fetchone();

  if row[0] == 0:
    ## GET/PRINT A WORD THAT HASN'T BEEN WOTD OR ONE THAT WAS USED LONGEST AGO
    sqlstr = "SELECT rowid, word, type, pronunciation, definition FROM wotd ORDER BY wotd_date LIMIT 1;"
    c.execute(sqlstr);
    row = c.fetchone();
    rowid = row[0];
    print("Today's Word-of-the-Day is:");
    print(row[1] + " (" + row[2] + "), [" + row[3] + "], def: " + row[4]);
    ## UPDATE THAT WORD'S RECORD WITH TODAY'S DATE AS wotd_date
    sqlstr = "UPDATE wotd SET wotd_date=date('now') WHERE rowid=" + str(rowid);
    c.execute(sqlstr);
    conn.commit();
    gentle_quit();

  else: ## PRINT TODAY'S WOTD
    sqlstr = "SELECT word, type, pronunciation, definition FROM wotd WHERE wotd_date=DATE('now');";
    c.execute(sqlstr);
    row = c.fetchone();
    print("Today's Word of the Day is:");
    print(row[0] + " (" + row[1] + "), [" + row[2] + "], def: " + row[3]);
    gentle_quit();

def print_word_to_file(word):
  ## TODO: VALIDATE/SANITIZE word
  sqlstr = "SELECT word, type, example, pronunciation, definition, interesting_fact FROM wotd WHERE word = LOWER(\""+ word +"\");"
  c.execute(sqlstr);
  row = c.fetchone();

  if row is None:
    gentle_quit("Sorry, "+ word +" does not exist in the database.");

  ## CONFIRM THAT USER IS OK WITH OVERWRITING EXISTING FILE, IF IT EXISTS.
  yn = input("If "+ word +".txt exists, this will overwrite it.  Do you want to proceed? (y/n):")
  if yn.lower() != 'y':
    gentle_quit("File write aborted.");

  try:
    filename = word +".txt";
    filehandle = open(filename, "w");
  except:
    print("Error openning the filename (\""+ filename +"\"). You might not have write permissions for the destination directory.");

  filehandle.write("\n".join(row));
  filehandle.close();
  print(filename + " saved.");

  gentle_quit();

def add_new_word(filename):
  try:
    filehandle = open(filename, "r");
  except:
    print("Error: the filename/path you entered (\""+ filename +"\") does not exist or you do not have read permissions for that file.");

  new_word = filehandle.read();
  new_word = new_word.splitlines();

  ## CHECK THAT THE WORD FILE HAS EXACTLY SIX LINES:
  word_file_len = len(new_word);
  if word_file_len != 6:
    print("Error. Incorrect format of new word file.");
    print_word_file_format();
    gentle_quit();

  ## FIRST, CHECK WHETHER THE WORD ALREADY EXISTS IN THE DB:
  word_lc = new_word[0].lower();
  sqlstr = "SELECT COUNT(*) FROM wotd WHERE word_lc=\"" + word_lc + "\"";
  c.execute(sqlstr);
  row = c.fetchone();

  if row[0] >= 1:
    print("Error: " + new_word[0] + " already exists in the wotd database.");
    gentle_quit();

  username = getpass.getuser();

  sqlstr = "INSERT INTO wotd(word_lc, word, type, pronunciation, definition, example, interesting_fact, contributor_name) VALUES(?,?,?,?,?,?,?,?)";

  ## VALIDATE AND SANITIZE INPUT:

  ## NEW WORD:
  if (len(new_word[0])>45):
    gentle_quit("Input error: New word too long.");

#  if (FN(new_word[0])):
#    gentle_quit("Input error: Invalid character(s) used in new word.");

  ## TYPE:
  if new_word[1].lower() not in ["adjective", "conjunction", "determiner", "exclamation", "noun", "preposition", "pronoun", "verb"]:
    gentle_quit("Input error: New word not of accepted type (adjective, conjunction, determiner, exclamation, noun, preposition, pronoun, verb)");

  ## PRONUNCIATION:
  ## TODO: VALIDATE pronunciation
#  print "pronunciation: " + new_word[2];

  ## DEFINITION:
  ## TODO: VALIDATE definition
#  print "definition: " + new_word[3];

  ## EXAMPLE:
  ## TODO: VALIDATE example
#  print "example: " + new_word[4];

  ## INTERESTING FACT:
  ## TODO: VALIDATE interesting_fact
#  print "interesting_fact: " + new_word[5];

  new_word = [word_lc] + new_word + [username];
  c.execute(sqlstr, new_word);
  conn.commit();
  print("Thank you. Your wotd entry for " + new_word[1] + " has been added.");
  filehandle.close();
  gentle_quit();

def edit_word(filename):
  try:
    filehandle = open(filename, "r");
  except:
    print("Error: the filename/path you entered (\""+ filename +"\") does not exist or you do not have read permissions for that file.");

  word_file = filehandle.read();
  word_file = word_file.splitlines();

  ## CHECK THAT THE UPDATE WORD FILE HAS EXACTLY SIX LINES:
  word_file_len = len(word_file);
  if word_file_len != 6:
    print("Error. Incorrect format of new word file.");
    print_word_file_format();
    gentle_quit();

## == MAIN PROGRAM FLOW ==
## PARSE INPUT LINE AND EXIT IF BAD INPUT IS RECIEVED:
if len(sys.argv) == 1:
  print_wotd();
elif len(sys.argv) == 2 and sys.argv[1] == "r":
    print_random_word();
elif len(sys.argv) == 2 and (sys.argv[1] == "--h" or sys.argv[1] == "--help"):
    print_help();
elif len(sys.argv) == 3 and sys.argv[1] == "pf":
  print_word_to_file(sys.argv[2]);
elif len(sys.argv) == 3 and sys.argv[1] == "e":
    edit_word();
elif len(sys.argv) == 3 and sys.argv[1] == "a":
    add_new_word(sys.argv[2]);
else:
  argerr();

## THE END. THAT'S ALL FOLKS.
conn.close()
