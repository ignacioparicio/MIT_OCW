class NewsStory(object):
    def __init__(self, guid, title, description, link, pubdate):
        self.guid = guid
        self.title = title
        self.description = description
        self.link= link
        self.pubdate = pubdate
    
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
    def __init__(self, phrase):
        self.phrase = phrase.lower()
        
    def in_phrase_in(self, text):
        text = self.prepare_text(text)
        if self.phrase in text:
            # Extra checks to ensure same phrase ending in text (avoid plurals)
            if (self.phrase[-1] == text[-1]) or self.phrase + ' ' in text:
                return True
            else:
                return False
        else:
            return False
    
    def prepare_text(self, text):
        ''' Return text in lowercase, removing all punctuation signs and
         with single spaces replacing multiple spaces
         '''
        text = text.lower()
        # Use regular expressions to remove all punctuation signs
        text = re.sub(r'[^\w]', ' ', text)
        # Transform into list and back into string to eliminate extra spaces
        text = text.split()
        text = ' '.join(text)
        return text

# Problem 3
# TODO: TitleTrigger

class TitleTrigger(PhraseTrigger):
    def evaluate(self, story):
        return self.in_phrase_in(story.get_title())

# Problem 4
class DescriptionTrigger(PhraseTrigger):
    def evaluate(self, story):
        return self.in_phrase_in(story.get_description())
        
        

# ------------------------------------------------------------------------------

cuddly    = NewsStory('', 'The purple cow is soft and cuddly.', '', '', datetime.now())
exclaim   = NewsStory('', 'Purple!!! Cow!!!', '', '', datetime.now())
symbols   = NewsStory('', 'purple@#$%cow', '', '', datetime.now())
spaces    = NewsStory('', 'Did you see a purple     cow?', '', '', datetime.now())
caps      = NewsStory('', 'The farmer owns a really PURPLE cow.', '', '', datetime.now())
exact     = NewsStory('', 'purple cow', '', '', datetime.now())

plural    = NewsStory('', 'Purple cows are cool!', '', '', datetime.now())
separate  = NewsStory('', 'The purple blob over there is a cow.', '', '', datetime.now())
brown     = NewsStory('', 'How now brown cow.', '' ,'', datetime.now())
badorder  = NewsStory('', 'Cow!!! Purple!!!', '', '', datetime.now())
nospaces  = NewsStory('', 'purplecowpurplecowpurplecow', '', '', datetime.now())
nothing   = NewsStory('', 'I like poison dart frogs.', '', '', datetime.now())

list_stories = [cuddly, exclaim, symbols, spaces, caps, exact,
                plural, separate, brown, badorder, nospaces, nothing]

s1 = TitleTrigger('PURPLE COW')
s2  = TitleTrigger('purple cow')

a = TitleTrigger(s2)
for story in list_stories:
    print('Evaluation of', story.get_title(), a.evaluate(story))
