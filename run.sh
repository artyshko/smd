#!/bin/bash
python3 GUI/spotify.py 2>/dev/null
python3 GUI/qtw.py 2>/dev/null & python3 GUI/backend.py 2>/dev/null
