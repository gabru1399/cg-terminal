import json

tpath = r'C:\Users\SIGMA\.gemini\antigravity\brain\dd17432c-1f2f-4f43-8cac-144e2e2ee49f\.system_generated\logs\transcript.jsonl'
with open(tpath, 'r', encoding='utf-8') as f:
    for i, line in enumerate(f):
        if 125 <= i <= 147:
            obj = json.loads(line)
            calls = obj.get('tool_calls', [])
            for c in calls:
                cmd = c.get('args', {}).get('CommandLine')
                path = c.get('args', {}).get('Path')
                print(f"Step {i}: {c.get('name')}: {cmd or path}")
