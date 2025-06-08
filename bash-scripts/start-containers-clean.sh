#!/bin/bash

# Check if at least one port is provided
if [ $# -eq 0 ]; then
  echo "Usage: $0 port1 [port2 ...]"
  exit 1
fi

echo "🔍 Checking for processes using ports: $@"

for PORT in "$@"; do
  PIDS=$(sudo lsof -ti :$PORT)
  if [ -n "$PIDS" ]; then
    echo "⚠️  Port $PORT is in use by PID(s): $PIDS"
    echo "🔪 Killing processes on port $PORT..."
    sudo kill -9 $PIDS
  else
    echo "✅ Port $PORT is free."
  fi
done

echo "✅ Done!"
