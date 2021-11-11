import json
import os

import pandas as pd
import nltk
from nltk.stem import WordNetLemmatizer


# Run manually:
#  import nltk
#  nltk.download('punkt', 'resources')
#  nltk.download('wordnet', 'resources')
#  nltk.download('averaged_perceptron_tagger', 'resources')
#  nltk.download('universal_tagset', 'resources')
nltk.data.path.append(os.path.join(os.path.dirname(__file__), '..', 'resources'))

wnl = WordNetLemmatizer()


ALLOWED_POSES = [
    'ADJ',   # green
    'ADV',   # up, when
    'DET',   # a, every
    'NOUN',  # home
    'NUM',   # twenty, 1337
    'PRON',  # he
    'VERB',  # say
]

IGNORE_WORDS = [
    'tone', 'skin', ''
]


def normalize_word(word):
    res = wnl.lemmatize(word)
    if res is None:
        return None
    return res.lower()


def __main__():
    df_src_filename = os.path.join(os.path.dirname(__file__), '..', 'resources', 'emoji_df_clean_eng.csv')
    df_src = pd.read_csv(df_src_filename)

    df_dest = pd.DataFrame(columns=['emoji', 'meanings', 'words', 'poses'])
    df_dest_filename = os.path.join(os.path.dirname(__file__), '..', 'resources', 'emoji_df_words.csv')

    for i, row in df_src.iterrows():
        emoji = row['emoji']
        meanings = json.loads(row['src_meanings'])

        words = set()
        poses_res = {}

        for meaning in meanings:
            tokens = list(nltk.tokenize.word_tokenize(meaning))
            tokens_normal = [normalize_word(x) for x in tokens]

            poses = dict(nltk.pos_tag(tokens, tagset='universal'))
            poses = {normalize_word(x): y for x, y in poses.items()}
            print('{} -> {} -> {}'.format(emoji, tokens_normal, poses))
            words |= set(tokens_normal)
            poses_res |= poses

        print('{} -> {}'.format(emoji, words))
        df_dest = df_dest.append({
            'emoji': emoji,
            'meanings': json.dumps(meanings, ensure_ascii=False),
            'words': json.dumps(list(words), ensure_ascii=False),
            'poses': json.dumps(poses_res, ensure_ascii=False),
        }, ignore_index=True)

    df_dest.to_csv(df_dest_filename)


if __name__ == '__main__':
    __main__()
