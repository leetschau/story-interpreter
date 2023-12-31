import sys
import whisper
import nagisa
from jamdict import Jamdict
from pathlib import Path
import translators as ts
import pickle

from header import qmd_header

inp = Path(sys.argv[1])
kwp = Path.home() / '.config/story-interpreter/known-words.txt'
header = qmd_header(inp.stem)

if kwp.is_file():
    kwl = open(kwp).readlines()
    known_words = set([w.strip() for w in kwl])
else:
    known_words = set()

print(f'Known words: {known_words}')

linesep = '\n\n'
jam = Jamdict()
cache = inp.with_suffix('.pkl')

if inp.suffix == '.mp3':
    if cache.is_file():
        with open(cache, 'rb') as f:
            tres = pickle.load(f)
        print(f'Load speech recognition from {cache}')
    else:
        afile = whisper.load_audio(inp)
        model = whisper.load_model("large-v2")
        tres = {
            'transcript':
                model.transcribe(afile, language='Japanese', initial_prompt='漢字で書き写す'),
            'translation':
                model.transcribe(afile, task='translate')}
        with open(cache, 'wb') as f:
            pickle.dump(tres, f)
        print(f'Write cache file to {cache}')
elif inp.suffix == '.txt':
    text = open(inp, 'r').read()
    transtext = ts.translate_text(text, translator='iciba', from_language='ja', to_language='zh')
    tres = {'transcript': {'segments': [{'text': line} for line in text.split('\n')]},
            'translation': {'segments': [{'text': line} for line in transtext.split('\n')]}}
    print(tres)
else:
    sys.exit('Only files with extension mp3 and txt are supported!')


vocab = {}
lines = []

for si, sentence in enumerate(tres['transcript']['segments']):
    words = nagisa.tagging(sentence['text'])
    bw = []
    for idx, word in enumerate(words.words):
        if len(word.strip()) == 0:
            continue
        if (word in vocab) or (word in known_words):
            bw.append(word)
        else:
            exp = "\n".join([ent.text() for ent in jam.lookup(word).entries])
            vocab[word] = f'{words.postags[idx]}, {exp}'
            bw.append(f'{word} [^{word}]')
    lines.append(' '.join(bw))

translationstr = linesep.join([line['text'] for line in tres['translation']['segments']])
body = (f"# Text{linesep}{linesep.join(lines)}{linesep}"
        f"# Translation{linesep}{translationstr}")
dictstr = linesep.join([f'[^{k}]: {v}' for k, v in vocab.items()])

with open(inp.with_suffix('.qmd'), 'w') as f:
    f.write(f'{header}{linesep}{linesep}{body}{linesep}{linesep}{dictstr}')
