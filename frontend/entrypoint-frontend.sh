#!/bin/sh
# if a command is not provided, set a default command
if [ $# -eq 0 ]; then
  set -- npm run dev
fi
echo "$PWD"
# update to new packages on each container start
npm i
# use exec to replace pid 1 with the command
exec "$@"
