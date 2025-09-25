#!/bin/bash
echo "🧪 Testing HTTP proxy access (after DNS setup)..."
echo "Testing: http://mcp.ziksaka.com/mcp"
echo ""

curl -H "Authorization: Bearer 4cbe3249a0c9b034b141e7f5564935118f39008fe95efc52c646af2946ab3e55" \
     -H "Content-Type: application/json" \
     -X POST http://mcp.ziksaka.com/mcp \
     -d '{"jsonrpc":"2.0","method":"ping","id":1}' \
     --max-time 10 \
     --fail \
     --silent \
     --show-error

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ HTTP proxy working! Now you can add SSL certificate."
else
    echo ""
    echo "❌ HTTP proxy not working. Check:"
    echo "   1. DNS record added?"
    echo "   2. Nginx proxy host configured?"
    echo "   3. Domain propagated? (try: nslookup mcp.ziksaka.com)"
fi
