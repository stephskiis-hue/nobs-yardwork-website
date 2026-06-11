#!/usr/bin/env python3
"""
SMS bridge for No-BS Yardwork weekly SEO audit.

Sends long messages by splitting at line boundaries into ~1500-char chunks
(each prefixed with [i/N]). Polls inbound replies from your phone since
last processed SID, so Claude can read "GO" / edit prompts on next run.

Usage:
  python _seo-twilio.py send "message text"
  cat file.txt | python _seo-twilio.py send
  python _seo-twilio.py poll            # prints JSON list of new inbounds
  python _seo-twilio.py reply "text"    # alias of send
"""
import os
import sys
import json
from pathlib import Path

try:
    from twilio.rest import Client
except ImportError:
    sys.stderr.write("twilio package missing. Run: pip install twilio\n")
    sys.exit(1)

HERE = Path(__file__).resolve().parent
ENV_FILE = HERE / '_seo-twilio.env'
STATE_FILE = HERE / '_seo-twilio-state.json'
MAX_SMS = 1500  # Twilio hard cap is 1600 per body; leave room for [i/N] prefix


def load_env():
    if not ENV_FILE.exists():
        sys.stderr.write(f"Missing env file: {ENV_FILE}\n")
        sys.stderr.write("Create it with:\n")
        sys.stderr.write("  TWILIO_ACCOUNT_SID=AC...\n")
        sys.stderr.write("  TWILIO_AUTH_TOKEN=...\n")
        sys.stderr.write("  TWILIO_FROM_NUMBER=+1XXXXXXXXXX  (your Twilio number)\n")
        sys.stderr.write("  TWILIO_TO_NUMBER=+12049000438    (your phone)\n")
        sys.exit(1)
    env = {}
    for line in ENV_FILE.read_text(encoding='utf-8').splitlines():
        line = line.strip()
        if line and not line.startswith('#') and '=' in line:
            k, v = line.split('=', 1)
            env[k.strip()] = v.strip().strip('"').strip("'")
    required = ['TWILIO_ACCOUNT_SID', 'TWILIO_AUTH_TOKEN',
                'TWILIO_FROM_NUMBER', 'TWILIO_TO_NUMBER']
    missing = [k for k in required if k not in env or not env[k]]
    if missing:
        sys.stderr.write(f"Missing required env vars: {missing}\n")
        sys.exit(1)
    return env


def get_client():
    env = load_env()
    return Client(env['TWILIO_ACCOUNT_SID'], env['TWILIO_AUTH_TOKEN']), env


def split_message(text, max_len=MAX_SMS):
    """Split at line boundaries; never mid-word. Returns list of chunks."""
    chunks = []
    buf = ""
    for line in text.splitlines(keepends=True):
        if len(line) > max_len:
            # paragraph longer than max — hard split
            if buf:
                chunks.append(buf)
                buf = ""
            for i in range(0, len(line), max_len):
                chunks.append(line[i:i + max_len])
            continue
        if len(buf) + len(line) > max_len:
            chunks.append(buf)
            buf = line
        else:
            buf += line
    if buf:
        chunks.append(buf)
    return chunks or [""]


def send(message):
    client, env = get_client()
    chunks = split_message(message)
    total = len(chunks)
    sent = []
    for i, chunk in enumerate(chunks, 1):
        prefix = f"[{i}/{total}]\n" if total > 1 else ""
        msg = client.messages.create(
            from_=env['TWILIO_FROM_NUMBER'],
            to=env['TWILIO_TO_NUMBER'],
            body=prefix + chunk,
        )
        sent.append(msg.sid)
    return sent


def load_state():
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text(encoding='utf-8'))
        except Exception:
            pass
    return {}


def save_state(state):
    STATE_FILE.write_text(json.dumps(state, indent=2), encoding='utf-8')


def poll():
    """Return inbound messages from user's phone since last processed SID."""
    client, env = get_client()
    state = load_state()
    last_sid = state.get('last_processed_sid')

    msgs = client.messages.list(
        from_=env['TWILIO_TO_NUMBER'],
        to=env['TWILIO_FROM_NUMBER'],
        limit=20,
    )

    new_msgs = []
    for m in msgs:
        if m.sid == last_sid:
            break
        new_msgs.append({
            'sid': m.sid,
            'body': m.body,
            'date_sent': m.date_sent.isoformat() if m.date_sent else None,
            'from': m.from_,
        })

    new_msgs.reverse()

    if new_msgs:
        state['last_processed_sid'] = new_msgs[-1]['sid']
        state['last_poll'] = new_msgs[-1]['date_sent']
        save_state(state)

    return new_msgs


def main():
    if len(sys.argv) < 2:
        sys.stderr.write(__doc__)
        sys.exit(1)

    cmd = sys.argv[1].lower()

    if cmd in ('send', 'reply'):
        if len(sys.argv) >= 3:
            body = ' '.join(sys.argv[2:])
        else:
            body = sys.stdin.read()
        if not body.strip():
            sys.stderr.write("Empty message — nothing sent.\n")
            sys.exit(1)
        sids = send(body)
        print(json.dumps({'sent_count': len(sids), 'sids': sids}))

    elif cmd == 'poll':
        msgs = poll()
        print(json.dumps(msgs, indent=2, ensure_ascii=False))

    else:
        sys.stderr.write(f"Unknown command: {cmd}\n")
        sys.stderr.write(__doc__)
        sys.exit(1)


if __name__ == '__main__':
    main()
