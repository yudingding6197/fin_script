#!/usr/bin/env python
# -*- coding:gbk -*-

import win32com.client as win

speak = win.Dispatch("SAPI.SpVoice")
speak.Speak("come on")
speak.Speak("���������")
#print("Hello")