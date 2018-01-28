"""
This demo file shows you how to use the new_message_callback to interact with
the recorded audio after a keyword is spoken. It uses the speech recognition
library in order to convert the recorded audio into text.

Information on installing the speech recognition library can be found at:
https://pypi.python.org/pypi/SpeechRecognition/
"""

import snowboydecoder
import sys
import signal
import speech_recognition as sr
import os
import requests
import glob
import logging
import logging.handlers

LOG_FILENAME = 'log-listen.log'

my_logger = logging.getLogger('MyLogger')
my_logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

handler = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=1024*1024*5, backupCount=5)
handler.setFormatter(formatter)

my_logger.addHandler(handler)

interrupted = False

def audioRecorderCallback(data):
    try:
        my_logger.info('Sending audio buffer to remote %s ...' % remote)

        url = "http://%s/sarah/listen" % remote
        payload = { 'buffer' : data }

        response = requests.post(url, data=payload)
    except requests.exceptions.RequestException as e:
        print("unable to contact remote host %s : %s" % (remote, e))

def detectedCallback():
    my_logger.info('Hotword detected ...')
    snowboydecoder.play_audio_file()
    sys.stdout.flush()

def signal_handler(signal, frame):
    global interrupted
    interrupted = True

def interrupt_callback():
    global interrupted
    return interrupted

if len(sys.argv) != 3:
    print("Error: missing parameters")
    print("Usage: python listen.py your.model remote")
    sys.exit(-1)

model = sys.argv[1]
remote = sys.argv[2]

# capture SIGINT signal, e.g., Ctrl+C
signal.signal(signal.SIGINT, signal_handler)

detector = snowboydecoder.HotwordDetector(model, sensitivity=0.4, audio_gain=1.3)
print("Listening... Press Ctrl+C to exit")

# main loop
detector.start(detected_callback=detectedCallback,
               audio_recorder_callback=audioRecorderCallback,
               interrupt_check=interrupt_callback,
               sleep_time=0.01,
               silent_count_threshold=2)

detector.terminate()
