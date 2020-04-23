#!/bin/sh
set -e

eval "$(pyenv init -)"
exec "$@"
