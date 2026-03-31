import json

def parse_fingerprint(raw):

    try:
        return json.loads(raw)
    except:
        return None
