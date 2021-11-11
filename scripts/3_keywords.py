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
    'tone', 'skin', 'a'
]


def __main__():
    keywords: dict[str, int] = {}

    df_src_filename = os.path.join(os.path.dirname(__file__), '..', 'resources', 'emoji_df_words.csv')
    df_src = pd.read_csv(df_src_filename)

    df_dest = pd.DataFrame(columns=['emoji', 'keywords'])
    df_dest_filename = os.path.join(os.path.dirname(__file__), '..', 'resources', 'emoji_df_keywords.csv')

    for i, row in df_src.iterrows():
        emoji = row['emoji']
        words = set(json.loads(row['words']))
        poses = json.loads(row['poses'])

        for word in words:
            if word in IGNORE_WORDS:
                # print('ignoring word "{}"'.format(word_normal))
                continue
            pos = poses[word]
            if pos not in ALLOWED_POSES:
                # print('ignoring "{}" -> {}'.format(word_normal, pos))
                continue
            keywords[word] = keywords.get(word, 0) + 1
            # print('setting "{}" -> {}'.format(word_normal, pos))

    # word_to_count = keywords.items()
    # count_to_word = [(count, word) for word, count in word_to_count]
    # count_to_word.sort(reverse=True)
    # for count, word in count_to_word:
    #     print('{} -> {}'.format(word, count))

    for i, row in df_src.iterrows():
        emoji = row['emoji']
        words = set(json.loads(row['words']))
        poses = json.loads(row['poses'])

        res = ''
        keywords_counted = {}
        for word in words:
            pos = poses[word]
            if pos not in ALLOWED_POSES:
                # print('ignoring "{}" -> {}'.format(word, pos))
                continue

            res += '{}({}) '.format(word, keywords.get(word, '-'))
            count = keywords.get(word)
            if count is None:
                continue

            keywords_counted[word] = count
        print('{} -> {}'.format(emoji, res))

        df_dest = df_dest.append({
            'emoji': emoji,
            'keywords': json.dumps(keywords_counted, ensure_ascii=False),
        }, ignore_index=True)

    df_dest.to_csv(df_dest_filename)


if __name__ == '__main__':
    __main__()
