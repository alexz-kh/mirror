#!/bin/python

# -*- coding: utf-8 -*-\

#import time, pyaudio, wave, os, urllib,urllib2,pycurl,httplib,sys,string
import logging
from ctypes import *
import pyaudio
import pprint

import speech_recognition as sr

"""
https://pythonspot.com/en/speech-recognition-using-google-speech-api/
https://www.youtube.com/watch?v=lp8132pU5Og
https://stackoverflow.com/questions/25394329/python-voice-recognition-library-always-listen
https://github.com/aikikode/uspeak
"""
"""
Disable log: https://stackoverflow.com/questions/7088672/pyaudio-working-but-spits-out-error-messages-each-time
"""



#mirror_name = "vika"
mirror_name = "test"
mirror_lang = 'ru_RU'
#mirror_lang = 'en_US'



def capture():
    print('1')


def get_value(audio):
    # Speech recognition using Google Speech Recognition
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio,
        # key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        answer = r.recognize_google(audio, language=mirror_lang,
                                    show_all=True)
        LOG.debug("You said:{}".format(pp.pformat(answer)))
    except sr.UnknownValueError:
        LOG.error("Google Speech Recognition could not understand audio")
        return False
    except sr.RequestError as e:
        LOG.error(
            "Could not request results from Google Speech"
            " Recognition service; {0}".format(e))
        return False
    return answer


def disable_c_messages():

    # From alsa-lib Git 3fd4ab9be0db7c7430ebd258f2717a976381715d
    # $ grep -rn snd_lib_error_handler_t
    # include/error.h:59:typedef void (*snd_lib_error_handler_t)(const char *file, int line, const char *function, int err, const char *fmt, ...) /* __attribute__ ((format (printf, 5, 6))) */;
    # Define our error handler type

    error_handler_func = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int,
                                   c_char_p)

    def py_error_handler(filename, line, function, err, fmt):
        pass

    c_error_handler = error_handler_func(py_error_handler)

    asound = cdll.LoadLibrary('libasound.so')
    # Set error handler
    asound.snd_lib_error_set_handler(c_error_handler)
    # Initialize PyAudio
    p = pyaudio.PyAudio()
    # p.terminate()


if __name__ == '__main__':
    LOG = logging.getLogger(__name__)
    LOG.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    LOG.addHandler(ch)

    disable_c_messages()
    pp = pprint.PrettyPrinter(indent=4)

    # Record Audio
    r = sr.Recognizer()
    i = 0
    while True:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source) # listen for 1 second to calibrate the energy threshold for ambient noise levels
            LOG.debug("Say something!")
            audio = r.listen(source)
            LOG.debug("Captured!")
        result = get_value(audio)
        #import ipdb; ipdb.set_trace()
        if mirror_name in result:
            LOG.debug('Master call me!')

        i = i+1
        print i





