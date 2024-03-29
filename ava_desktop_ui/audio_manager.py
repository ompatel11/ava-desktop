from __future__ import division
import re
import sys
import threading
import time
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from google.cloud import speech
import pyaudio
from six.moves import queue
import pyautogui
import platform as _platform
import yaml
from yaml.loader import SafeLoader

from Models import user
from Models.TaskRunner import RunTask

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
# credential_path = "ava-daemon-4ce53760f667.json"
# os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path


class ThreadWithResult(threading.Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs={}, *, daemon=None):
        def function():
            self.result = target(*args, **kwargs)
        super().__init__(group=group, target=function, name=name, daemon=daemon)


class TranscriptModifier(object):
    """Modifies the transcript according to the type of file detected"""

    def __init__(self, transcript, extension):
        """Check the currently working file type in the __init__()"""
        self.transcript = transcript
        self.languages = ["html", "py", "js", "css", "cpp"]
        self.extension = extension

        commands = self.fetch_commands(self.extension)
        # t1 = threading.Thread(target=self.modify_continuous_speech(commands))

    def startTrasnscription(self):
        thread1 = ThreadWithResult(target=self.executetasks)
        thread1.start()
        thread1.join()
        print(thread1.result)
        return thread1.result

    def fetch_commands(self, ext):
        # Open the file and load the file
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

    def executetasks(self):
        print("Tasks= ", user.current_user.task_list)
        for item in user.current_user.task_list:
            print(item['name'].casefold())
            # str(self.transcript).casefold()
            if str(self.transcript).casefold() == str(item['name']).casefold():
                print("Match found")
                runTaskObject = RunTask(item['name'])
                print("Running Task")
                runTaskObject.enumerateData()
                return True
            else:
                return False

    def modify_continuous_speech(self, commands):

        self.transcript = self.transcript.lower()
        words = self.transcript.split(' ')
        print("Transcript= " + self.transcript)

        skipNxtItr = False
        for i, val in enumerate(words):
            if skipNxtItr:
                skipNxtItr = False
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
                            self.moveUp(commands[val][1]["direction"][j + 1])
                            continue
                        if commands[val][1]['direction'][j] == "down":
                            # Down def ():
                            self.moveDown(commands[val][1]["direction"][j + 1])
                            continue
                        if commands[val][1]['direction'][j] == "left":
                            # Left
                            self.moveLeft(int(commands[val][1]["direction"][j + 1]))

                            if commands[val][1]['direction'][j] == "right":
                                # Right
                                self.moveRight(commands[val][1]["direction"][j + 1])
                                continue
                continue
            except Exception as e:
                print(e)
                simulatekeys(val)
                continue

    def moveLeft(self, index):
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
        self.THRESHOLD = 300
        self._rate = rate
        self.chunk_size = chunk_size
        self.SILENT_CHUNKS = 3 * self._rate / self.chunk_size
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
        print("In Exit")
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
            silent_chunks = 0

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
            silent = self.is_silent(chunk)

            self.audio_input.append(chunk)
            if chunk is None:
                return
            data.append(chunk)
            # Now consume whatever other data's still buffered.
            while True:
                try:
                    chunk = self._buff.get(block=False)
                    if silent:
                        silent_chunks += 1
                        if silent_chunks > self.SILENT_CHUNKS:
                            print("Silence detected")
                            break
                    if chunk is None:
                        return
                    data.append(chunk)
                    self.audio_input.append(chunk)

                except queue.Empty:
                    break

            yield b"".join(data)

    def is_silent(self, chunk):
        """Returns 'True' if below the 'silent' threshold"""
        return max(chunk) < 0


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

    while True:
        if _platform.system() == 'Windows':
            time.sleep(2)
            window = win32gui.GetForegroundWindow()
            print(win32gui.GetForegroundWindow())
            # Select the Editor and will wait till that Application is in foreground
            active_window_name = win32gui.GetWindowText(window)
            print("Window Name = " + active_window_name)
            if active_window_name != 'main':
                break
    return True if active_window_name != 'main' else False


