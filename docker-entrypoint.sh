#!/bin/bash

set -e

case "$1" in
  ui_test)
    exec pipenv run pytest
    ;;
  *)
    exec "$@"
    ;;
esac
