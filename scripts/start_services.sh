#!/bin/bash
set -eu

python scripts/wait_for_db.py

uvicorn app.main:app --host 0.0.0.0 --port 8000 &
UVICORN_PID=$!

python app/gradio_ui/interface.py &
GRADIO_PID=$!

shutdown() {
  kill "$UVICORN_PID" "$GRADIO_PID" 2>/dev/null || true
}

trap shutdown INT TERM

wait -n "$UVICORN_PID" "$GRADIO_PID"
shutdown
wait || true
