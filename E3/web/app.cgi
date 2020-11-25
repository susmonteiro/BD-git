#!/usr/bin/python3
import sys
sys.path.insert(0, '/afs/.ist.utl.pt/users/5/6/ist192456/.local/lib/python2.7/site-packages')
from wsgiref.handlers import CGIHandler
from app import app

CGIHandler().run(app)