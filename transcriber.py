import logging
import pathlib

from converter import Converter
from wrapper import WhisperWrapper

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger()


class Transcriber:
    def __init__(self, audio_path: str) -> None:
        self.converter = None
        working_path = pathlib.Path(audio_path)

        if not working_path.suffix.startswith(".wav"):
            logger.info(f"Converting {working_path.suffix} to .wav")
            self.converter = Converter(str(working_path))
            source_path = self.converter.temp_file_path
        else:
            source_path = str(working_path)

        transcriber = WhisperWrapper(source_path)
        print(transcriber.json)

        if self.converter:
            logger.info("Cleaning up temporary files")
            self.converter.clean_up()


if __name__ == "__main__":
    Transcriber("samples/bruce.mp3")
