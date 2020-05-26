import os

# file.truncate(0) will clear everything in a file. This is how I cleared all code in the extractor files, since I did copy it as I just wanted the names.

valid = 'https://www.%s.com'

class AllExtractors:
    def __init__(self):
        self.extractors = os.listdir('extractor') # Will list everything in this folder
        '''
        print(os.getcwd()) # This will get the current directory of where this file is located.
        '''
        self.extractors.remove('__init__.py')
        # already have these extractors coded manually
        self.extractors.remove('youtube.py')
        self.extractors.remove('yahoo.py')
        self.extractors.remove('steam.py')
        self.extractors.remove('twitter.py')
        self.extractors.remove('twitch.py')

        '''
        List Comprehension!
        '''
        self.extractors = [element.replace('.py', '') for element in self.extractors]  # replace .py with nothing
        self.extractors = [element.replace(element, valid %element) for element in self.extractors]
        self.manual_add_known_extractors()

    def manual_add_known_extractors(self):
        self.extractors.append('https://www.youtube.com/watch?v=')
        self.extractors.append('https://uk.news.yahoo.com')
        self.extractors.append('https://store.steampowered.com')
        self.extractors.append('https://www.pornhubpremium.com')
        self.extractors.append('https://twitter.com')
        self.extractors.append('https://twitch.tv')

    @property
    def pack_extractors(self):
        return self.extractors