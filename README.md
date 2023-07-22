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
