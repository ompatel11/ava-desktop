FROM python
RUN mkdir ava-desktop && cd ava-desktop
COPY ava_desktop_ui ./ava_desktop_ui
RUN apt-get update && apt-get install -y python3-opencv
RUN pip3 install opencv-python
RUN pip3 install -r /ava_desktop_ui/requirements.txt
RUN pip3 install Pyrebase
CMD python3 /ava_desktop_ui/main.py