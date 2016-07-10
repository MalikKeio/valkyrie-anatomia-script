#!/usr/bin/env python3

import os
import re

from names import CHAPTERS, CHARACTERS, JP, EN, SIDE_STORY_CHAPTERS, SIDE_STORY_CHAPTERS_LEN, OTHER_STORIES, EINHERJAR, STORIES, STATUS, TRANSLATED, INPROGRESS, NOSTORY
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
        # Remove comments //
        line = line.split('//')[0]
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
    def __init__(self, path, title, body, subtitle="", subsubtitle=""):
        self.title = title
        self.subtitle = subtitle
        self.subsubtitle = subsubtitle
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
    <h2>%s</h2>
    <h3>%s</h3>
    %s
    <script>
    (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
    (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
    m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
    })(window,document,'script','https://www.google-analytics.com/analytics.js','ga');

    ga('create', 'UA-79560349-1', 'auto');
    ga('send', 'pageview');

    </script>
</body>
</html>''' % (self.path, self.title, self.title, self.subtitle, self.subsubtitle, self.body)
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

def create_subchapters(folder, chapter_content_div, csspath, title, subtitle=""):
    found = False
    for root, dirs, files in os.walk(folder):
        for name in files:
            found = True
            filejp_path = os.path.join(root, name)
            fileen_path = filejp_path.replace("jp/", "en/")
            html_body = getHTMLForOneQuest(filejp_path, fileen_path)
            out_folder_path = folder.replace("jp/", "%s/" % HTML_HOME)
            if not os.path.exists(out_folder_path):
                os.makedirs(out_folder_path)
            target = "%s/%s.html" % (out_folder_path, name)
            subchapter_name = name.split(',')[0][0:-3]
            chapter_content_div.create_child(["subchapter"], '<a href="%s">%s</a>' % (target.replace("%s/" % HTML_HOME, ""), subchapter_name))
            with open(target, "w") as out:
                if len(files) > 1:
                    out.write(HTMLFile(csspath, title, html_body, subtitle=subtitle, subsubtitle="Part %s" % subchapter_name).getHTML())
                else:
                    out.write(HTMLFile(csspath, title, html_body, subtitle=subtitle).getHTML())
    chapter_content_div.sort()
    if found:
        global chapter_count
        chapter_count += 1

def add_progress_to_chapter(chapter_div_class, chapter_div, chapter, title):
    if chapter[STATUS] is TRANSLATED:
        chapter_div_class.append('translated')
        translation_completion['count'] += 1
    elif chapter[STATUS] is INPROGRESS:
        chapter_div_class.append('in-progress')
        translation_completion['count'] += 0.5
    elif chapter[STATUS] is NOSTORY:
        chapter_div_class.append('no-story')
        # Do not count chapters with no story in translation progression
        translation_completion['max'] -= 1
    translation_completion['max'] += 1
    chapter_div.create_child(chapter_div_class, title)


def add_simple_chapters(chapters, story_div, namespace):
    for chapter_index in chapters:
        en_chapter = "en/%s/%d" % (namespace, chapter_index)
        chapter_div = story_div.create_child(['chapter'])
        title = "%d. %s &mdash; %s" % (chapter_index, chapters[chapter_index][JP], chapters[chapter_index][EN])
        add_progress_to_chapter(['chapter-title'], chapter_div, chapters[chapter_index], title)
        chapter_content_div = chapter_div.create_child(['chapter-content'])
        create_subchapters('jp/%s/%d' % (namespace, chapter_index), chapter_content_div, '../../', title)


HTML_HOME = "html"
index_html_body = Div(['file'])
progression_div = index_html_body.create_child(["progression"])
chapter_count = 0
translation_completion = {'max': 0, 'count': 0}
main_story_div = index_html_body.create_child(["main-story"])
add_simple_chapters(CHAPTERS, main_story_div, 'main')
side_story_div = index_html_body.create_child(["side-story"])
for chapters in SIDE_STORY_CHAPTERS:
    einherjar = chapters[EINHERJAR]
    en_chapter = "en/side/%s" % einherjar
    chapter_div = side_story_div.create_child(['chapter'])
    try:
        title = "%s &mdash; %s" % (einherjar, CHARACTERS[einherjar])
    except KeyError:
        print("[WARN] Unknown Einherjar: %s" % einherjar)
        title = "%s &mdash; %s" % (einherjar, "")
    chapter_div.create_child(['chapter-title'], title)
    chapter_content_div = chapter_div.create_child(['chapter-content'])
    story_index = 1
    for story in chapters[STORIES]:
        story_title = "%s &mdash; %s" % (story[JP], story[EN])
        add_progress_to_chapter(['chapter-subtitle'], chapter_content_div, story, story_title)
        chapter_content_subdiv = chapter_content_div.create_child()
        create_subchapters('jp/side/%s/%d' % (einherjar,story_index), chapter_content_subdiv, '../../../', title, subtitle=story_title)
        story_index += 1
other_stories_div = index_html_body.create_child(["other-stories"])
add_simple_chapters(OTHER_STORIES, other_stories_div, 'other')
CHAPTER_TOTAL_COUNT = len(CHAPTERS) + SIDE_STORY_CHAPTERS_LEN + len(OTHER_STORIES)
progression_div.innerHTML = "Transcript Progression: %.2f%%<br>Translation Progression: %.2f%%" % (100*(chapter_count/CHAPTER_TOTAL_COUNT), 100*(translation_completion['count']/translation_completion['max']))
print("Transcript Progression: %d/%d" % (chapter_count, CHAPTER_TOTAL_COUNT))
print("Translation Progression: %.1f/%d" % (translation_completion['count'], translation_completion['max']))
with open("%s/index.html" % HTML_HOME, 'w') as out:
    out.write(HTMLFile('', 'Valkyrie Anatomia &ndash;The Origin&ndash;<br>Script', index_html_body.getHTML()).getHTML())
