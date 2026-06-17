#!/bin/bash
# Dubbelklik om de Skyline Digital site lokaal te starten.
# Houd dit venster open tijdens het bekijken/opnemen. Ctrl+C om te stoppen.

cd "$(dirname "$0")" || exit 1
PORT=8097
NAME="Skyline Digital"

lsof -nP -iTCP:$PORT -sTCP:LISTEN -t 2>/dev/null | xargs kill -9 2>/dev/null
URL="http://localhost:$PORT"
echo ""
echo "  $NAME — lokale server"
echo "  Open in je browser:  $URL"
echo "  Houd dit venster open. Ctrl+C om te stoppen."
echo ""
( sleep 1 && open "$URL" ) &
python3 -m http.server $PORT
