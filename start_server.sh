#!/bin/bash
# Simple local server for previewing the Cortex app

PORT=8000

echo "🚀 Starting Cortex Preview Server..."
echo "📱 Open your browser to: http://localhost:$PORT"
echo "💡 Tip: Open DevTools and switch to 'iPhone 12 Mini' responsive mode"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python3 -m http.server $PORT
