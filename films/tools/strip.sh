#!/usr/bin/env bash
# Contact strip of a clip for review: 6 frames across, lifted a little so dark
# shots are readable. Usage: films/tools/strip.sh clip.mp4 out.jpg
set -euo pipefail
in="$1"; out="$2"
n=$(ffprobe -v error -select_streams v:0 -count_packets -show_entries stream=nb_read_packets -of csv=p=0 "$in")
last=$((n - 1))
sel=""
for k in 0 1 2 3 4 5; do sel="${sel:+$sel+}eq(n\\,$((last * k / 5)))"; done
ffmpeg -loglevel error -y -i "$in" -vf "select='$sel',scale=250:-1,eq=brightness=0.08:contrast=1.2,tile=6x1" -frames:v 1 "$out"
