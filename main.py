from __future__ import division

import re
import sys
import os
import threading
from google.cloud import speech
import pyaudio
from six.moves import queue
import pyautogui
from sys import platform as _platform
import win32gui
import yaml
from yaml.loader import SafeLoader

print(_platform)

# Audio recording parameters
RATE = 16000
CHUNK = int(RATE / 10)  # 100ms

# Service Account Info
credential_path = "ava-daemon-4ce53760f667.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path


class TranscriptModifier(object):
    """Modifies the transcript according to the type of file detected"""

    def __init__(self, transcript, extension):
        """Check the currently working file type in the __init__()"""
        self.transcript = transcript
        self.languages = ["html", "py", "js", "css", "cpp"]
        self.extension = extension

        commands = self.fetch_commands(self.extension)
        if self.extension == "py":
            t1 = threading.Thread(target=self.modify_transcript(commands))
            t1.start()

        if self.extension == "cpp":
            t1 = threading.Thread(target=self.modify_transcript(commands))
            t1.start()

    def fetch_commands(self, language):
        # Open the file and load the file
        print(language)
        with open("programming_commands.yaml") as f:
            data = yaml.load(f, Loader=SafeLoader)
            commands = data[language]
        return commands

    def modify_transcript(self, commands):
        self.transcript = self.transcript.lower()
        words = self.transcript.split(' ')
        length = len(words)
        print("Transcript= " + self.transcript)
        print(f"Length= {length}")

        skipNxtItr = False
        for i, val in enumerate(words):
            print(f"I = {i}")
            if skipNxtItr:
                skipNxtItr = False
                print("Skipped")
                continue
            if length != 1 and i != (length - 1):
                if val + words[i + 1] == "elsa" or val == "elsafe" or val + words[i + 1] == "elsea" or val + words[i + 1] == "elseif":
                    simulatekeys("else if(){\n\n}")
                    simulatekeys("\t")
                    self.moveLeft(5)
                    skipNxtItr = True
                    continue

            if val == "text":
                for j, value in enumerate(words):
                    if j == 0:
                        continue
                    try:
                        simulatekeys(value)
                    except Exception as e:
                        print(e)
                        break
                break

            try:
                simulatekeys(commands[val][0])
                print(commands[val][0])
                print("Try Block")
                if len(commands[val]) > 1:
                    for j in range(len(commands[val][1]['direction'])):
                        if j % 2 != 0:
                            continue
                        if commands[val][1]['direction'][j] == "ctrl+right":
                            self.move_ctrl_right(commands[val][1]['direction'][j + 1])

                        if commands[val][1]['direction'][j] == "ctrl+left":
                            self.move_ctrl_left(commands[val][1]['direction'][j + 1])

                        if commands[val][1]['direction'][j] == "up":
                            # Up def ():
                            print("Here is UP")
                            self.moveUp(commands[val][1]["direction"][j + 1])
                            continue
                        if commands[val][1]['direction'][j] == "down":
                            # Down def ():
                            self.moveDown(commands[val][1]["direction"][j + 1])
                            continue
                        if commands[val][1]['direction'][j] == "left":
                            # Left
                            print("LEFT")
                            self.moveLeft(int(commands[val][1]["direction"][j + 1]))

                            if commands[val][1]['direction'][j] == "right":
                                # Right
                                self.moveRight(commands[val][1]["direction"][j + 1])
                                continue
                continue
            except Exception as e:
                print("Exception = ", e)
                simulatekeys(val)
                continue

    def modify_cpp(self):
        commands = self.fetch_commands("cpp")
        print(commands)

    def modify_python(self):
        """Modify the transcript according to python language"""

        self.transcript = self.transcript.lower()
        words = self.transcript.split(' ')
        commands = self.fetch_commands("python")

        print("Transcript= " + self.transcript)

        for i, val in enumerate(words):
            if val == "text":
                for j, value in enumerate(words):
                    if j == 0:
                        continue
                    try:
                        simulatekeys(value)
                    except Exception as e:
                        print(e)
                        break
                break

            try:
                simulatekeys(commands[val][0])
                if commands[val][1]['direction'] == "up":
                    # Up def ():
                    print("Here is UP")
                    self.moveUp(commands[val][1])
                    continue
                if commands[val][1]['direction'] == "down":
                    # Down def ():
                    self.moveDown(commands[val][2])
                    continue
                if commands[val][1]['direction'] == "left":
                    # Left
                    print("LEFT")
                    self.moveLeft(commands[val][2])
                    continue
                if commands[val][1]['direction'] == "right":
                    # Right
                    self.moveRight(commands[val][2])
                    continue

            except Exception as e:
                print("Exception")
                simulatekeys(val)

    def moveLeft(self, index):
        print("Inside moveLeft")
        for i in range(index):
            pyautogui.press("left")

    def moveRight(self, index):
        for i in range(index):
            pyautogui.press("right")

    def moveUp(self, index):
        for i in range(index):
            pyautogui.press("up")

    def moveDown(self, index):
        for i in range(index):
            pyautogui.press("down")

    def move_ctrl_right(self, index):
        for i in range(index):
            pyautogui.hotkey("ctrl", "right")

    def move_ctrl_left(self, index):
        for i in range(index):
            pyautogui.hotkey("ctrl", "right")

    def skipLeft(self):
        pyautogui.hotkey("ctrl", "left")

    def skipRight(self):
        pyautogui.hotkey("ctrl", "right")

    def mouseScrollUp(self):
        pyautogui.press("pageup")

    def mouseScrollDown(self):
        pyautogui.press("pagedown")

    def gotoEnd(self):
        pyautogui.press("end")

    def gotoLine(self, line):
        pyautogui.hotkey("ctrl", "g")
        pyautogui.typewrite(line)
        pyautogui.press("enter")


