# portuguese_flash_card_generator
A small tool to create audio files for portuguese flashcards.  Easily import these files into Anki notcards.

Insert a .csv with the following columns

* Portuguese
* English
* Audio
* Tags (no spaces allowed, write "common_phrases" not "common phrases")


If you are unsure of either the English or Portuguese translation for a particular, just write "x" in that column and the tool
will translate for you.


The tool will automatically translate the phrases, record the correct pronunciation and save an .mp3 file for each phrase in the output folder.  It will also create a single .csv file to import into Anki.

Once complete:
Bulk import the new audio files into Anki's library.
Bulk import the newly created .csv file to Anki, and Anki will generate a new notecard deck complete with audio files.


TODO:  add additional language support... tons of other things.
