#!/usr/bin/env python3

import os
import re

from names import CHAPTERS, CHARACTERS, JP, EN, SIDE_STORY_CHAPTERS, OTHER_STORIES, EINHERJAR, STORIES
CLASSES = {
    "f": "file",
    "u": "utterance",
    "u-jp": "utterance-jp",
    "u-en": "utterance-en",
    "s": "speaker",
    "c": "content",
    "l": "line",
    "w": "window",
    "t": "transition",
    "b": "battle"
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
class Transition:
    def getHTML(self):
        return '<div class="%s"><div class="%s-jp"><hr></div><div class="%s-en"><hr></div></div>' % (3*(CLASSES['t'],))
class Battle:
    def getHTML(self):
        return '<div class="%s"><div class="%s-jp"><hr>戦闘<hr></div><div class="%s-en"><hr>Battle<hr></div></div>' % (3*(CLASSES['b'],))
class File:
    def __init__(self):
        self.children = []
    def add_child(self, child):
        if isinstance(child, Utterance) or isinstance(child, Window) or isinstance(child, Transition) or isinstance(child, Battle):
            self.children.append(child)
        else:
            raise TypeError("Child's instance is not supported: %s" % child)
    def getHTML(self):
        html = '<div class="%s">' % CLASSES['f']
        for child in self.children:
            html += child.getHTML()
        html += '</div>'
        return html
class Div:
    def __init__(self, classes=None, innerHTML=""):
        if classes is None:
            classes = []
        self.innerHTML = innerHTML
        self.classes = classes
        self.children = []
    def getHTML(self):
        innerHTML = self.innerHTML
        for child in self.children:
            innerHTML += child.getHTML()
        if len(self.classes) == 0:
            return "<div>%s</div>" % innerHTML
        else:
            classString = ' '.join(self.classes)
            return '<div class="%s">%s</div>' % (classString, innerHTML)
    def add_child(self, child):
        self.children.append(child)
    def create_child(self, classes=None, innerHTML=""):
        div = Div(classes, innerHTML)
        self.add_child(div)
        return div
    def sort(self):
        self.children.sort(key=lambda child: child.getHTML())
class HTMLFile:
    def __init__(self, path, title, body):
        self.title = title
        self.body = body
        self.path = path
    def getHTML(self):
        html = '''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <link rel="stylesheet" href="%sstyle.css">
    <title>%s</title>
</head>
<body>
    <h1>%s</h1>
    %s
</body>
</html>''' % (self.path, self.title, self.title, self.body)
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
        if linejp == "---":
            # This is a transition
            f.add_child(Transition())
        elif linejp == "!!!":
            # This is a battle
            f.add_child(Battle())
        elif linejp[0] == "\t" and len(linejp) > 1 and linejp[1] != "\t":
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

def create_subchapters(folder, chapter_content_div, csspath, title):
    for root, dirs, files in os.walk(folder):
        for name in files:
            filejp_path = os.path.join(root, name)
            fileen_path = filejp_path.replace("jp/", "en/")
            html_body = getHTMLForOneQuest(filejp_path, fileen_path)
            out_folder_path = folder.replace("jp/", "%s/" % HTML_HOME)
            if not os.path.exists(out_folder_path):
                os.makedirs(out_folder_path)
            target = "%s/%s.html" % (out_folder_path, name)
            chapter_content_div.create_child(["subchapter"], '<a href="%s">%s</a>' % (target.replace("%s/" % HTML_HOME, ""), name.split(',')[0]))
            with open(target, "w") as out:
                out.write(HTMLFile(csspath, title, html_body).getHTML())

HTML_HOME = "html"
index_html_body = Div(['file'])
main_story_div = index_html_body.create_child(["main-story"])
for chapter_index in CHAPTERS:
    en_chapter = "en/main/%d" % chapter_index
    chapter_div = main_story_div.create_child(['chapter'])
    title = "%d. %s &mdash; %s" % (chapter_index, CHAPTERS[chapter_index][JP], CHAPTERS[chapter_index][EN])
    chapter_div.create_child(['chapter-title'], title)
    chapter_content_div = chapter_div.create_child(['chapter-content'])
    create_subchapters('jp/main/%d' % chapter_index, chapter_content_div, '../../', title)
    chapter_content_div.sort()
side_story_div = index_html_body.create_child(["side-story"])
for chapters in SIDE_STORY_CHAPTERS:
    einherjar = chapters[EINHERJAR]
    en_chapter = "en/side/%s" % einherjar
    chapter_div = side_story_div.create_child(['chapter'])
    try:
        title = "%s &mdash; %s" % (einherjar, CHARACTERS[einherjar])
    except KeyError:
        print("[WARN] Unkown Einherjar: %s" % einherjar)
        title = "%s &mdash; %s" % (einherjar, "")
    chapter_div.create_child(['chapter-title'], title)
    chapter_content_div = chapter_div.create_child(['chapter-content'])
    story_index = 1
    for stories in chapters[STORIES]:
        story_title = "%s &mdash; %s" % (stories[JP], stories[EN])
        chapter_content_div.create_child(['chapter-subtitle'], story_title)
        create_subchapters('jp/side/%s/%d' % (einherjar,story_index), chapter_content_div, '../../../', title)
        story_index += 1
with open("%s/index.html" % HTML_HOME, 'w') as out:
    out.write(HTMLFile('', 'Valkyrie Anatomia &ndash;The Origin&ndash;<br>Script', index_html_body.getHTML()).getHTML())
