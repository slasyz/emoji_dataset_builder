from ruwordnet import RuWordNet
from ruwordnet.models import Sense, Synset


class Thesaurus:
    def __init__(self, wn: RuWordNet):
        self.wn = wn

    def get_hypernym(self, word: str):
        pass


def print_sense(sense: Sense):
    print('sense:', sense)
    print('id =', sense.id)
    print('lemma =', sense.lemma)
    print('name =', sense.name)
    print('synset_id =', sense.synset_id)


def print_synset(synset: Synset):
    print('synset:', synset)
    print('hypernyms:', synset.hypernyms)
    print('hyponyms:', synset.hyponyms)


if __name__ == '__main__':
    wn = RuWordNet()
    th = Thesaurus(wn)

    # words = ['привет', 'сковородка',
    #          'спаржа', 'средневековый замок', 'замок', 'авокадо']
    words = ['улыбка']
    for word in words:
        print()
        print('-'*(len(word) + 4))
        print('- {} -'.format(word))
        print('-'*(len(word) + 4))

        senses = wn.get_senses(word)
        for sense in senses:
            print('---------------------')
            print_sense(sense)
            print_synset(sense.synset)
