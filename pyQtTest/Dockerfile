FROM python
COPY audio_manager.py ./
COPY ava-daemon-4ce53760f667.json ./
RUN apt-get update
RUN apt-get install libasound-dev libportaudio2 libportaudiocpp0 portaudio19-dev -y
COPY requirements.txt ./
COPY programming_commands.yaml ./
RUN pip install --trusted-host pypi.python.org -r requirements.txt
CMD ["python", "main.py"]
