#!/usr/bin/env python
# coding: utf-8
# created by hevlhayt@foxmail.com 
# Date: 2016/6/10 
# Time: 18:22
#
import os
from ctypes import cdll

from Cookit.settings import STATICFILES_DIRS, BASE_DIR

PROJECT_NAME = 'COOKIT'
NLU_COP_TOPIC = {}
NLU_HRL_TOPIC = {}
NLU_PAT_TOPIC = {}
STATIC_FOLDER = STATICFILES_DIRS[0]

TEMP_PATH = os.path.join(STATIC_FOLDER, 'temp')


# HYBRID_DLL = ''
# HYBRID_MODEL_FILE = ''

HYBRID_DLL = cdll.LoadLibrary(os.path.join(BASE_DIR, "static/enlu/libhybrid_nlu.2.0.0.dll"))
HYBRID_MODEL_FILE = os.path.join(BASE_DIR, "static/enlu/model/model_Default")

CRF_DLL = cdll.LoadLibrary(os.path.join(BASE_DIR, "static/enlu/libadv_func_lib.so"))
CRF_MODEL_FILE = os.path.join(BASE_DIR, "static/enlu/tag_ws.dat")

MODEL_DIR = os.path.join(BASE_DIR, 'static/enlu/model')
MODELS = {d.split('_')[1]: os.path.join(MODEL_DIR, d)
          for d in os.listdir(MODEL_DIR)}

# print MODELS

