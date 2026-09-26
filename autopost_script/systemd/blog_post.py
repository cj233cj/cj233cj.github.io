# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "flask",
#   "requests",
# ]
# ///

import os
import base64
import requests
from datetime import datetime, timezone
from flask import Flask, request, jsonify

app = Flask(__name__)

GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]
GITHUB_REPO  = os.environ["GITHUB_REPO"]
BRANCH       = os.environ.get("BRANCH", "main")
SECRET       = os.environ["POST_SECRET"]

@app.route("/post", methods=["POST"])
def post():
    if request.headers.get("X-Secret") != SECRET:
        return jsonify({"error": "unauthorized"}), 401

    data = request.get_json(force=True)
    body = data.get("text", "").strip()
    tags = data.get("tags", "")

    if not body:
        return jsonify({"error": "no text"}), 400

    now      = datetime.now(timezone.utc)
    date_str = now.strftime("%Y-%m-%d")
    ts       = now.strftime("%H%M%S")
    filename = f"{date_str}-{ts}.md"
    path     = f"content/timeline/{filename}"

    tag_list = ""
    if tags:
        tag_list = ", ".join(f'"{t.strip()}"' for t in tags.split(","))

    content = f"""---
date: {date_str}
tags: [{tag_list}]
---

{body}
"""

    encoded = base64.b64encode(content.encode()).decode()

    resp = requests.put(
        f"https://api.github.com/repos/{GITHUB_REPO}/contents/{path}",
        headers={
            "Authorization": f"Bearer {GITHUB_TOKEN}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        },
        json={
            "message": f"memo {date_str} {ts}",
            "content": encoded,
            "branch": BRANCH,
        },
    )

    if resp.status_code == 201:
        return jsonify({"ok": True, "file": path}), 201
    else:
        return jsonify({"error": resp.json().get("message", "unknown")}), resp.status_code


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
