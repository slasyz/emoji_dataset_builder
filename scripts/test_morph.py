import os

import nltk

nltk.data.path.append(os.path.join(os.path.dirname(__file__), '..', 'resources'))

words = [
    ':', 'a', 'is', 'on', 'in', 'hello', 'apple', 'running', 'grinning'
]

poses = nltk.pos_tag(words, tagset='universal')
print(poses)
