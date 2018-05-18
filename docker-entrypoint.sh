#!/bin/bash

set -e

case "$1" in
  ui_test)
    exec pipenv run pytest --driver=Firefox --base-url=http://redash:5000 --verify-base-url --variables=variables.json --html=report.html
    ;;
  *)
    exec "$@"
    ;;
esac
