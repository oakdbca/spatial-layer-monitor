#!/bin/bash

# Start the first process
# env > /etc/.cronenv
# sed -i 's/\"/\\"/g' /etc/.cronenv
cat /dev/urandom | tr -dc 'a-f0-9' | fold -w 32 | head -n 1 > /app/git_hash

if [ $ENABLE_CRON == "True" ];
then
echo "Starting Python Cron"
python /bin/scheduler.py /app/python-cron /app/logs/python-cron.log &
status=$?
if [ $status -ne 0 ]; then
  echo "Failed to start cron: $status"
  exit $status
fi

fi

echo "System Started"
/bin/bash
