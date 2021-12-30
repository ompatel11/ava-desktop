FROM python
RUN mkdir ava-desktop && cd ava-desktop
COPY ava_desktop_ui ./ava_desktop_ui
RUN pip3 install -r /ava_desktop_ui/requirements.txt
CMD python3 /ava_desktop_ui/main.py

python3 -m pip install win32gui