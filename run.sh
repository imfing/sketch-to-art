#!/bin/bash

# Set host to 0.0.0.0 instead of localhost
export HOST=0.0.0.0

# Run server in the background
(cd server && python3 app_stylize.py) &
(cd server && python3 app_pix.py) &

# Run front-end
yarn dev