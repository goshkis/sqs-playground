#!/bin/bash

SESS=egorsqs

tmux new-session -d -s $SESS
BASE=$(tmux display-message -p "#{base-index}")
BASEP=$(tmux display-message -p "#{pane-base-index}")
tmux split-window -h
tmux split-window -h
tmux select-layout even-horizontal
tmux send -t $SESS:$BASE.$BASEP "python3 ./server.py" C-m
tmux send -t $SESS:$BASE.$(($BASEP+1)) "python3 ./worker.py" C-m
# client will start with 5s delay to allow service to start
tmux send -t $SESS:$BASE.$(($BASEP+2)) "sleep 5;python3 ./client.py" C-m
tmux -2 attach-session -d -t egorsqs
