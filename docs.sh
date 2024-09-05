#!/bin/sh
exec sphinx-build -b html ./docs-source/ ./docs/ "$@"
