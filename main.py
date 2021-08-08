from __future__ import division

import platform
import re
import sys
import os
import threading
import time

from google.cloud import speech
import pyaudio
from six.moves import queue
import pyautogui
import platform as _platform
import yaml
from yaml.loader import SafeLoader

print(f"Platform = {platform.system()}")
if _platform.system() == "Linux":
    import gi

    gi.require_version("Wnck", "3.0")
    from gi.repository import Wnck

if _platform.system() == "Windows":
    import win32gui

# Audio recording parameters
STREAMING_LIMIT = 240000  # 4 minutes
SAMPLE_RATE = 16000
CHUNK_SIZE = int(SAMPLE_RATE / 10)  # 100ms
RED = "\033[0;31m"
GREEN = "\033[0;32m"
YELLOW = "\033[0;33m"
istyping = False
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
            t1 = threading.Thread(target=self.modify_programming_ext(commands))
            t1.start()

        if self.extension == "cpp":
            t1 = threading.Thread(target=self.modify_programming_ext(commands))
            t1.start()

    def fetch_commands(self, ext):
        # Open the file and load the file
        print(ext)
        if ext == "word":
            with open("word_commands.yaml") as f:
                data = yaml.load(f, Loader=SafeLoader)
                commands = data[ext]
        else:
            with open("programming_commands.yaml") as f:
                data = yaml.load(f, Loader=SafeLoader)
                commands = data[ext]
        return commands

    def modify_word_ext(self, commands):
        pass

    def modify_programming_ext(self, commands):
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
                if type(commands[val]) == list:
                    simulatekeys(commands[val][0])
                else:
                    simulatekeys(commands[val])
                    continue
                print(commands[val])
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
            pyautogui.hotkey("ctrl", "left")

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


def get_current_time():
    """Return Current Time in MS."""

    return int(round(time.time() * 1000))


class ResumableMicrophoneStream:
    """Opens a recording stream as a generator yielding the audio chunks."""

    def __init__(self, rate, chunk_size):
        self._rate = rate
        self.chunk_size = chunk_size
        self._num_channels = 1
        self._buff = queue.Queue()
        self.closed = True
        self.start_time = get_current_time()
        self.restart_counter = 0
        self.audio_input = []
        self.last_audio_input = []
        self.result_end_time = 0
        self.is_final_end_time = 0
        self.final_request_end_time = 0
        self.bridging_offset = 0
        self.last_transcript_was_final = False
        self.new_stream = True
        self._audio_interface = pyaudio.PyAudio()
        self._audio_stream = self._audio_interface.open(
            format=pyaudio.paInt16,
            channels=self._num_channels,
            rate=self._rate,
            input=True,
            frames_per_buffer=self.chunk_size,
            # Run the audio stream asynchronously to fill the buffer object.
            # This is necessary so that the input device's buffer doesn't
            # overflow while the calling thread makes network requests, etc.
            stream_callback=self._fill_buffer,
        )

    def __enter__(self):

        self.closed = False
        return self

    def __exit__(self, type, value, traceback):

        self._audio_stream.stop_stream()
        self._audio_stream.close()
        self.closed = True
        # Signal the generator to terminate so that the client's
        # streaming_recognize method will not block the process termination.
        self._buff.put(None)
        self._audio_interface.terminate()

    def _fill_buffer(self, in_data, *args, **kwargs):
        """Continuously collect data from the audio stream, into the buffer."""

        self._buff.put(in_data)
        return None, pyaudio.paContinue

    def setExit(self):
        self.closed = True

    def generator(self):
        """Stream Audio from microphone to API and to local buffer"""

        while not self.closed:
            data = []

            if self.new_stream and self.last_audio_input:

                chunk_time = STREAMING_LIMIT / len(self.last_audio_input)

                if chunk_time != 0:

                    if self.bridging_offset < 0:
                        self.bridging_offset = 0

                    if self.bridging_offset > self.final_request_end_time:
                        self.bridging_offset = self.final_request_end_time

                    chunks_from_ms = round(
                        (self.final_request_end_time - self.bridging_offset)
                        / chunk_time
                    )

                    self.bridging_offset = round(
                        (len(self.last_audio_input) - chunks_from_ms) * chunk_time
                    )

                    for i in range(chunks_from_ms, len(self.last_audio_input)):
                        data.append(self.last_audio_input[i])

                self.new_stream = False

            # Use a blocking get() to ensure there's at least one chunk of
            # data, and stop iteration if the chunk is None, indicating the
            # end of the audio stream.
            chunk = self._buff.get()
            self.audio_input.append(chunk)

            if chunk is None:
                return
            data.append(chunk)
            # Now consume whatever other data's still buffered.
            while True:
                try:
                    chunk = self._buff.get(block=False)

                    if chunk is None:
                        return
                    data.append(chunk)
                    self.audio_input.append(chunk)

                except queue.Empty:
                    break

            yield b"".join(data)


def simulatekeys(transcript):
    """Simulates the keys as the speech is recognized"""
    if istyping:
        keys = transcript
        for key in keys:
            pyautogui.write(key)
    else:
        pyautogui.write(transcript)


