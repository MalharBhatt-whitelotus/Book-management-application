#!/bin/zsh

# ===== CONFIG =====
PROJECT_DIR="/Users/maulik/malhar /day-14 task/book_management_application"
APP_IMPORT="main:app"
HOST="127.0.0.1"
PORT="8000"
URL="http://${HOST}:${PORT}/"
VENV_PATH="../.venv/bin/activate"
APP_NAME="Google Chrome"

# ===== Close only the local app tabs in Chrome =====
close_local_tabs() {
  osascript <<EOF
tell application "$APP_NAME"
	repeat with w in every window
		set tabIndexesToClose to {}
		
		repeat with i from 1 to (count of tabs of w)
			set currentTab to tab i of w
			if (URL of currentTab starts with "$URL") then
				set end of tabIndexesToClose to i
			end if
		end repeat
		
		repeat with j from (count of tabIndexesToClose) to 1 by -1
			close tab (item j of tabIndexesToClose) of w
		end repeat
	end repeat
end tell
EOF
}

# ===== MOVE TO PROJECT =====
cd "$PROJECT_DIR" || {
  echo "❌ Could not cd into $PROJECT_DIR"
  return 1 2>/dev/null || exit 1
}

# ===== ACTIVATE VENV =====
if [[ -f "$VENV_PATH" ]]; then
  source "$VENV_PATH"
else
  echo "❌ Virtual environment not found at: $PROJECT_DIR/$VENV_PATH"
  return 1 2>/dev/null || exit 1
fi

# ===== START UVICORN IN BACKGROUND =====
python -m uvicorn "$APP_IMPORT" --reload --host "$HOST" --port "$PORT" &
UVICORN_PID=$!

echo "🚀 Starting FastAPI app..."
echo "PID: $UVICORN_PID"

# ===== CLEANUP FUNCTION =====
cleanup() {
  echo ""
  echo "🛑 Stopping FastAPI server..."
  kill "$UVICORN_PID" 2>/dev/null
  wait "$UVICORN_PID" 2>/dev/null
  echo "✅ Server stopped."
  close_local_tabs
  ECHO "Only Local Tabs are closed"
}

trap cleanup INT TERM EXIT

# ===== WAIT FOR SERVER TO START =====
sleep 1

# ===== OPEN BROWSERS =====
open -a "$APP_NAME" "$URL"
open -na "$APP_NAME" --args --incognito "$URL"

echo "🌐 Opened:"
echo "   1) Chrome normal     -> $URL"
echo "   2) Chrome incognito -> $URL"
echo ""
echo "Press Ctrl+C to stop the server."

wait "$UVICORN_PID"