import logging
from pydub import AudioSegment
import tempfile
import os

FRAME_RATE = 16_000
logger = logging.getLogger()


class Converter:
    def __init__(self, file_path: str):
        working_file = AudioSegment.from_file(file_path)
        self.temp_file_path = None
        # Create a temporary file to store the output
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
            temp_file_path = temp_file.name

            # Ensure the audio has a sample rate of 16 kHz
            if working_file.frame_rate != FRAME_RATE:
                working_file = working_file.set_frame_rate(FRAME_RATE)

            # Export the audio to the temporary file
            working_file.export(
                temp_file_path,
                format="wav",
            )

        # Do whatever you need to do with the temporary file
        # For now, let's just print the temporary file path
        logging.info("Temporary WAV file:", temp_file_path)
        self.temp_file_path = temp_file_path

    def clean_up(self):
        if self.temp_file_path:
            os.unlink(self.temp_file_path)


if __name__ == "__main__":
    Converter("samples/bruce.mp3")
