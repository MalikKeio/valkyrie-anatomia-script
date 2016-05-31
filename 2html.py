#!/usr/bin/env python3

import os
import re

from names import CHAPTERS, CHARACTERS
CLASSES = {
    "f": "file",
    "u": "utterance",
    "u-jp": "utterance-jp",
    "u-en": "utterance-en",
    "s": "speaker",
    "c": "content",
    "l": "line",
    "w": "window"
}

class Content:
    def __init__(self):
        self.lines = []
    def add_line(self, line):
        self.lines.append(line)
    def getHTML(self):
        html = '<div class="%s">' % CLASSES['c']
        for line in self.lines:
            html += '<div class="%s">%s</div>' % (CLASSES['l'], line)
        html += '</div>'
        return html
class UtterancePerLanguage:
    def __init__(self, speaker, content, language):
        # speaker is a str!
        self.speaker = speaker
        self.content = content
        self.language = language
    def getHTML(self):
        html = '<div class="%s-%s"><div class="%s">%s</div>%s</div>' %                (CLASSES['u'], self.language, CLASSES['s'], self.speaker,
                    self.content.getHTML())
        return html
class Utterance:
    def __init__(self, children=None):
        if children is None:
            children = []
        self.children = children
    def add_child(self, child):
        if isinstance(child, UtterancePerLanguage):
            self.children.append(child)
        else:
            raise TypeError("Child's instance is not supported: %s" % child)
    def getHTML(self):
        html = '<div class="%s">' % CLASSES['u']
        for child in self.children:
            html += child.getHTML()
        html += '</div>'
        return html

class WindowPerLanguage:
    def __init__(self, content, language):
        self.content = content
        self.language = language
    def getHTML(self):
        html = '<div class="%s-%s">%s</div>' % (CLASSES['w'], self.language, self.content.getHTML())
        return html
class Window:
    def __init__(self, children=None):
        if children is None:
            children = []
        self.children = children
    def add_child(self, child):
        if isinstance(child, WindowPerLanguage):
            self.children.append(child)
        else:
            raise TypeError("Child's instance is not supported: %s" % child)
    def getHTML(self):
        html = '<div class="%s">' % CLASSES['w']
        for child in self.children:
            html += child.getHTML()
        html += '</div>'
        return html
class File:
    def __init__(self):
        self.children = []
    def add_child(self, child):
        if isinstance(child, Utterance) or isinstance(child, Window):
            self.children.append(child)
        else:
            raise TypeError("Child's instance is not supported: %s" % child)
    def getHTML(self):
        html = '<div class="%s">' % CLASSES['f']
        for child in self.children:
            html += child.getHTML()
        html += '</div>'
        return html

def getHTMLForOneQuest(filejp, fileen):
    print("[INFO] Opening '%s' and '%s'..." % (filejp, fileen))
    f = File()
    content_jp = None
    content_en = None
    previous_line_empty = True
    for linejp, lineen in zip(open(filejp), open(fileen)):
        # remove new line character
        linejp = linejp[:-1]
        lineen = lineen[:-1]
        if len(linejp) == 0:
            previous_line_empty = True
            continue
        if linejp[0] == "\t" and len(linejp) > 1 and linejp[1] != "\t":
            # This is a line of speech
            if content_jp is None or content_en is None:
                print("[WARN] I guess there is a syntax error in the vp file around:\n    %s" % linejp)
            else:
                # Remove the first tab
                content_jp.add_line(linejp[1:])
                content_en.add_line(lineen[1:])
        elif linejp[0] == "\t" and len(linejp) > 1 and linejp[1] == "\t":
            if previous_line_empty:
                content_jp = Content()
                content_en = Content()
                content_jp.add_line(linejp[2:])
                content_en.add_line(lineen[2:])
                window_jp = WindowPerLanguage(content_jp, 'jp')
                window_en = WindowPerLanguage(content_en, 'en')
                window = Window([window_jp, window_en])
                f.add_child(window)
            else:
                content_jp.add_line(linejp[2:])
                content_en.add_line(lineen[2:])
        else:
            # This is a speaker
            if linejp in CHARACTERS:
                # This is a speaker
                content_jp = Content()
                content_en = Content()
                utterance_jp = UtterancePerLanguage(linejp, content_jp, 'jp')
                utterance_en = UtterancePerLanguage(lineen, content_en, 'en')
                utterance = Utterance([utterance_jp, utterance_en])
                f.add_child(utterance)
            else:
                # This is an unknown character. That would be a bug.
                print("[WARN] Unknown character: %s" % linejp)
        previous_line_empty = False
    return f.getHTML()

HTML_HOME = "html"
for chapter in CHAPTERS:
    index = int(chapter.split('.')[0])
    en_chapter = "en/%s" % CHAPTERS[chapter]
    for root, dirs, files in os.walk('jp/%s' % chapter):
        for name in files:
            filejp_path = os.path.join(root, name)
            fileen_path = en_chapter + "/" + name
            html = getHTMLForOneQuest(filejp_path, fileen_path)
            out_folder_path = "%s/%d" % (HTML_HOME, index)
            if not os.path.exists(out_folder_path):
                os.makedirs(out_folder_path)
            target = "%s/%s.html" % (out_folder_path, name)
            with open(target, "w") as out:
                out.write(html)