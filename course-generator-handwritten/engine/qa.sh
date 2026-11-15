#!/bin/bash
# qa.sh <L> : render end-of-beat stills for every beat, tile into qa sheets
L=$1; rm -rf $L/stills; mkdir -p $L/stills $L/qa
python3 - $L <<'P' > /tmp/claude-0/qa_$L.txt
import json,sys,collections
L=sys.argv[1]; d=collections.OrderedDict()
for sc,b,*_ in json.load(open(f'{L}/beats.json')): d.setdefault(sc,[]).append(b)
for sc,bs in d.items(): print(sc,' '.join(f'{b}:e' for b in bs))
P
while read sc specs; do node render.js $L still $sc $specs 2>&1 | grep -E "PAGEERR|WORDMISS|Error" ; done < /tmp/claude-0/qa_$L.txt
ls $L/stills/*.jpg | sort -V > /tmp/claude-0/qa_list_$L.txt
n=0; i=0; args=(); for f in $(cat /tmp/claude-0/qa_list_$L.txt); do args+=(-i $f); n=$((n+1)); if [ $n = 6 ]; then ffmpeg -v error -y "${args[@]}" -filter_complex "xstack=inputs=6:layout=0_0|w0_0|0_h0|w0_h0|0_h0+h0|w0_h0+h0,scale=1600:-1" $L/qa/sheet$i.jpg; args=(); n=0; i=$((i+1)); fi; done
if [ $n -gt 0 ]; then while [ $n -lt 6 ]; do args+=(-f lavfi -i color=black:s=1920x1080:d=1); n=$((n+1)); done; ffmpeg -v error -y "${args[@]}" -filter_complex "xstack=inputs=6:layout=0_0|w0_0|0_h0|w0_h0|0_h0+h0|w0_h0+h0,scale=1600:-1" -frames:v 1 $L/qa/sheet$i.jpg; fi
ls $L/qa
