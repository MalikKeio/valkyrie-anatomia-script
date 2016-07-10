Script taken with help from Youtube Channel:
https://www.youtube.com/channel/UCHd-COkuR2lB_NbaST6I4xw

# Contributing

Contribution are most welcome.
To contribute, you can among other things:
- transcribe the Japanese script from the game
- translate the game in English (or any language you want)
- edit the translation, spell-checking, etc
- play the Valkyrie Anatomia game ;)

The Japanese script is to be put inside the `jp` folder.
The English script is to be put inside the `en` folder.

If you want to start a new language, just add the translated script with the
same directory tree as for the Japanese script.

## Directory tree

Each language has its own root directory (e.g. `en` for English), and you will
find inside three folders: `main`, `side` and `other`, for (guess what?) the
main story, the side story and other stories.

Each main story chapter is numbered and inside it you will find `.vp` files (one
for each sub-chapter in the game). Open it with any text editor.
The syntax of the `.vp` files will be explained in the next section.

Chapter names (and their numbering) and proper names (those that appear above
the speech box) are inside `names.py`.

## Syntax

`.vp` file syntax is very simple. There is only five rules. If reading the rules
bother you, just see any `.vp` file and follow the same convention. Here are the
rules:
- A line that starts with no tabulation is the name of speaker who speaks the
next lines until another speaker speeks.
- A line that starts with 1 tabulation is a line of speech.
- A line that starts with 2 tabulations is a text box taking all the screen
for which the speaker is not explicitly indicated. When going to the next
screen, there is a line break between such two "screen-sized" text box.
- `---` means some kind of scene transition.
- `!!!` means that a battle happens.

Moreover, you can add comments at the end of lines with `//`.

FYI, I use atom as a text editor and I created an atom plugin to highlight
syntax according to the above rule. This plugin even implements some handy
keyboard shortcuts. See: https://github.com/valkyrieanatomia/language-vp

# HTML output

The repo includes a Python program (`2html.py`) to automatically publish the
translation in clean HTML format.

You can by the way see the latest translation online here: https://valkyrieanatomia.github.io/.

# Some comments for programmers

To initialize an English script, run the following script (this will take care
of a bunch of time-consuming task so that you only have to focus on
translating):

    ./2english-init.py

Generate HTML view with:

    ./2html.py
