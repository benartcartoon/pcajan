"""Restricted remote Colab controller. Requires GitHub CLI (`gh auth login`).
Uses private benartcartoon/kontrol issues. Never executes arbitrary commands.
"""
import json
import os
import subprocess
import time
import webbrowser
from pathlib import Path

REPO = 'benartcartoon/kontrol'
STATE = Path.home() / 'AI-Agent' / 'github_issue_state.json'
COLAB = 'https://colab.research.google.com/drive/1A6EpaD0g5W9_ammkd6QqxyKF5LCz2Bc9'
ACTIONS = {'COLAB_OPEN', 'COLAB_CLOSE'}


def gh(*args):
    result = subprocess.run(['gh', *args], capture_output=True, text=True, timeout=35)
    if result.returncode:
        raise RuntimeError(result.stderr.strip() or 'GitHub CLI failed')
    return result.stdout


def log(message):
    print(message, flush=True)
    root = Path.home() / 'AI-Agent' / 'logs'
    root.mkdir(parents=True, exist_ok=True)
    with (root / 'remote_agent.log').open('a', encoding='utf-8') as f:
        f.write(message + '\n')


def open_colab():
    webbrowser.open(COLAB, new=2)
    log('Colab URL sent to browser; actual tab loading not verified.')


def close_colab():
    # Safe failure: never send keystrokes to an unverified browser tab.
    # Runtime deletion requires browser integration and explicit verification.
    raise RuntimeError('Safe close unavailable: Colab tab/runtime cannot be verified. No keys sent.')


def main():
    STATE.parent.mkdir(parents=True, exist_ok=True)
    # On first run, do not execute existing issues created before installation.
    if not STATE.exists():
        current = json.loads(gh('api', f'repos/{REPO}/issues?state=open&per_page=100'))
        STATE.write_text(json.dumps([x['number'] for x in current if 'pull_request' not in x]), encoding='utf-8')
    seen = set(json.loads(STATE.read_text(encoding='utf-8')))
    log('Remote controller started; allowed: COLAB_OPEN. Close fails safely.')
    while True:
        try:
            issues = json.loads(gh('api', f'repos/{REPO}/issues?state=open&per_page=100'))
            for issue in sorted(issues, key=lambda x: x['number']):
                if 'pull_request' in issue or issue['number'] in seen:
                    continue
                number = issue['number']
                title = issue['title'].strip().upper()
                seen.add(number)
                STATE.write_text(json.dumps(sorted(seen)), encoding='utf-8')
                if title not in ACTIONS:
                    log(f'Ignored unsupported issue #{number}: {title}')
                    continue
                try:
                    if title == 'COLAB_OPEN':
                        open_colab()
                    else:
                        close_colab()
                    gh('issue', 'comment', str(number), '-R', REPO, '-b', 'DONE: Open request sent to browser; page load not verified.')
                except Exception as exc:
                    log(f'Issue #{number}: {exc}')
                    gh('issue', 'comment', str(number), '-R', REPO, '-b', f'ERROR: {exc}')
                gh('issue', 'close', str(number), '-R', REPO)
        except Exception as exc:
            log(f'Polling error: {exc}')
        time.sleep(15)


if __name__ == '__main__':
    main()