class AudioManager:
    """"
    It is a class that manages the audio stream, start and pause.
    Provides a control from the user interface
    """

    # noinspection PyTypeChecker
    def __init__(self, main_obj):
        self._mainObject = main_obj

        cred = {
            "type": "service_account",
            "project_id": "ava-daemon",
            "private_key_id": "4ce53760f66722d399600fe21a614b2794ea25b6",
            "private_key": "-----BEGIN PRIVATE "
                           "KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC4WWZLLFJXVLaF"
                           "\nxLbb8wB9mCH9EPIzcvpBiCOU9gzE13bVdq1XBBmiKwHksMEhdEOHSKVMk4Az7NFI"
                           "\nqpZKDp6sSYkIVvn8r4Pkcts5jaraHlxmIJwEvZsSFhM25kYL8VPC35Gb6fH3ZNJY\ntxe"
                           "/QrAN87PKnqlItcw1n0ignvSNmPNCasR69W1uW3G1/hHcxmn8qOBcMfRLo3qp"
                           "\nHHsLQqPGPdovJUGpsItXiYyCKzyZcWctWt86N3ZiSH5khGTqLEGa7zf6/cAy8xs6\nNk00x5RsyKDsWuYGv3"
                           "/GjBFXuL1hZkMvQeFqH3qSNJYmAx5JpbkwqaMeJGDPtQzw"
                           "\nnILfTi3jAgMBAAECggEAFP1o3kpPnc3xck2xnF2QwrwdspjJWv5ObEO5+W4Cii8W"
                           "\nQrvehLfcy1AmSQmvE8YPIkotOAjbYg4mziVOM2RywJ8m0SJGGHVLiSliuKzetTMb"
                           "\nxi0UVp3YGDkXOvsBIr75kIiwJZZ/jHGYWa2PMKHBNfV3lSx3jeXVOI3IUTGIGs8L\n0wDx/0Jq"
                           "/IzLAleD0TuX3v1njxtP3UrPA3w9z35oonw7gFz8WIq1g0VOlTgMRFq7\n3WolvClDBGNfV81hb"
                           "/vHq6kmO69dBKq4ZDmWokXM/cfEpMTjEH4Zxi3dInORAmH0\n4TqJU4RXDVlsdLRB"
                           "/qHCKzzVsx8Awci8g1oTarhwEQKBgQDrPXdpWU72MaiWzJbs\nEy10rUaFQI2UAl76d6+qX7/F2i1y0wlCg/SJPC"
                           "/9lG/tpMppeF89aRz4bwZFrkIe\ninRrcrCHw/4UDuglDW7bNi3iwaRizQn4j5FUq4lOT3N+1udNAN5"
                           "/6ll8ds74TFZp\nXsTQLXl0vmdW06zysbUElZlCZQKBgQDInjVlsOcXjjhTOOivm6Vofldb2F7ElGCN"
                           "\nszNFmQvioDcr2ctIK1MYVqxP7DNVHf4OGcblmN/JTP4qVM0+tf4/KALKq9zcYCht"
                           "\n8W2rFh7DLfaH7tJolLaQggNnJZ0FP/KaIPW3VXMn1c5ClsBOciA2t+JFkS9sWbUj"
                           "\nOy3L7peGpwKBgBfqlORiDxQasmA6hrGTtZBiOYQ8rug4YX2ng3WX7IBqESrWZ9+a"
                           "\nWNdHBj4KxGJt2aJleZFdyXM8nm+hKtm+C94MuAPlmkRhy5pQxk+FL58ZPuRIolXi"
                           "\nCs2H7xrGGyDvKm76wqRQqC5uSdaWtEZcOzhLF0kWPp1mQfQeux+vMfi9AoGAd9TY\nfFeAkbdnuX4irtI"
                           "/qPzeXYQOh0lBqyJBG+9hBAtDKTQ8km0eg0kyP8MMnmj92ZpY\nDciU037jypFAz5aRuVPC5yBlGlVtkM5G"
                           "/YyG73rC6Usj70f1DLg8JB55fitGU/4g\nB1RJJqA1Rd0aHUFaMJUB2R/xvbyPz"
                           "+2HW2q2o70CgYEAwKUlTanxB8yDej92OwCi"
                           "\nRNhKaK0bBlRZpdJLz80bBLbI31Ffziib9NPdnUHnxRnf4tkghzC2pIWtsfErEnZS"
                           "\nh0HXlvZ1ucXA42t0KyrMlieZMUbjUIH2tEt9WHXgnBY+kM+6dqPoMzQjRbZREpxU"
                           "\nRHosnXBXmgpHDJYzT2Yy7Hc=\n-----END PRIVATE KEY-----\n",
            "client_email": "ava-desktop-demo@ava-daemon.iam.gserviceaccount.com",
            "client_id": "116614411031984579551",
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/ava-desktop-demo%40ava-daemon"
                                    ".iam.gserviceaccount.com "
        }

        self.language_code = "en-US"  # a BCP-47 language tag
        self.client = speech.SpeechClient.from_service_account_info(cred)
        self.config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=SAMPLE_RATE,
            language_code=self.language_code,
            enable_automatic_punctuation=False,
        )

        self.streaming_config = speech.StreamingRecognitionConfig(
            config=self.config, interim_results=True,
        )
        self.mic_manager = None
        self.isClosed = False

    def stop(self):
        if self._mainObject is not None:
            self._mainObject.ui.btnMicrophoneControl.setIconSize(QSize(32, 32))
            self._mainObject.ui.btnMicrophoneControl.setIcon(QIcon("Icons/Icon ionic-ios-mic.png"))
            self._mainObject.ui.btnMicrophoneControl.setStyleSheet("""
                                    background-color: rgb(62, 60, 84);
                                    border: 1px solid white;
                                    border-radius: 40;
                                    """)
        self.mic_manager.setExit()
        self.isClosed = True

    # noinspection PyTypeChecker
    def start(self):
        self.mic_manager = ResumableMicrophoneStream(SAMPLE_RATE, CHUNK_SIZE)
        try:
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
                        print("Speech API called")
                        # Now, put the transcription responses to use.
                        self.listen_print_loop(responses, stream, "cpp")

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
        except Exception as e:

            self.stop()
            print(e)

    def listen_print_loop(self, responses, stream, extension):
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
            if self._mainObject is not None:
                self._mainObject.ui.lblLiveTranscript.setText(transcript)
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
                modify_transcript = TranscriptModifier(transcript, extension)
                if not modify_transcript.startTrasnscription():
                    self.stop()

                # Exit recognition if any of the transcribed phrases could be
                # one of our keywords.
                if re.search(r"\b(exit|quit|stop)\b", transcript, re.I):
                    self.stop()

            else:
                sys.stdout.write(RED)
                sys.stdout.write("\033[K")
                sys.stdout.write(str(corrected_time) + ": " + transcript + "\r")

                stream.last_transcript_was_final = False


# obj = AudioManager(None)
# obj.start()