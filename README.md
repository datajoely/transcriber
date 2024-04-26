# Transcriber

A utility which uses the [whisper.cpp](https://github.com/ggerganov/whisper.cpp) to transcribe audio files

## Getting started

- Install Pixi `curl -fsSL https://pixi.sh/install.sh | bash`
- Set up the whisper model: `pixi run install_whisper` 
  - Downloads and unzips the `whisper.cpp` repo
  - Builds the from source
  - Downloads `tiny.en` model
  - Cleans up
- Run pass an MP3 to the model as WAV: `python -m transcriber  | jq -c`  
