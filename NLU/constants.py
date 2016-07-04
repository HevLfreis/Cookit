#!/usr/bin/env python
# coding: utf-8
# created by hevlhayt@foxmail.com 
# Date: 2016/6/10 
# Time: 18:22
#
import os

from Cookit.settings import STATICFILES_DIRS

PROJECT_NAME = 'COOKIT'
NLU_COP_TOPIC = {}
NLU_HRL_TOPIC = {}
NLU_PAT_TOPIC = {}
STATIC_FOLDER = STATICFILES_DIRS[0]

TEMP_PATH = os.path.join(STATIC_FOLDER, 'temp')