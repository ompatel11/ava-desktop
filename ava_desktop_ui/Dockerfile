FROM python
COPY audio_manager.py ./
COPY main.py ./
COPY widgets/ ./widgets
COPY application ./application
COPY Icons ./Icons
COPY requirements.txt ./
COPY programming_commands.yaml ./
RUN apt-get update
RUN apt-get install libasound-dev libportaudio2 libportaudiocpp0 portaudio19-dev -y
RUN pip install pyaudio
RUN pip install -r ./requirements.txt
CMD ["python", "main.py"]


