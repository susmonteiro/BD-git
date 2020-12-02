#!/usr/bin/python3
import sys
from wsgiref.handlers import CGIHandler
from app import app

CGIHandler().run(app)
