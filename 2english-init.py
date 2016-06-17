#!/usr/bin/env python3

import os

from names import CHAPTERS, CHARACTERS

en_chapter = "en/"
if not os.path.exists(en_chapter):
    os.makedirs(en_chapter)
for root, dirs, files in os.walk('jp/'):
    for name in files:
        path = os.path.join(root, name)
        target_path = path.replace('jp/', 'en/')
        if os.path.exists(target_path):
            print("[WARN] %s exists!" % target_path)
        else:
            with open(path) as f:
                if not os.path.exists(target_path):
                    os.makedirs("/".join(target_path.split('/')[0:-1]))
                target = open(target_path, "w")
                for line in f:
                    speaker = line[:-1]
                    if speaker in CHARACTERS:
                        target.write("%s\n" % CHARACTERS[speaker])
                    else:
                        target.write(line)
