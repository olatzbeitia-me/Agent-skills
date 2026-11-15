#!/bin/bash
# render_lecture.sh <L> <label> : renders scenes in 2 lanes, muxes to out/<label>.mp4
L=$1; LABEL="$2"; mkdir -p out
SC=($(python3 -c "import json;print(' '.join(dict.fromkeys(r[0] for r in json.load(open('$L/beats.json')))))"))
a=(); b=(); for i in "${!SC[@]}"; do if [ $((i%2)) = 0 ]; then a+=(${SC[$i]}); else b+=(${SC[$i]}); fi; done
rm -f $L/parts/*.mp4
(for s in "${a[@]}"; do node render.js $L video $s; done) > $L/log_a.txt 2>&1 &
(for s in "${b[@]}"; do node render.js $L video $s; done) > $L/log_b.txt 2>&1 &
wait
~/.explainer-video/venv/bin/python mux.py $L "out/$LABEL.mp4"
