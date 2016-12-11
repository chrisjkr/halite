#!/bin/bash

if hash python3 2>/dev/null; then
    ./halite -d "30 30" "python3 v4.py" "python3 v3.py" "python3 ambiturner.py"
else
    ./halite -d "30 30" "python v4.py" "python v3.py" "python ambiturner.py"
fi
