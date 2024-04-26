import json
import os
import pathlib
import subprocess
import tempfile
import logging

logger = logging.getLogger()


class WhisperWrapper:
    def __init__(self, input_file_path:str, model_name="tiny.en"):
        if pathlib.Path(input_file_path).is_absolute():
            self.input_file_path = input_file_path
        else:
            self.input_file_path = str(pathlib.Path("../" + input_file_path))
        self.model_name = model_name
        self.json = self.process_input_file()

    def process_input_file(self):
        output_structure = {}

        # Create a temporary file
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as temp_file:
            output_file_path = temp_file.name

            # Define the command
            command = [
                "./main",
                "-m",
                f"models/ggml-{self.model_name}.bin",
                "-f",
                self.input_file_path,
                "--output-json-full",
                "--output-file",
                f"{output_file_path}",
            ]

            # Run the command
            try:
                logger.info(f"Executing command: {" ".join(command)}")
                process = subprocess.Popen(
                    command,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    cwd="whisper.cpp-master/",
                )
                _, stderr = process.communicate()

                # Check if the command was successful
                if process.returncode == 0:
                    logger.info("Command execution successful.")

                    # Read the output from the temporary file
                    with open(output_file_path + ".json", "r") as temp_output_file:
                        data = temp_output_file.read()
                        output_structure = json.loads(data)
                else:
                    logger.error("Error executing command: %s", command)
                    raise subprocess.SubprocessError()

            except Exception as e:
                logger.error("An error occurred: %s, %s", e, stderr)
                process.kill()  # Kill the process if an exception occurs
                raise  # Re-raise the exception

            finally:
                # Remove the temporary file
                os.unlink(output_file_path)
                pass

        return json.dumps(output_structure)


if __name__ == "__main__":
    print(WhisperWrapper("samples/jfk.wav").json)
