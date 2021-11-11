from razdel import tokenize
from pymorphy2 import MorphAnalyzer
from pymystem3 import Mystem
from ruwordnet import RuWordNet

from typing import Iterator


class Tokenizer:
    def __init__(self, morph: MorphAnalyzer):
        self.morph = morph

    def normalize(self, token: str) -> str:
        print('->', token)
        print(self.morph.normal_forms(token))

        parsed = self.morph.parse(word)
        print(parsed)

        parsed[0].inflect({})

        return token

    def tokenize(self, text: str) -> Iterator[str]:
        # TODO: split the sentence
        for token in tokenize(text):
            yield self.normalize(token)


def model_to_dict(model):
    return {i.name: getattr(model, i.name) for i in model.__table__.columns}


if __name__ == '__main__':
    morph = MorphAnalyzer()
    tz = Tokenizer(morph)
    m = Mystem()
    wn = RuWordNet()

    words = ['сковородка', 'сковорода', 'сковородки',
             'генерировать', 'сгенерировано']
    for word in words:
        print('morph.parse:', morph.parse(word))
        print('m.lemmatize:', m.lemmatize(word))
        print('m.analyze:', m.analyze(word))
        print('wn.get_senses', wn.get_senses(word))

        senses = wn.get_senses(word)
        if len(senses) > 0:
            print('wn.get_senses[0]', model_to_dict(senses[0]))
        print()

    # words = ['улыбка', 'улыбаться', 'улыбался', 'сковородка']
    #
    # for word in words:
    #     tz.normalize(word)
