# Transcriber

A utility which uses the [whisper.cpp](https://github.com/ggerganov/whisper.cpp) to transcribe audio files. I wrote this [literally hours before @charliemarsh released this](https://github.com/charliermarsh/whisper.cpp-cli), but it was a fun task to use Pixi to build things from source.

## Getting started

- Install Pixi `curl -fsSL https://pixi.sh/install.sh | bash`
- Set up the whisper model: `pixi run install_whisper` 
  - Downloads and unzips the `whisper.cpp` repo
  - Builds the from source
  - Downloads `tiny.en` model
  - Cleans up build
- Run example: `python -m transcriber | jq -c`  (Will transcribe "`samples/bruce.mp3`")
  - Transcriber class will auto-convert audio files to WAV format at runtime

## Render the streamlit app:

`streamlit run app.py`

![streamlit_app](media/image.png)
