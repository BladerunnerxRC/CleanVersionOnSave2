import requests, json, os
from settings import load_settings

def sync_latest_rename():
    cfg = load_settings()
    api_key = cfg.get('apiKey')        # store API key in config.json
    endpoint = cfg.get('apiEndpoint')
    history = os.path.join(os.path.dirname(__file__), '..', 'data', 'rename_history.json')

    try:
        with open(history) as f:
            last = json.loads(f.readlines()[-1])
        headers = {'Authorization': f'Bearer {api_key}'}
        requests.post(endpoint, json=last, headers=headers, timeout=10)
    except Exception as e:
        print(f"[Integration Error] {e}")
