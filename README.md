# emoji dataset builder

My scripts pipeline to construct an emojis dataset.

The code quality is bad and it's not intented to be viewed by anyone.

## Installation

- `pip install -r requirements.txt`
- `ruwordnet download`
- `argospm update && argospm install translate-en_ru`
- `tar xvf resources/emjpd.org.tar.gz -C resources`
- `python` and:
```python
import nltk

nltk.download('punkt', 'resources')
nltk.download('wordnet', 'resources')
nltk.download('averaged_perceptron_tagger', 'resources')
nltk.download('universal_tagset', 'resources')
```