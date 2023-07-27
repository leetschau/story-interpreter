# Story Interpreter

Story interpreter *listen* to a audio file (by far only MP3 is supported),
and generate interpretion ebook (HTML & epub) via `quarto`.

## Prerequistes

* quarto
* openai-whisper
* nagisa
* jamdict

## Usage

```sh
python app.py sakura.mp3
quarto render sakura.qmd
```

Now you have a *sakura.html* and *sakura.epub* containing thorough explanations
about the transcriptions of the audio material.

## Configuration

Put known words file at ~/.config/story-interpreter/known-words.txt.
Every word a line, for example:
```
は
を
と
か
に
の
ます
です
これ
私
日本
人
```

You can use known-words.txt in this repo as a default template:
```sh
mkdir ~/.config/story-interpreter
cp known-words.txt ~/.config/story-interpreter
```

