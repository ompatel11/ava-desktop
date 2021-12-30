FROM python
RUN mkdir ava-desktop && cd ava-desktop
COPY ava_desktop_ui ./ava_desktop_ui
RUN python3 -m pip install -r /ava_desktop_ui/requirements.txt
CMD python3 main.py

