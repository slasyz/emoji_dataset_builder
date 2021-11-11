# На маке не работает argostranslate, поэтому этот скрипт нужно запускать на линуксе.
# pip install argostranslate pandas
# argospm update && argospm install translate-en_ru

import json
import os

import pandas as pd
from argostranslate import translate


installed_languages = translate.load_installed_languages()
translation_en_ru = installed_languages[0].get_translation(installed_languages[1])


translate_cache = {}


def translate(s: str) -> str:
    cached = translate_cache.get(s)
    if cached is not None:
        return cached

    res = translation_en_ru.translate(s)
    translate_cache[s] = res
    return res


def __main__():
    df_src_filename = os.path.join(os.path.dirname(__file__), 'emoji_df_keywords.csv')
    df_src = pd.read_csv(df_src_filename)

    df_dest = pd.DataFrame(columns=['emoji', 'keywords_ru'])
    df_dest_filename = os.path.join(os.path.dirname(__file__), 'emoji_df_keywords_ru.csv')

    for i, row in df_src.iterrows():
        emoji = row['emoji']
        keywords = json.loads(row['keywords'])

        keywords_ru = {}

        for keyword, count in keywords.items():
            keyword_ru = translate(keyword)
            keywords_ru[keyword_ru] = count

        print('({}) {} -> {}'.format(i, emoji, keywords_ru))

        df_dest = df_dest.append({
            'emoji': emoji,
            'keywords_ru': json.dumps(keywords_ru, ensure_ascii=False),
        }, ignore_index=True)

        if i % 10 == 0:
            df_dest.to_csv(df_dest_filename)

    df_dest.to_csv(df_dest_filename)


if __name__ == '__main__':
    __main__()