def checkFocus():
    """Loop to check the application focus continuously from the list"""

    '''
    # Get current focused window title in Linux 
    import gi
    import time
    
    gi.require_version("Wnck", "3.0")
    from gi.repository import Wnck
    
    time.sleep(2)
    scr = Wnck.Screen.get_default()
    scr.force_update()
    print(scr.get_active_window().get_name())
    '''
    while True:
        if _platform.system() == 'Windows':
            time.sleep(2)
            window = win32gui.GetForegroundWindow()
            # Select the Editor and will wait till that Application is in foreground
            active_window_name = win32gui.GetWindowText(window)
            print("Window Name = " + active_window_name)
            if active_window_name == 'ava-desktop – main.cpp':
                break
        if _platform.system() == 'Linux':
            time.sleep(2)
            scr = Wnck.Screen.get_default()
            scr.force_update()
            print(scr.get_active_window().get_name())
    return True if active_window_name == 'ava-desktop – main.cpp' else False


def listen_print_loop(responses, stream, extension):
    """Iterates through server responses and prints them.

    The responses passed is a generator that will block until a response
    is provided by the server.

    Each response may contain multiple results, and each result may contain
    multiple alternatives; for details, see https://goo.gl/tjCPAU.  Here we
    print only the transcription for the top alternative of the top result.

    In this case, responses are provided for interim results as well. If the
    response is an interim one, print a line feed at the end of it, to allow
    the next result to overwrite it, until the response is a final one. For the
    final one, print a newline to preserve the finalized transcription.
    """

    for response in responses:

        if get_current_time() - stream.start_time > STREAMING_LIMIT:
            stream.start_time = get_current_time()
            break

        if not response.results:
            continue

        result = response.results[0]

        if not result.alternatives:
            continue

        transcript = result.alternatives[0].transcript

        result_seconds = 0
        result_micros = 0

        if result.result_end_time.seconds:
            result_seconds = result.result_end_time.seconds

        if result.result_end_time.microseconds:
            result_micros = result.result_end_time.microseconds

        stream.result_end_time = int((result_seconds * 1000) + (result_micros / 1000))

        corrected_time = (
                stream.result_end_time
                - stream.bridging_offset
                + (STREAMING_LIMIT * stream.restart_counter)
        )
        # Display interim results, but with a carriage return at the end of the
        # line, so subsequent lines will overwrite them.

        if result.is_final:

            sys.stdout.write(GREEN)
            sys.stdout.write("\033[K")
            sys.stdout.write(str(corrected_time) + ": " + transcript + "\n")

            stream.is_final_end_time = stream.result_end_time
            stream.last_transcript_was_final = True
            TranscriptModifier(transcript, extension)
            # Exit recognition if any of the transcribed phrases could be
            # one of our keywords.
            if re.search(r"\b(exit|quit)\b", transcript, re.I):
                sys.stdout.write(YELLOW)
                sys.stdout.write("Exiting...\n")
                stream.closed = True
                break

        else:
            sys.stdout.write(RED)
            sys.stdout.write("\033[K")
            sys.stdout.write(str(corrected_time) + ": " + transcript + "\r")

            stream.last_transcript_was_final = False


class AudioManager:
    """"
    It is a class that manages the audio stream, start and pause.
    Provides a control from the user interface
    """

    def __init__(self):
        self.language_code = "en-US"  # a BCP-47 language tag
        self.client = speech.SpeechClient()
        self.config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=SAMPLE_RATE,
            language_code=self.language_code,
            enable_automatic_punctuation=False,
        )

        self.streaming_config = speech.StreamingRecognitionConfig(
            config=self.config, interim_results=True,
        )
        self.mic_manager = ResumableMicrophoneStream(SAMPLE_RATE, CHUNK_SIZE)

    def stop(self):
        self.mic_manager.setExit()

    def start(self):
        if checkFocus():
            with self.mic_manager as stream:

                while not stream.closed:
                    sys.stdout.write(YELLOW)
                    sys.stdout.write(
                        "\n" + str(STREAMING_LIMIT * stream.restart_counter) + ": NEW REQUEST\n"
                    )

                    stream.audio_input = []
                    audio_generator = stream.generator()

                    requests = (
                        speech.StreamingRecognizeRequest(audio_content=content)
                        for content in audio_generator
                    )

                    responses = self.client.streaming_recognize(self.streaming_config, requests)

                    # Now, put the transcription responses to use.
                    listen_print_loop(responses, stream, "cpp")

                    if stream.result_end_time > 0:
                        stream.final_request_end_time = stream.is_final_end_time
                    stream.result_end_time = 0
                    stream.last_audio_input = []
                    stream.last_audio_input = stream.audio_input
                    stream.audio_input = []
                    stream.restart_counter = stream.restart_counter + 1

                    if not stream.last_transcript_was_final:
                        sys.stdout.write("\n")
                    stream.new_stream = True


obj = AudioManager()
obj.start()

obj.stop()