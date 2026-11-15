#!/bin/bash
# build.sh <LectureDir>: extract narration, voice it, build scenes.js
# Requires env: TTS_API_KEY, TTS_MODEL, TTS_VOICE (optional TTS_URL, ATEMPO=1.05, PAR=6). Put them in .env (gitignored).
set -e; cd "$(dirname "$0")"; [ -f .env ] && set -a && . ./.env && set +a
L=$1; mkdir -p $L/audio; node extract.js $L
ATEMPO=${ATEMPO:-1.05} PAR=${PAR:-6} python3 tts.py $L | grep -v "^retry" | tail -1
python3 - $L <<'P'
import json,sys
L=sys.argv[1]; b=json.load(open(f'{L}/beats.json'))
open(f'{L}/scenes.js','w').write('const TEXTS='+json.dumps({r[1]:r[2] for r in b})+';\n'+open(f'{L}/spec.js').read())
P
