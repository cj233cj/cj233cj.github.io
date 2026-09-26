# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "textual>=0.60",
#   "requests",
# ]
# ///
"""
timeline_post_tui.py

A terminal UI for posting entries to the timeline-post Flask server
(the one with the /post endpoint, GITHUB_TOKEN/GITHUB_REPO/POST_SECRET env vars).

Run:
    uv run timeline_post_tui.py

First run asks for the server URL and shared secret, then remembers them
in timeline_post_config.json next to this script (chmod 600).

Keybindings:
    ctrl+s       post the entry
    ctrl+enter   post (from inside the body — needs a terminal that supports
                 the extended keyboard protocol; falls back to a plain
                 newline if your terminal doesn't distinguish it from Enter)
    enter        post (from the tags field)
    ctrl+r       edit server settings
    ctrl+l       list local copies
    ctrl+q       quit
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import requests
from textual import work
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Vertical, Horizontal, VerticalScroll
from textual.screen import ModalScreen
from textual.widgets import (
    Header, Footer, TextArea, Input, Button, Static, Label, ListView, ListItem,
)

APP_DIR = Path(__file__).resolve().parent
CONFIG_PATH = APP_DIR / "timeline_post_config.json"
LOCAL_POSTS_DIR = APP_DIR / "local_posts"
DRAFT_PATH = APP_DIR / "timeline_post_draft.md"
DRAFT_SAVE_DELAY = 0.6  # seconds of typing idle before the draft is flushed to disk


# ---------------------------------------------------------------------------
# config
# ---------------------------------------------------------------------------

def load_config() -> dict:
    if CONFIG_PATH.exists():
        try:
            return json.loads(CONFIG_PATH.read_text())
        except (json.JSONDecodeError, OSError):
            pass
    return {}


def save_config(cfg: dict) -> None:
    CONFIG_PATH.write_text(json.dumps(cfg, indent=2))
    try:
        CONFIG_PATH.chmod(0o600)
    except OSError:
        pass


# ---------------------------------------------------------------------------
# local copy helpers
# ---------------------------------------------------------------------------

def _unique_path(base: str) -> Path:
    """Return base.md, or base-1.md, base-2.md, ... if collisions."""
    path = LOCAL_POSTS_DIR / f"{base}.md"
    n = 1
    while path.exists():
        path = LOCAL_POSTS_DIR / f"{base}-{n}.md"
        n += 1
    return path


def save_local_copy(body: str, tags: str, status: str, detail: str = "") -> Path:
    """Always save a local .md copy of an attempted post, success or failure."""
    LOCAL_POSTS_DIR.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc)
    date_str = now.strftime("%Y-%m-%d")
    ts = now.strftime("%H%M%S")

    path = _unique_path(f"{date_str}-{ts}-{status}")

    tag_list = ""
    if tags:
        tag_list = ", ".join(f'"{t.strip()}"' for t in tags.split(","))

    frontmatter = [
        "---",
        f"date: {date_str}",
        f"tags: [{tag_list}]",
        f"status: {status}",
    ]
    if detail:
        detail_escaped = detail.replace('"', "'")
        frontmatter.append(f'detail: "{detail_escaped}"')
    frontmatter.append("---")

    content = "\n".join(frontmatter) + f"\n\n{body}\n"
    path.write_text(content)
    return path


# ---------------------------------------------------------------------------
# settings modal
# ---------------------------------------------------------------------------

class SettingsScreen(ModalScreen[dict | None]):
    """Modal for entering/editing server URL + secret."""

    DEFAULT_CSS = """
    SettingsScreen {
        align: center middle;
    }
    #dialog {
        width: 60;
        height: auto;
        border: round $accent;
        padding: 1 2;
        background: $panel;
    }
    #dialog Input {
        margin-bottom: 1;
    }
    #buttons {
        align-horizontal: right;
        height: auto;
    }
    #test-result {
        color: $text-muted;
        height: auto;
    }
    """

    BINDINGS = [Binding("escape", "cancel", "Cancel")]

    def __init__(self, cfg: dict):
        super().__init__()
        self._cfg = cfg
        self._testing = False

    def compose(self) -> ComposeResult:
        with Vertical(id="dialog"):
            yield Label("Server settings")
            yield Input(
                value=self._cfg.get("url", ""),
                placeholder="http://host:8080  (no trailing /post)",
                id="url",
            )
            yield Input(
                value=self._cfg.get("secret", ""),
                placeholder="shared secret (X-Secret header)",
                password=True,
                id="secret",
            )
            yield Static("", id="test-result")
            with Horizontal(id="buttons"):
                yield Button("Test", id="test")
                yield Button("Cancel", id="cancel")
                yield Button("Save", id="save", variant="primary")

    def _fields(self) -> tuple[str, str]:
        url = self.query_one("#url", Input).value.strip().rstrip("/")
        secret = self.query_one("#secret", Input).value.strip()
        return url, secret

    def _set_result(self, markup: str) -> None:
        # Safe: always called on the main (UI) thread.
        self.query_one("#test-result", Static).update(markup)

    def action_cancel(self) -> None:
        self.dismiss(None)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "save":
            url, secret = self._fields()
            if not url or not secret:
                self.notify("URL and secret are both required.",
                            severity="error")
                return
            self.dismiss({"url": url, "secret": secret})
            return

        if event.button.id == "test":
            if self._testing:
                return
            url, secret = self._fields()
            if not url or not secret:
                self.notify("Fill in URL and secret before testing.",
                            severity="warning")
                return
            self._testing = True
            self.query_one("#test", Button).disabled = True
            self._set_result("testing...")
            self._test(url, secret)
            return

        self.dismiss(None)

    @work(thread=True, exclusive=True)
    def _test(self, url: str, secret: str) -> None:
        try:
            r = requests.get(
                f"{url}/health",
                headers={"X-Secret": secret},
                timeout=5,
            )
        except requests.RequestException as exc:
            msg = f"[red]cannot reach server: {exc.__class__.__name__}[/red]"
        else:
            if r.status_code == 200:
                msg = "[green]connection OK[/green]"
            elif r.status_code == 401:
                msg = "[red]secret rejected (401)[/red]"
            elif r.status_code == 404:
                msg = ("[yellow]server reachable, "
                       "but no /health endpoint[/yellow]")
            else:
                msg = f"[red]HTTP {r.status_code}[/red]"

        self.app.call_from_thread(self._finish_test, msg)

    def _finish_test(self, msg: str) -> None:
        # Runs on the main thread. Guard against the modal having been
        # dismissed while the request was in flight.
        self._testing = False
        try:
            self._set_result(msg)
            self.query_one("#test", Button).disabled = False
        except Exception:
            pass


# ---------------------------------------------------------------------------
# local copies modal
# ---------------------------------------------------------------------------

class LocalCopiesScreen(ModalScreen[None]):
    """Read-only browser for local_posts/."""

    DEFAULT_CSS = """
    LocalCopiesScreen { align: center middle; }
    #dialog {
        width: 90%;
        height: 80%;
        border: round $accent;
        padding: 1 2;
        background: $panel;
    }
    #copies-list { height: 1fr; }
    ListItem { padding: 0 1; }
    """

    BINDINGS = [Binding("escape", "dismiss", "Close")]

    def compose(self) -> ComposeResult:
        with Vertical(id="dialog"):
            yield Label("Local copies (local_posts/)")
            with VerticalScroll():
                yield ListView(id="copies-list")
            yield Static("esc to close", id="hint")

    def on_mount(self) -> None:
        lv = self.query_one("#copies-list", ListView)
        if not LOCAL_POSTS_DIR.exists():
            lv.append(ListItem(Label("(no local copies yet)")))
            return
        files = sorted(LOCAL_POSTS_DIR.glob("*.md"), reverse=True)
        if not files:
            lv.append(ListItem(Label("(no local copies yet)")))
            return
        for f in files:
            lv.append(ListItem(Label(f.name)))

    def action_dismiss(self) -> None:
        self.dismiss(None)


# ---------------------------------------------------------------------------
# main app
# ---------------------------------------------------------------------------

class TimelinePostApp(App):
    TITLE = "Timeline Post"

    CSS = """
    #body {
        height: 1fr;
        border: round $primary;
        margin: 1 1 0 1;
    }
    #tags {
        margin: 1 1 0 1;
    }
    #status {
        margin: 0 1 1 1;
        color: $text-muted;
        height: auto;
    }
    """

    BINDINGS = [
        Binding("ctrl+s", "post", "Post"),
        Binding("ctrl+r", "settings", "Settings"),
        Binding("ctrl+l", "local_copies", "Local"),
        Binding("ctrl+q", "quit", "Quit"),
    ]

    def __init__(self):
        super().__init__()
        self.cfg = load_config()
        self._draft_timer = None

    def compose(self) -> ComposeResult:
        yield Header()
        yield TextArea(id="body")
        yield Input(placeholder="tags (comma separated, optional)", id="tags")
        yield Static(self._status_text(), id="status")
        yield Footer()

    # ---- lifecycle -------------------------------------------------------

    def on_mount(self) -> None:
        if DRAFT_PATH.exists():
            try:
                self.query_one("#body", TextArea).text = DRAFT_PATH.read_text()
                self.notify("Restored unsaved draft.")
            except OSError:
                pass
        self.query_one("#body", TextArea).focus()
        if not self.cfg.get("url") or not self.cfg.get("secret"):
            self.action_settings()

    def _status_text(self) -> str:
        target = self.cfg.get("url") or "(not configured)"
        return (
            f"target: {target}   "
            "ctrl+s post · ctrl+r settings · ctrl+l local · ctrl+q quit"
        )

    # ---- draft autosave --------------------------------------------------

    def on_text_area_changed(self, event: TextArea.Changed) -> None:
        # Debounce: cancel any pending save and schedule a fresh one, so a
        # burst of keystrokes results in one write shortly after typing
        # pauses instead of a write per keystroke.
        if self._draft_timer is not None:
            self._draft_timer.stop()
        self._draft_timer = self.set_timer(
            DRAFT_SAVE_DELAY, lambda: self._save_draft(event.text_area.text)
        )

    def _save_draft(self, text: str) -> None:
        try:
            DRAFT_PATH.write_text(text)
        except OSError:
            pass

    # ---- key handling ----------------------------------------------------

    def on_key(self, event) -> None:
        if event.key == "ctrl+enter":
            event.stop()
            self.action_post()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        if event.input.id == "tags":
            self.action_post()

    # ---- actions ---------------------------------------------------------

    def action_settings(self) -> None:
        def handle(result: dict | None) -> None:
            if result:
                self.cfg = result
                save_config(self.cfg)
                self.query_one("#status", Static).update(self._status_text())
                self.notify("Settings saved.")

        self.push_screen(SettingsScreen(self.cfg), handle)

    def action_local_copies(self) -> None:
        self.push_screen(LocalCopiesScreen())

    def action_post(self) -> None:
        if not self.cfg.get("url") or not self.cfg.get("secret"):
            self.notify("Set server URL and secret first (ctrl+r).",
                        severity="error")
            self.action_settings()
            return

        body = self.query_one("#body", TextArea).text.strip()
        if not body:
            self.notify("Nothing to post — body is empty.",
                        severity="warning")
            return

        # Flush any debounced draft write so the on-disk draft reflects
        # exactly what's about to be posted, in case it fails.
        if self._draft_timer is not None:
            self._draft_timer.stop()
            self._draft_timer = None
            self._save_draft(self.query_one("#body", TextArea).text)

        tags = self.query_one("#tags", Input).value.strip()
        self.query_one("#status", Static).update("[yellow]posting...[/yellow]")
        self.do_post(body, tags)

    @work(thread=True)
    def do_post(self, body: str, tags: str) -> None:
        url = self.cfg["url"].rstrip("/") + "/post"
        try:
            resp = requests.post(
                url,
                headers={"X-Secret": self.cfg["secret"]},
                json={"text": body, "tags": tags},
                timeout=15,
            )
        except requests.RequestException as exc:
            detail = f"{exc.__class__.__name__}: {exc}"
            local_path = save_local_copy(body, tags, status="failed",
                                         detail=detail)
            self.app.call_from_thread(self._post_failed, detail, local_path)
            return

        if resp.status_code == 201:
            try:
                data = resp.json()
                remote_path = data.get("file", "?")
            except ValueError:
                remote_path = "?"
            local_path = save_local_copy(body, tags, status="posted",
                                         detail=remote_path)
            self.app.call_from_thread(self._post_succeeded,
                                      remote_path, local_path)
            return

        try:
            msg = resp.json().get("error", resp.text)
        except ValueError:
            msg = resp.text
        detail = f"{resp.status_code}: {msg}"
        local_path = save_local_copy(body, tags, status="failed",
                                     detail=detail)
        self.app.call_from_thread(self._post_failed, detail, local_path)

    # ---- completion handlers --------------------------------------------

    def _post_succeeded(self, remote_path: str, local_path: Path) -> None:
        self.notify(f"Posted: {remote_path}\nsaved copy: {local_path.name}")
        self.query_one("#body", TextArea).text = ""
        self.query_one("#tags", Input).value = ""
        DRAFT_PATH.unlink(missing_ok=True)
        self.query_one("#status", Static).update(
            f"[green]last posted: {remote_path}  "
            f"(copy: {local_path.name})[/green]"
        )

    def _post_failed(self, message: str, local_path: Path) -> None:
        self.notify(
            f"Failed: {message}\nsaved copy: {local_path.name}",
            severity="error",
            timeout=8,
        )
        self.query_one("#status", Static).update(
            f"[red]last post failed: {message}  "
            f"(copy: {local_path.name})[/red]"
        )


if __name__ == "__main__":
    TimelinePostApp().run()