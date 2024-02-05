#!/bin/sh
if ! screen -list | grep -q "io"; then
  cd /home/os/mcserver/python
  screen -S io -d -m python main.py
fi