class MicrophoneStream(object):
    """Opens a recording stream as a generator yielding the audio chunks."""

    def __init__(self, rate, chunk):
        self._rate = rate
        self._chunk = chunk

        # Create a thread-safe buffer of audio data
        self._buff = queue.Queue()
        self.closed = True

    def __enter__(self):
        self._audio_interface = pyaudio.PyAudio()
        self._audio_stream = self._audio_interface.open(
            format=pyaudio.paInt16,
            # The API currently only supports 1-channel (mono) audio
            # https://goo.gl/z757pE
            channels=1,
            rate=self._rate,
            input=True,
            frames_per_buffer=self._chunk,
            stream_callback=self._fill_buffer,
        )

        self.closed = False

        return self

    def __exit__(self, types, value, traceback):
        self._audio_stream.stop_stream()
        self._audio_stream.close()
        self.closed = True
        self._buff.put(None)
        self._audio_interface.terminate()

    def _fill_buffer(self, in_data, frame_count, time_info, status_flags):
        """Continuously collect data from the audio stream, into the buffer."""
        self._buff.put(in_data)
        return None, pyaudio.paContinue

    def generator(self):
        while not self.closed:
            chunk = self._buff.get()
            if chunk is None:
                return
            data = [chunk]

            # Now consume whatever other data's still buffered.
            while True:
                try:
                    chunk = self._buff.get(block=False)
                    if chunk is None:
                        return
                    data.append(chunk)
                except queue.Empty:
                    break

            yield b"".join(data)


def simulatekeys(transcript):
    """Simulates the keys as the speech is recognized"""
    pyautogui.write(transcript)
    keys = transcript
    # for key in keys:
    #     pyautogui.write(key)


def checkFocus():
    """Loop to check the application focus continuously from the list"""
    # time.sleep(4)
    while True:
        window = win32gui.GetForegroundWindow()
        # Select the Editor and will wait till that Application is in foreground
        active_window_name = win32gui.GetWindowText(window)
        print("Window Name = " + active_window_name)
        if active_window_name == 'ava-desktop – main.cpp':
            break
    return True if active_window_name == 'ava-desktop – main.cpp' else False


def listen_print_loop(responses, extension):
    """Iterates through server responses and prints them"""
    num_chars_printed = 0
    for response in responses:
        if not response.results:
            continue

        # The `results` list is consecutive. For streaming, we only care about
        # the first result being considered, since once it's `is_final`, it
        # moves on to considering the next utterance.
        result = response.results[0]
        if not result.alternatives:
            continue

        # Display the transcription of the top alternative.
        transcript = result.alternatives[0].transcript

        # Display interim results, but with a carriage return at the end of the
        # line, so subsequent lines will overwrite them.
        #
        # If the previous result was longer than this one, we need to print
        # some extra spaces to overwrite the previous result
        overwrite_chars = " " * (num_chars_printed - len(transcript))
        if not result.is_final:

            sys.stdout.write(transcript + overwrite_chars + "\r")
            sys.stdout.flush()

            num_chars_printed = len(transcript)

        else:
            final_transcript = transcript + overwrite_chars
            TranscriptModifier(final_transcript, extension)

            # Exit recognition if any of the transcribed phrases could be
            # one of our keywords.
            if re.search(r"\b(exit|quit)\b", transcript, re.I):
                print("Exiting..")
                break

            num_chars_printed = 0


# noinspection PyTypeChecker
def main():
    language_code = "en-US"  # a BCP-47 language tag

    client = speech.SpeechClient()
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code=language_code,
        enable_automatic_punctuation=False,
    )

    streaming_config = speech.StreamingRecognitionConfig(
        config=config, interim_results=True
    )
    if checkFocus():
        with MicrophoneStream(RATE, CHUNK) as stream:
            audio_generator = stream.generator()
            requests = (
                speech.StreamingRecognizeRequest(audio_content=content)
                for content in audio_generator
            )

            responses = client.streaming_recognize(streaming_config, requests)

            # Now, put the transcription responses to use.
            # Extension Argument Added
            listen_print_loop(responses, "cpp")


if __name__ == "__main__":
    main()
