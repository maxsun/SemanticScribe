# Notes Parser
Python code for parsing Markdown notes into Roam-Research like data.

All notes have 2 main components: a title and text blocks.
For example, we might have the file `todays_note.md` containing the markdown:
```
- Washington DC is the capital of [[the United States]].
- George Washington was the first president of [[the United States]].
  - He became president in 1798
```
The note's title is specified by its filename, in this case "todays note". Text blocks are specified by newlines beginning with "-".

Text blocks contain either plain text or references to other notes or text blocks.
References are written `[[note title]]` or `[[text block id]]`.

If a reference is made to a nonexistent note, then the note is created dynamically.
In the above example, the note `the United States` is created and linked to the notes which reference it automatically.
