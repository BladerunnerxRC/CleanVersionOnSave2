import time, re

SEMVER_PATTERN = r'^(\d+)\.(\d+)\.(\d+)$'

def bump_version(current, part='patch'):
    major, minor, patch = map(int, current.split('.'))
    if part == 'major':
        major += 1; minor = 0; patch = 0
    elif part == 'minor':
        minor += 1; patch = 0
    else:
        patch += 1
    return f"{major}.{minor}.{patch}"

def append_timestamp(name):
    ts = time.strftime('%Y%m%d-%H%M%S')
    return re.sub(r'\.([^.]+)$', f'-{ts}.\\1', name)
