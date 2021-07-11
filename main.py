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

        if self.extension == "py":
            t1 = threading.Thread(target=self.modify_python())
            t1.start()

        if self.extension == "cpp":
            t1 = threading.Thread(target=self.modify_cpp())
            t1.start()

    def fetch_commands(self, language):
        # Open the file and load the file
        print(language)
        with open("programming_commands.yaml") as f:
            data = yaml.load(f, Loader=SafeLoader)
            commands = data[language]

        return commands

    def modify_cpp(self):
        commands = self.fetch_commands("cpp")
        print(commands)

    def modify_python(self):
        """Modify the transcript according to python language"""

        self.transcript = self.transcript.lower()
        words = self.transcript.split(' ')
        commands = self.fetch_commands("python")

        print("Transcript= " + self.transcript)

        skipItr = False
        skipNxtItr = False
        moveLeft = 0
        moveRight = 0

        for i, val in enumerate(words):
            print(val, i)
            if val == "text":
                j = 0
                for j, value in enumerate(words):
                    if value == "text":
                        continue
                    simulatekeys(words[j])
                break
            if skipNxtItr:
                skipNxtItr = False
                continue
            if skipItr:
                skipItr = False
                continue
            if val == "up":
                pyautogui.press("up")
                continue
            if val == "down":
                pyautogui.press("down")
                continue
            if val == "left":
                pyautogui.press("left")
                continue
            if val == "right":
                pyautogui.press("right")
                continue
            if i == (len(words) - 1):
                print("Do nothing")
            else:
                if words[i] + words[i + 1] == "dictionaryitem":
                    skipItr = True
                    skipNxtItr = True
                    simulatekeys('"":""')
                    self.moveLeft(4)
                    continue
                if words[i] + words[i + 1] == "copystatement" or words[i] + words[i + 1] == "ctrl" or words[i] + words[
                    i + 1] == "controlc":
                    pyautogui.hotkey("shift", "end")
                    pyautogui.hotkey("ctrl", "c")
                    skipItr = True
                    continue
                if words[i] + words[i + 1] == "pastestatement" or words[i] + words[i + 1] == "ctrl-v" or words[i] + \
                        words[i + 1] == "controlv":
                    pyautogui.hotkey("ctrl", "v")
                    print("Paste")
                    skipItr = True
                    continue
                if words[i] + words[i + 1] == "doublequotes" or words[i] + words[i + 1] == "doublecoats" or words[i] + \
                        words[i + 1] == "doublecode" or words[i] + words[i + 1] == "doublecourts":
                    skipItr = True
                    simulatekeys('""')
                    self.moveLeft(1)
                    continue
                if words[i] + words[i + 1] == "singlequotes" or words[i] + words[i + 1] == "singlecoats" or words[i] + \
                        words[i + 1] == "singlecode":
                    skipItr = True
                    simulatekeys("''")
                    self.moveLeft(1)
                    continue
                if words[i] + words[i + 1] == "stringitem":
                    skipItr = True
                    simulatekeys("'',")
                    self.moveLeft(2)
                    moveRight = 1
                    continue
                if words[i] + words[i + 1] == "callme" or words[i] + words[i + 1] == "callme":
                    skipItr = True
                    simulatekeys(",")
                    continue
                if words[i] + words[i + 1] == "goto":
                    self.gotoLine(words[i + 2])
                    skipItr = True
                    skipNxtItr = True
                    continue
                if words[i] + words[i + 1] == "capslock":
                    pyautogui.press("capslock")
                if words[i] + words[i + 1] == "moveup":
                    self.moveUp(1)
                    skipItr = True
                    continue
                if words[i] + words[i + 1] == "movedown":
                    self.moveDown(1)
                    skipItr = True
                    continue
                if words[i] + words[i + 1] == "moveleft":
                    self.moveLeft(1)
                    skipItr = True
                    continue
                if words[i] + words[i + 1] == "moveright":
                    self.moveRight(1)
                    skipItr = True
                    continue
                if words[i] + words[i + 1] == "skipright":
                    self.skipRight()
                    skipItr = True
                    continue
                if words[i] + words[i + 1] == "skipleft":
                    self.skipLeft()
                    skipItr = True
                    continue
                if words[i] + words[i + 1] == "scrollup":
                    self.mouseScrollUp()
                    skipItr = True
                    continue
                if words[i] + words[i + 1] == "scrolldown":
                    self.mouseScrollDown()
                    skipItr = True
                    continue
                if words[i] + words[i + 1] == "init":
                    simulatekeys("__init__")
                    skipItr = True
                    continue
            print("Val = ", commands)
            try:
                # backslash
                print("Here" + commands[val])
                simulatekeys(commands[val])
                if val == "if":
                    self.moveLeft(1)
                if val == "list":
                    self.moveLeft(1)
                if val == "function":
                    self.moveLeft(3)
                    continue
                if val == "askew":
                    self.moveLeft(1)
                if val == "print":
                    self.moveLeft(2)
                if val == "class":
                    self.moveLeft(2)
                    continue

            except Exception as e:
                print(e)
                if val == "backspace":
                    pyautogui.press("backspace")
                    continue
                if val == "capitalize" or val == "capitalized":
                    words[i + 1] = words[i + 1].capitalize()
                    continue
                if val == "undo":
                    pyautogui.hotkey("ctrl", "z")
                    continue
                if val == "end" or val == "and":
                    self.gotoEnd()
                    continue
                if val == "end" or val == "and":
                    self.gotoEnd()
                    continue
                simulatekeys(val)
                if moveLeft != 0:
                    self.moveLeft(1)
                if moveRight != 0:
                    print(moveRight)
                    moveRight = 0
                    self.moveRight(2)

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
