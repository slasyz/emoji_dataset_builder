import hashlib
import json
import os
import re
import urllib.parse as up

import requests
from lxml import html
import pandas as pd


df_src_filename = os.path.join(os.path.dirname(__file__), '..', 'resources', 'emoji_df_src.csv')
df_src = pd.read_csv(df_src_filename)

df_clean_eng = pd.DataFrame(columns=['emoji', 'src_meanings', 'clean_meanings'])
df_clean_eng_filename = os.path.join(os.path.dirname(__file__), '..', 'resources', 'emoji_df_clean_eng.csv')


def get_with_cache(url: str) -> str:
    host = up.urlparse(url).netloc
    hash = hashlib.md5(url.encode('utf-8')).hexdigest()
    filepath = os.path.join(os.path.dirname(__file__), '..', 'resources', host, hash + '.html')

    try:
        with open(filepath, 'r') as f:
            # print('reading {} from file ({})'.format(url, filepath))
            return f.read()
    except FileNotFoundError:
        pass

    with requests.get(url) as req:
        if not req.ok:
            print(req.content)
            raise Exception('Response not ok.')
        # print('reading {} from url'.format(url))
        data = req.content.decode('utf-8', 'ignore')

    with open(filepath, 'w') as f:
        # print('dumping {} to file ({})'.format(url, filepath))
        f.write(data)

    return data


def remove_regexp(r: str, s: str) -> str:
    return re.compile(r).sub('', s)


def clean_emoji_text(s: str):
    result = []

    s = s.lower()
    if 'face with ' in s:
        s = s.replace('face with ', '')
    s = re.sub(r'[,:] [a-z-]+ skin tone', '', s)
    s = re.sub(r'[,:] [a-z]+ hair', '', s)
    s = s.replace(', bald', '')
    s = re.sub(r'\s+', ' ', s)

    rx = re.compile(r'[,:] beard')
    if len(rx.findall(s)) > 0:
        result.append('beard')
        s = rx.sub('', s)

    s = re.sub(r'^(man|woman|person) (in|with) ', '', s)
    s = re.sub(r'^(left|right)-facing ', '', s)
    s = re.sub(r' room$', '', s)
    s = re.sub(r' (gesture|hand)$', '', s)
    if s.startswith('woman '):
        return []
    s = re.sub(r'^(man|person) ', '', s)
    s = s.removeprefix('playing ')
    s = s.removeprefix('flag: ')
    s = s.removeprefix('keycap digit')

    if ' and ' in s:
        for x in s.split(' and '):
            result += clean_emoji_text(x)
        return result

    s = re.sub(r'\s+', ' ', s)
    result.append(s)
    return result


for i, row in df_src.iterrows():
    emoji = row['emoji']
    name = row['name']
    group = row['group']
    subgroup = row['sub_group']

    src_meanings = []

    url = 'https://emojipedia.org/{}'.format(emoji)
    data = get_with_cache(url)

    parser = html.HTMLParser(encoding='utf-8')
    document = html.document_fromstring(data, parser=parser)
    elements = document.xpath('.//h1')
    main_meaning = elements[0].text_content()
    main_meaning = re.sub(r'^\S+', '', main_meaning).strip()
    src_meanings.append(main_meaning)

    elements = document.xpath(".//h2[text() = 'Also Known As']")
    if len(elements) > 0:
        elements = elements[0].xpath('./following::ul[1]/li')
        for el in elements:
            add_meaning = el.text_content()
            add_meaning = re.sub(r'^\S+', '', add_meaning).strip()
            src_meanings.append(add_meaning)

    clean_meanings = [clean_emoji_text(x) for x in src_meanings]
    clean_meanings = [x for sublist in clean_meanings for x in sublist]
    df_clean_eng = df_clean_eng.append({
        'emoji': emoji,
        'src_meanings': json.dumps(src_meanings),
        'clean_meanings': json.dumps(clean_meanings),
    }, ignore_index=True)
    print(i, end='.')
    if i % 100 == 0:
        print()

    if i % 300 == 3:
        df_clean_eng.to_csv(df_clean_eng_filename)

df_clean_eng.to_csv(df_clean_eng_filename)
