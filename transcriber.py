import pathlib

from converter import Converter
from wrapper import WhisperWrapper


class Transcriber:
    def __init__(self, audio_path) -> None:
        self.converter = None
        working_path = pathlib.Path(audio_path)

        if not working_path.suffix.startswith(".wav"):
            self.converter = Converter(str(working_path))
            source_path = self.converter.temp_file_path
        else:
            source_path = str(working_path)

        transcriber = WhisperWrapper(source_path)
        print(transcriber.json)

        if self.converter:
            self.converter.clean_up()


if __name__ == "__main__":
    Transcriber("samples/bruce.mp3")
