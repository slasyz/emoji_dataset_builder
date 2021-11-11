import json
import os
from typing import Iterable

import pandas as pd
from pymorphy2 import MorphAnalyzer
from ruwordnet import RuWordNet  # ruwordnet download


wn = RuWordNet()
morph = MorphAnalyzer()


def get_hypernyms(synset_ids: Iterable[str]) -> set[str]:
    res = set()
    for synset_id in synset_ids:
        synset = wn[synset_id]
        for hp in synset.hypernyms:
            res.add(hp.id)

    return res


def get_hyponyms(synset_ids: Iterable[str]) -> set[str]:
    res = set()
    for synset_id in synset_ids:
        synset = wn[synset_id]
        for hp in synset.hyponyms:
            res.add(hp.id)

    return res


def get_synset_name(synset_id):
    return wn[synset_id].title


def get_word_synsets(word) -> set[str]:
    synsets = set()

    senses = wn.get_senses(word)
    if senses is not None:
        synsets |= {x.synset_id for x in senses[:max(3, len(senses))]}

    # res |= get_hypernyms(synsets)
    # res |= get_hyponyms(synsets)

    return synsets


def normalize_word_ru(word: str) -> set[str]:
    res = morph.parse(word)
    if res is None or len(res) == 0:
        return set(word)

    return {x.normal_form for x in res[:max(2, len(res))]}


def __main__():
    df_src_filename = os.path.join(os.path.dirname(__file__), '..', 'resources', 'emoji_df_keywords_ru.csv')
    df_src = pd.read_csv(df_src_filename)

    df_dest = pd.DataFrame(columns=['emoji', 'synsets', 'synsets_names'])
    df_dest_filename = os.path.join(os.path.dirname(__file__), '..', 'resources', 'emoji_df_synsets.csv')

    for i, row in df_src.iterrows():
        emoji = row['emoji']
        keywords_ru = json.loads(row['keywords_ru'])

        synsets = set()

        keywords_normalized = set()
        for keyword in keywords_ru.keys():
            keywords_normalized |= normalize_word_ru(keyword)
            for x in keywords_normalized:
                synsets |= get_word_synsets(x)

        synsets_list = list(synsets)
        synsets_names = [wn[x].title for x in synsets_list]

        print('({}) {} -> {} - {}'.format(i, emoji, synsets_list, synsets_names))

        df_dest = df_dest.append({
            'emoji': emoji,
            'synsets': json.dumps(synsets_list, ensure_ascii=False),
            'synsets_names': json.dumps(synsets_names, ensure_ascii=False),
        }, ignore_index=True)

        if i % 10 == 0:
            df_dest.to_csv(df_dest_filename)

    df_dest.to_csv(df_dest_filename)


if __name__ == '__main__':
    __main__()
