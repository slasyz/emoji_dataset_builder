import json
import os

import pandas as pd
from ruwordnet import RuWordNet

wn = RuWordNet()


def __main__():
    df_src_filename = os.path.join(os.path.dirname(__file__), '..', 'resources', 'emoji_df_synsets.csv')
    df_src = pd.read_csv(df_src_filename)

    df_dest = pd.DataFrame(columns=['synset', 'name', 'emojis'])
    df_dest_filename = os.path.join(os.path.dirname(__file__), '..', 'resources', 'emoji_df_result.csv')

    synset_to_emojis = {}

    for i, row in df_src.iterrows():
        emoji = row['emoji']
        synsets = json.loads(row['synsets'])

        for synset in synsets:
            emojis = synset_to_emojis.get(synset, [])
            emojis.append(emoji)
            synset_to_emojis[synset] = emojis

    for synset, emojis in synset_to_emojis.items():
        df_dest = df_dest.append({
            'synset': synset,
            'name': wn[synset].title,
            'emojis': json.dumps(emojis, ensure_ascii=False),
        }, ignore_index=True)
    df_dest.to_csv(df_dest_filename)


if __name__ == '__main__':
    __main__()
