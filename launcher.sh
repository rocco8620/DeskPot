#!/bin/bash
BASE="`dirname "${0}"`"


source "${BASE}/env/bin/activate"
python3 "${BASE}/DeskPot.py" --no-wait

