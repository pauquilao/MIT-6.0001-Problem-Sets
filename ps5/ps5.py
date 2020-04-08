# 6.0001/6.00 Problem Set 5 - RSS Feed Filter
# Name: Paulo Quilao
# Collaborators: none
# Time: long

import feedparser
import string
import time
import threading
from project_util import translate_html
from mtTkinter import *
from datetime import datetime
import pytz
import pprint

#-----------------------------------------------------------------------

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        description = translate_html(entry.description)
        pubdate = translate_html(entry.published)

        try:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")
            pubdate.replace(tzinfo=pytz.timezone("GMT"))
          #  pubdate = pubdate.astimezone(pytz.timezone('EST'))
          #  pubdate.replace(tzinfo=None)
        except ValueError:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")

        newsStory = NewsStory(guid, title, description, link, pubdate)
        ret.append(newsStory)
    return ret


#======================
# Data structure design
#======================

# Problem 1
# TODO: NewsStory

class NewsStory(object):
    def __init__(self, guid, title, description, link, pubdate):
        self.guid = guid
        self.title = title
        self.description = description
        self.link = link
        self.pubdate = pubdate

    #  getters
    def get_guid(self):
        return self.guid

    def get_title(self):
        return self.title

    def get_description(self):
        return self.description

    def get_link(self):
        return self.link

    def get_pubdate(self):
        return self.pubdate

    #  setters
    def set_guid(self, guid):
        self.guid = guid

    def set_title(self, title):
        self.title = title

    def set_description(self, description):
        self.description = description

    def set_link(self, link):
        self.link = link

    def set_pubdate(self, pubdate):
        self.pubdate = self


#======================
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        # DO NOT CHANGE THIS!
        raise NotImplementedError


# PHRASE TRIGGERS

# Problem 2
# TODO: PhraseTrigger

class PhraseTrigger(Trigger):
    def __init__(self, phrase_trigger):
        self.phrase = phrase_trigger

    def get_phrase(self):
        return self.phrase

    def is_phrase_in(self, text):
        #  import regular expression
        #  to strip passed arg of any punctuation marks
        import re

        punctuation = string.punctuation
        regex = re.compile(r"[{}]".format(re.escape(punctuation)))
        #  replace each punctuation with a white space
        #  to return valid triggers concatenated in one string
        #  using puntuations (e.g. purple#^&$#^$cow)
        text_strip = regex.sub(" ", text)

        #  standardize passed arguments to lowercase letters
        #  and store each word in a list
        phrase = self.get_phrase()
        text_list = [str(word).lower() for word in text_strip.split()]
        phrase_list = [str(word).lower() for word in phrase.split()]
        index_list = []

        #  check if each word in the passed phrase trigger
        #  is in passed text
        for word in phrase_list:
            if word not in text_list:
                return False
            else:
                #  iterate each word and iterator of each item in the passed argument
                for index, text in enumerate(text_list):
                    if word == text:
                        #  get the index of the matched word in text
                        index_list.append(index)
        #  get the difference between succeeding and preceeding indices
        index_value = [index_list[i + 1] - index_list[i]
                       for i in range(len(index_list) - 1)]

        #  test for consecutiveness
        #  consecutive words in the passed text should have difference
        #  in indices by one (1) since they occur in the list back-to-back
        for value in index_value:
            if value != 1:
                return False

        return True


# Problem 3
# TODO: TitleTrigger

class TitleTrigger(PhraseTrigger):
    def evaluate(self, story):
        # get the title in the NewsStory
        return self.is_phrase_in(story.get_title())


# Problem 4
# TODO: DescriptionTrigger

class DescriptionTrigger(PhraseTrigger):
    def evaluate(self, story):
        # get the description in the NewsStory
        return self.is_phrase_in(story.get_description())


# TIME TRIGGERS

# Problem 5
# TODO: TimeTrigger
# Constructor:
#        Input: Time has to be in EST and in the format of "%d %b %Y %H:%M:%S".
#        Convert time from string to a datetime before saving it as an attribute.

class TimeTrigger(Trigger):
    def __init__(self, pubtime):
        pubtime = datetime.strptime(pubtime, "%d %b %Y %H:%M:%S")
        pubtime = pubtime.replace(tzinfo=pytz.timezone("EST"))
        self.pubtime = pubtime


# Problem 6
# TODO: BeforeTrigger and AfterTrigger

class BeforeTrigger(TimeTrigger):
    def evaluate(self, story):
        #  triggers if story is published before the set time
        #  cast pubdate to offset-aware datetime to compare times correctly
        return self.pubtime > story.get_pubdate().replace(tzinfo=pytz.timezone("EST"))


class AfterTrigger(TimeTrigger):
    def evaluate(self, story):
        #  triggers if story is published after the set time
        #  cast pubdate to offset-aware datetime to compare times correctly
        return self.pubtime < story.get_pubdate().replace(tzinfo=pytz.timezone("EST"))


# COMPOSITE TRIGGERS

# Problem 7
# TODO: NotTrigger

class NotTrigger(Trigger):
    def __init__(self, trigger):
        self.trigger = trigger

    def evaluate(self, story):
        """inverts the ouput of passed trigger"""
        not_fire = not self.trigger.evaluate(story)
        return not_fire


# Problem 8
# TODO: AndTrigger

