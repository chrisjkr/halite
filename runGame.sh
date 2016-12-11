#!/bin/bash

if hash python3 2>/dev/null; then
    ./halite -d "30 30" "python3 v2.py" "python3 ambiturner.py"
else
    ./halite -d "30 30" "python v2.py" "python ambiturner.py"
fi
