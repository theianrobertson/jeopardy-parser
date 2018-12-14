# -*- coding: utf-8 -*-

import os

DEBUG = True

# Assumes the app is located in the same directory
# where this file resides
APP_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(APP_DIR, 'clues.db')

def parent_dir(path):
    '''Return the parent of a directory.'''
    return os.path.abspath(os.path.join(path, os.pardir))

PROJECT_ROOT = parent_dir(APP_DIR)
