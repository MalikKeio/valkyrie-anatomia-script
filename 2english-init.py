#!/usr/bin/env python3

import os

from names import CHAPTERS, CHARACTERS

for chapter in CHAPTERS:
    en_chapter = "en/%s" % CHAPTERS[chapter]
    if not os.path.exists(en_chapter):
        os.makedirs(en_chapter)
    for root, dirs, files in os.walk('jp/%s' % chapter):
        for name in files:
            path = os.path.join(root, name)
            target_path = en_chapter + "/" + name
            if os.path.exists(target_path):
                print("[WARN] %s exists!" % target_path)
            else:
                with open(path) as f:
                    target = open(en_chapter + "/" + name, "w")
                    for line in f:
                        speaker = line[:-1]
                        if speaker in CHARACTERS:
                            target.write("%s\n" % CHARACTERS[speaker])
                        else:
                            target.write(line)
