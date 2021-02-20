#!/bin/bash

tmux new-session -d bash
tmux split-window -h bash
tmux send -t 0:1.1 "python3 ./server.py" C-m
tmux send -t 0:1.2 "python3 ./worker.py" C-m
tmux -2 attach-session -d