class AndTrigger(Trigger):
    def __init__(self, trig1, trig2):
        self.trig1 = trig1
        self.trig2 = trig2

    def evaluate(self, story):
        """return True if both triggers fired"""
        fire = self.trig1.evaluate(
            story) == True and self.trig2.evaluate(story) == True
        return fire


# Problem 9
# TODO: OrTrigger

class OrTrigger(Trigger):
    def __init__(self, trig1, trig2):
        self.trig1 = trig1
        self.trig2 = trig2

    def evaluate(self, story):
        """return True if one of the triggers fired"""
        fire = self.trig1.evaluate(
            story) == True or self.trig2.evaluate(story) == True
        return fire


# ======================
# Filtering
# ======================
# Problem 10

def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """
    # TODO: Problem 10
    # This is a placeholder
    # (we're just returning all the stories, with no filtering)

    story_list = []
    for story in stories:
        for trigger in triggerlist:
            if trigger.evaluate(story):
                story_list.append(story)
                break

    return story_list


#======================
# User-Specified Triggers
#======================
# Problem 11

def read_trigger_config(filename):
    """
    filename: the name of a trigger configuration file

    Returns: a list of trigger objects specified by the trigger configuration
        file.
    """
    # We give you the code to read in the file and eliminate blank lines and
    # comments. You don't need to know how it works for now!

    trigger_file = open(filename, 'r')
    lines = []
    for line in trigger_file:
        line = line.rstrip()
        if not (len(line) == 0 or line.startswith('//')):
            lines.append(line)

    # TODO: Problem 11
    # line is the list of lines that you need to parse and for which you need
    # to build triggers

    #  split items in lines
    trigs_split = [tuple(item.split(",")) for item in lines]
    trig_keys = ["TITLE", "DESCRIPTION",
                 "AFTER", "BEFORE", "AND", "OR", "NOT", "ADD"]

    #  map configuration to trigger names
    triggers_dict = {}
    for tup in trigs_split:
        for key in trig_keys:
            if key == tup[1]:
                triggers_dict.setdefault(tup[0], [])
                for i in range(len(tup) - 1):
                    triggers_dict[tup[0]].append(tup[i + 1])
            elif key == tup[0]:
                triggers_dict.setdefault(tup[0], [])
                for i in range(len(tup) - 1):
                    triggers_dict[tup[0]].append(tup[i + 1])

    triggers_list = []
    trigs_obj = {}
    #  create trigger objects based on configuration
    for key, val in triggers_dict.items():

        if "TITLE" in val:
            obj = TitleTrigger(val[1])
            trigs_obj.setdefault(key, obj)

        elif "DESCRIPTION" in val:
            obj = DescriptionTrigger(val[1])
            trigs_obj.setdefault(key, obj)

        elif "Before" in val:
            obj = BeforeTrigger(val[1])
            trigs_obj.setdefault(key, obj)

        elif "AFTER" in val:
            obj = AfterTrigger(val[1])
            trigs_obj.setdefault(key, obj)

        elif "AND" in val:
            obj = AndTrigger(val[1], val[2])
            trigs_obj.setdefault(key, obj)

        elif "OR" in val:
            obj = OrTrigger(val[1], val[2])
            trigs_obj.setdefault(key, obj)

        elif key == "NOT":
            obj = NotTrigger(val[1])
            trigs_obj.setdefault(key, obj)

        #  add specified triggers to the list
        elif key == "ADD":
            for item in val:
                for obj_key, obj in trigs_obj.items():
                    if item == obj_key:
                        triggers_list.append(obj)

    return triggers_list


#  for debugging
# triggerlist = read_trigger_config('triggers.txt')
# pprint.pprint(triggerlist)


SLEEPTIME = 120  # seconds -- how often we poll


def main_thread(master):
    # A sample trigger list - you might need to change the phrases to correspond
    # to what is currently in the news
    try:
        t1 = TitleTrigger("COVID-19")
        t2 = DescriptionTrigger("President Duterte")
        t3 = DescriptionTrigger("Luzon Quarantne")
        t4 = AndTrigger(t2, t3)
        triggerlist = [t1, t4]

        # Problem 11
        # TODO: After implementing read_trigger_config, uncomment this line
        triggerlist = read_trigger_config('triggers.txt')

        # HELPER CODE - you don't need to understand this!
        # Draws the popup window that displays the filtered stories
        # Retrieves and filters the stories from the RSS feeds
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT, fill=Y)

        t = "Google & Yahoo Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica", 14),
                    yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)
        guidShown = []

        def get_cont(newstory):
            if newstory.get_guid() not in guidShown:
                cont.insert(END, newstory.get_title() + "\n", "title")
                cont.insert(
                    END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.get_description())
                cont.insert(
                    END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.get_guid())

        while True:

            print("Polling . . .", end=' ')
            # Get stories from Google's Top Stories RSS news feed
            stories = process("http://news.google.com/news?output=rss")

            # Get stories from Yahoo's Top Stories RSS news feed
            stories.extend(process("http://news.yahoo.com/rss/topstories"))

            stories = filter_stories(stories, triggerlist)

            list(map(get_cont, stories))
            scrollbar.config(command=cont.yview)

            print("Sleeping...")
            time.sleep(SLEEPTIME)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    root = Tk()
    root.title("Some RSS parser")
    t = threading.Thread(target=main_thread, args=(root,))
    t.start()
    root.mainloop()
