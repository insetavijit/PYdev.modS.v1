#!/bin/bash
micromamba activate modS.v1
python -m debugpy --listen 5678 --wait-for-client "$1"
