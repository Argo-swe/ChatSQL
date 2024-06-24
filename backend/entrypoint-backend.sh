#!/bin/sh
# if a command is not provided, set a default command
if [ $# -eq 0 ]; then
  set -- fastapi dev app.py --host 0.0.0.0
fi
echo "$PWD"
# update to new requirements on each container start
pip --no-cache-dir install --upgrade -r ../requirements.txt
# use exec to replace pid 1 with the command (e.g. python app.py)
exec "$@"
