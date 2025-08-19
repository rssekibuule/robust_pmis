#!/usr/bin/env bash
# Kill only the process listening on the given port (default 8069) without touching other odoo-bin processes.
# Usage: ./scripts/kill_port_8069.sh [port]
set -euo pipefail
PORT=${1:-8069}
PIDS=$(lsof -t -i:"${PORT}" -sTCP:LISTEN 2>/dev/null || true)
if [ -z "${PIDS}" ]; then
  echo "No process listening on port ${PORT}."
  exit 0
fi
echo "Found PID(s) ${PIDS} listening on port ${PORT}. Sending SIGTERM..."
kill ${PIDS} || true
# Wait briefly then force kill if still alive
sleep 1
for pid in ${PIDS}; do
  if kill -0 $pid 2>/dev/null; then
    echo "PID $pid still alive; sending SIGKILL."
    kill -9 $pid || true
  fi
done
# Final verification
if lsof -t -i:"${PORT}" -sTCP:LISTEN >/dev/null 2>&1; then
  echo "WARNING: A process is still listening on port ${PORT}."
  exit 1
fi
echo "Port ${PORT} is now free."
