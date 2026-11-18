#!/bin/sh
# Web search wrapper: strips SDK banner lines, returns clean JSON to stdout.
# usage: ws.sh "query" [num] [recency_days]
Q="$1"; N="${2:-10}"; R="$3"
if [ -n "$R" ]; then
  ARGS="{\"query\": \"$Q\", \"num\": $N, \"recency_days\": $R}"
else
  ARGS="{\"query\": \"$Q\", \"num\": $N}"
fi
z-ai function -n web_search -a "$ARGS" 2>/dev/null | sed -n '/^\[/,$p'
