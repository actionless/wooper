#!/bin/sh
coverage run --source=wooper -m unittest -v &&
python -m coverage html
