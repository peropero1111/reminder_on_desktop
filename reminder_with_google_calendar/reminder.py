from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
import sysconfig
import threading
import traceback
import uuid
from dataclasses import dataclass
from datetime import date, datetime, time, timedelta
from pathlib import Path
from typing import Any
import tkinter as tk
from tkinter import messagebox

try:
    from zoneinfo import ZoneInfo
except ImportError:  # pragma: no cover - Python 3.9+ has zoneinfo.
    ZoneInfo = None


def get_app_dir() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent


APP_DIR = get_app_dir()
CONFIG_PATH = APP_DIR / "reminder_widget_config.json"
LOCAL_REMINDERS_PATH = APP_DIR / "reminder_local_events.json"

FONT_FAMILY = "Malgun Gothic"
DAY_NAMES = ["월", "화", "수", "목", "금", "토", "일"]

DEFAULT_CONFIG: dict[str, Any] = {
    "ical_urls": [],
    "timezone": "Asia/Seoul",
    "refresh_minutes": 30,
    "notifications": {
        "enabled": True,
        "minutes_before": 30,
        "check_seconds": 60,
        "include_all_day": False,
    },
    "window": {
        "x": 40,
        "y": 80,
        "width": 215,
        "height": 320,
        "opacity": 0.94,
        "always_on_top": False,
        "frameless": True,
    },
    "privacy": {
        "mask_title": "비공개 일정",
        "hidden_events": [],
    },
    "theme": {
        "background": "#111315",
        "panel": "#1A1D21",
        "panel_soft": "#22272E",
        "text": "#F4F6F8",
        "muted": "#A9B1BA",
        "accent": "#70D6C4",
        "accent_2": "#FFB86B",
        "border": "#30363D",
        "today": "#344F52",
        "error": "#FF6B6B",
    },
}


@dataclass(frozen=True)
class ReminderEvent:
    id: str
    source: str
    title: str
    start: datetime
    end: datetime
    all_day: bool
    location: str = ""
    calendar_name: str = ""
    private: bool = False
    note: str = ""


def deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    merged = dict(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = deep_merge(merged[key], value)
        else:
            merged[key] = value
    return merged


def load_config() -> tuple[dict[str, Any], str | None]:
    if not CONFIG_PATH.exists():
        try:
            CONFIG_PATH.write_text(
                json.dumps(DEFAULT_CONFIG, indent=2, ensure_ascii=False),
                encoding="utf-8",
            )
        except OSError as exc:
            return dict(DEFAULT_CONFIG), f"설정 파일을 만들 수 없습니다: {exc}"
        return dict(DEFAULT_CONFIG), None

    try:
        user_config = json.loads(CONFIG_PATH.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError) as exc:
        return dict(DEFAULT_CONFIG), f"설정 파일을 읽을 수 없습니다: {exc}"

    return deep_merge(DEFAULT_CONFIG, user_config), None


def save_config(config: dict[str, Any]) -> None:
    CONFIG_PATH.write_text(
        json.dumps(config, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def ensure_stdlib_calendar_module() -> None:
    current = sys.modules.get("calendar")
    if current is not None:
        module_path = getattr(current, "__file__", "")
        try:
            is_local_calendar = Path(module_path).resolve() == APP_DIR / "calendar.py"
        except (OSError, RuntimeError, TypeError):
            is_local_calendar = False
        if not is_local_calendar:
            return

    stdlib_path = Path(sysconfig.get_path("stdlib")) / "calendar.py"
    spec = importlib.util.spec_from_file_location("calendar", stdlib_path)
    if spec is None or spec.loader is None:
        raise RuntimeError("표준 calendar 모듈을 불러올 수 없습니다.")

    module = importlib.util.module_from_spec(spec)
    sys.modules["calendar"] = module
    spec.loader.exec_module(module)


def clean_text(value: Any, fallback: str = "") -> str:
    text = str(value or fallback).replace("\\n", " ").replace("\n", " ").strip()
    return " ".join(text.split()) or fallback


def make_timezone(name: str):
    if ZoneInfo is not None:
        try:
            return ZoneInfo(name)
        except Exception:
            pass
    return datetime.now().astimezone().tzinfo


def date_to_datetime(value: date | datetime, tz) -> datetime:
    if isinstance(value, datetime):
        if value.tzinfo is None:
            return value.replace(tzinfo=tz)
        return value.astimezone(tz)
    return datetime.combine(value, time.min).replace(tzinfo=tz)


def valid_ical_urls(urls: Any) -> list[str]:
    valid_urls = []
    placeholders = ("PASTE_", "input_ical_urls")
    if isinstance(urls, str):
        raw_urls = [urls]
    elif isinstance(urls, list):
        raw_urls = urls
    else:
        return valid_urls

    for raw_url in raw_urls:
        url = str(raw_url).strip()
        if not url or any(marker in url for marker in placeholders):
            continue
        valid_urls.append(url)
    return valid_urls


def make_google_event_id(
    calendar_name: str,
    uid: str,
    recurrence_id: str,
    start: datetime,
    title: str,
    location: str,
) -> str:
    source = "|".join([calendar_name, uid, recurrence_id, start.isoformat(), title, location])
    return hashlib.sha256(source.encode("utf-8")).hexdigest()


def load_ical_dependencies():
    ensure_stdlib_calendar_module()

    try:
        import recurring_ical_events
        import requests
        from icalendar import Calendar
    except ImportError as exc:
        raise RuntimeError(
            "필요한 패키지가 없습니다. 먼저 `python -m pip install -r requirements.txt`를 실행하세요."
        ) from exc
    return recurring_ical_events, requests, Calendar


def event_from_component(component, tz, calendar_name: str) -> ReminderEvent | None:
    start_prop = component.get("DTSTART")
    if start_prop is None:
        return None

    raw_start = start_prop.dt
    raw_end = component.get("DTEND").dt if component.get("DTEND") is not None else None

    all_day = isinstance(raw_start, date) and not isinstance(raw_start, datetime)
    start = date_to_datetime(raw_start, tz)

    if raw_end is None:
        end = start + (timedelta(days=1) if all_day else timedelta(hours=1))
    else:
        end = date_to_datetime(raw_end, tz)

    if end <= start:
        end = start + (timedelta(days=1) if all_day else timedelta(hours=1))

    title = clean_text(component.get("SUMMARY"), "(제목 없음)")
    location = clean_text(component.get("LOCATION"))
    uid = clean_text(component.get("UID"))
    recurrence_id = clean_text(component.get("RECURRENCE-ID"))
    event_id = make_google_event_id(calendar_name, uid, recurrence_id, start, title, location)

    return ReminderEvent(
        id=event_id,
        source="google",
        title=title,
        start=start,
        end=end,
        all_day=all_day,
        location=location,
        calendar_name=calendar_name,
        private=str(component.get("CLASS", "")).upper() == "PRIVATE",
    )


def fetch_year_google_events(
    ical_urls: list[str],
    period_start: datetime,
    period_end: datetime,
    tz,
) -> list[ReminderEvent]:
    recurring_ical_events, requests, Calendar = load_ical_dependencies()

    query_start = period_start - timedelta(days=31)
    query_end = period_end + timedelta(days=1)
    events: list[ReminderEvent] = []
    seen: set[tuple[str, datetime, datetime, str]] = set()

    for url in ical_urls:
        response = requests.get(
            url,
            headers={"User-Agent": "GoogleCalendarDesktopReminder/1.0"},
            timeout=25,
        )
        response.raise_for_status()

        calendar_data = Calendar.from_ical(response.content)
        calendar_name = clean_text(calendar_data.get("X-WR-CALNAME"), "Google Calendar")
        expanded_events = recurring_ical_events.of(calendar_data).between(query_start, query_end)

        for component in expanded_events:
            if getattr(component, "name", "") != "VEVENT":
                continue
            event = event_from_component(component, tz, calendar_name)
            if event is None:
                continue
            if event.end <= period_start or event.start >= period_end:
                continue

            key = (event.title, event.start, event.end, event.location)
            if key in seen:
                continue
            seen.add(key)
            events.append(event)

    return sorted(events, key=lambda item: (item.start, item.end, item.title.lower()))


def parse_datetime(value: Any, tz) -> datetime | None:
    if not value:
        return None
    text = str(value).strip()
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    try:
        parsed = datetime.fromisoformat(text)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=tz)
    return parsed.astimezone(tz)


def load_local_reminders(tz) -> list[ReminderEvent]:
    if not LOCAL_REMINDERS_PATH.exists():
        return []

    try:
        payload = json.loads(LOCAL_REMINDERS_PATH.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError):
        return []

    raw_items = payload.get("reminders", payload) if isinstance(payload, dict) else payload
    if not isinstance(raw_items, list):
        return []

    reminders: list[ReminderEvent] = []
    for raw_item in raw_items:
        if not isinstance(raw_item, dict):
            continue

        title = clean_text(raw_item.get("title"))
        start = parse_datetime(raw_item.get("start"), tz)
        if not title or start is None:
            continue

        all_day = bool(raw_item.get("all_day", False))
        end = parse_datetime(raw_item.get("end"), tz)
        if end is None or end <= start:
            end = start + (timedelta(days=1) if all_day else timedelta(hours=1))

        reminders.append(
            ReminderEvent(
                id=clean_text(raw_item.get("id"), uuid.uuid4().hex),
                source="local",
                title=title,
                start=start,
                end=end,
                all_day=all_day,
                location=clean_text(raw_item.get("location")),
                note=clean_text(raw_item.get("note")),
            )
        )

    return sorted(reminders, key=lambda item: (item.start, item.end, item.title.lower()))


def save_local_reminders(reminders: list[ReminderEvent]) -> None:
    payload = {
        "version": 1,
        "reminders": [
            {
                "id": reminder.id,
                "title": reminder.title,
                "start": reminder.start.isoformat(),
                "end": reminder.end.isoformat(),
                "all_day": reminder.all_day,
                "location": reminder.location,
                "note": reminder.note,
            }
            for reminder in sorted(reminders, key=lambda item: (item.start, item.title.lower()))
        ],
    }
    LOCAL_REMINDERS_PATH.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def day_bounds(day: date, tz) -> tuple[datetime, datetime]:
    start = datetime.combine(day, time.min).replace(tzinfo=tz)
    return start, start + timedelta(days=1)


def event_active_on_day(event: ReminderEvent, day: date, tz) -> bool:
    day_start, day_end = day_bounds(day, tz)
    return event.start < day_end and event.end > day_start


def format_date_heading(day: date) -> str:
    weekday = DAY_NAMES[day.weekday()]
    return f"{day.month}월 {day.day}일 ({weekday})"


def format_event_time(event: ReminderEvent, day: date) -> str:
    if event.all_day:
        return "종일"

    end_for_date = event.end - timedelta(microseconds=1)
    if event.start.date() == day and end_for_date.date() == day:
        return f"{event.start:%H:%M}-{event.end:%H:%M}"
    if event.start.date() == day:
        return f"{event.start:%H:%M} 시작"
    if end_for_date.date() == day:
        return f"{event.end:%H:%M} 종료"
    return "계속"


def mark_name_for_day(day: date) -> str:
    return f"day_{day:%Y%m%d}"


class ReminderApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.config, self.config_error = load_config()
        self.theme = self.config["theme"]
        self.tz = make_timezone(str(self.config.get("timezone", "Asia/Seoul")))
        self.today = datetime.now(self.tz).date()
        self.period_start = datetime.combine(self.today, time.min).replace(tzinfo=self.tz)
        self.period_end = self.period_start + timedelta(days=365)

        self.google_events: list[ReminderEvent] = []
        self.local_reminders: list[ReminderEvent] = load_local_reminders(self.tz)
        self.loading = False
        self.last_error: str | None = None
        self.local_store_error: str | None = None
        self.local_event_tags: dict[str, str] = {}
        self.agenda_event_tags: dict[str, str] = {}
        self.drag_offset: tuple[int, int] | None = None

        notification_config = self.config.get("notifications", {})
        self.notifications_enabled = bool(notification_config.get("enabled", True))
        self.notification_minutes_before = max(1, int(notification_config.get("minutes_before", 30)))
        self.notification_check_seconds = max(10, int(notification_config.get("check_seconds", 60)))
        self.notification_include_all_day = bool(notification_config.get("include_all_day", False))
        self.sent_notification_keys: set[str] = set()
        self.notification_error: str | None = None

        privacy_config = self.config.get("privacy", {})
        self.hidden_event_keys: set[str] = set(privacy_config.get("hidden_events", []))
        self.privacy_select_mode = False

        self.root.title("Google Calendar Reminder")
        self.configure_window()
        self.build_ui()
        self.render()

        if self.config_error is None and valid_ical_urls(self.config.get("ical_urls", [])):
            self.refresh_google_events()

        self.schedule_auto_refresh()
        self.schedule_notification_check()
        self.root.protocol("WM_DELETE_WINDOW", self.close)

    def configure_window(self) -> None:
        window_config = self.config.get("window", DEFAULT_CONFIG["window"])

        width = int(window_config.get("width", 215))
        height = int(window_config.get("height", 320))
        x = int(window_config.get("x", 40))
        y = int(window_config.get("y", 80))

        self.root.geometry(f"{width}x{height}+{x}+{y}")
        self.root.minsize(215, 320)
        self.root.configure(bg=self.theme["background"])

        try:
            self.root.attributes("-alpha", float(window_config.get("opacity", 0.94)))
            self.root.attributes("-topmost", bool(window_config.get("always_on_top", False)))
        except tk.TclError:
            pass

        if bool(window_config.get("frameless", True)):
            self.root.overrideredirect(True)

    def build_ui(self) -> None:
        self.container = tk.Frame(
            self.root,
            bg=self.theme["background"],
            highlightthickness=1,
            highlightbackground=self.theme["border"],
        )
        self.container.pack(fill="both", expand=True)

        self.title_bar = tk.Frame(self.container, bg=self.theme["panel"], height=36)
        self.title_bar.pack(fill="x")
        self.title_bar.pack_propagate(False)
        self.title_bar.bind("<ButtonPress-1>", self.start_drag)
        self.title_bar.bind("<B1-Motion>", self.drag_window)

        self.title_label = tk.Label(
            self.title_bar,
            text="Reminder",
            bg=self.theme["panel"],
            fg=self.theme["text"],
            font=(FONT_FAMILY, 11, "bold"),
            anchor="w",
        )
        self.title_label.pack(side="left", padx=(8, 4), fill="x", expand=True)
        self.title_label.bind("<ButtonPress-1>", self.start_drag)
        self.title_label.bind("<B1-Motion>", self.drag_window)

        button_specs = [
            ("오늘", self.scroll_to_today, "오늘로 이동"),
            ("+", self.open_add_dialog, "Reminder 추가"),
            (self.privacy_button_text(), self.toggle_privacy, "숨길 일정 선택"),
            ("↻", self.refresh_google_events, "새로고침"),
            ("×", self.close, "닫기"),
        ]
        for label, command, tooltip in button_specs:
            button = tk.Button(
                self.title_bar,
                text=label,
                command=command,
                bd=0,
                relief="flat",
                bg=self.theme["panel"],
                fg=self.theme["text"],
                activebackground=self.theme["panel_soft"],
                activeforeground=self.theme["accent"],
                font=(FONT_FAMILY, 9, "bold"),
                width=3 if len(str(label)) > 1 else 2,
                cursor="hand2",
                takefocus=False,
            )
            button.pack(side="left", padx=(0, 1), pady=5)
            if command == self.toggle_privacy:
                self.privacy_button = button
            button.bind("<Enter>", lambda _event, text=tooltip: self.set_status(text))
            button.bind("<Leave>", lambda _event: self.render_status())

        self.summary_holder = tk.Frame(self.container, bg=self.theme["background"], height=72)
        self.summary_holder.pack(fill="x", padx=8, pady=(8, 4))
        self.summary_holder.pack_propagate(False)

        self.range_label = tk.Label(
            self.summary_holder,
            text="",
            bg=self.theme["panel"],
            fg=self.theme["accent"],
            font=(FONT_FAMILY, 8, "bold"),
            anchor="w",
            padx=10,
            pady=5,
        )
        self.range_label.pack(fill="x")

        self.next_label = tk.Label(
            self.summary_holder,
            text="",
            bg=self.theme["panel"],
            fg=self.theme["text"],
            font=(FONT_FAMILY, 8),
            anchor="nw",
            justify="left",
            padx=10,
            pady=5,
            wraplength=170,
        )
        self.next_label.pack(fill="both", expand=True)

        self.status_label = tk.Label(
            self.container,
            text="",
            bg=self.theme["background"],
            fg=self.theme["muted"],
            font=(FONT_FAMILY, 8),
            anchor="w",
        )
        self.status_label.pack(fill="x", padx=10, pady=(0, 4))

        agenda_frame = tk.Frame(self.container, bg=self.theme["background"])
        agenda_frame.pack(fill="both", expand=True, padx=8, pady=(0, 8))

        self.agenda_text = tk.Text(
            agenda_frame,
            bd=0,
            wrap="word",
            bg=self.theme["panel"],
            fg=self.theme["text"],
            insertbackground=self.theme["text"],
            selectbackground=self.theme["today"],
            font=(FONT_FAMILY, 9),
            padx=8,
            pady=8,
            relief="flat",
            height=6,
        )
        self.agenda_text.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(
            agenda_frame,
            orient="vertical",
            command=self.agenda_text.yview,
            width=10,
        )
        scrollbar.pack(side="right", fill="y")
        self.agenda_text.configure(yscrollcommand=scrollbar.set)

        self.agenda_text.tag_configure(
            "date",
            foreground=self.theme["accent"],
            font=(FONT_FAMILY, 9, "bold"),
            spacing1=7,
            spacing3=2,
        )
        self.agenda_text.tag_configure(
            "time",
            foreground=self.theme["accent_2"],
            font=(FONT_FAMILY, 8, "bold"),
        )
        self.agenda_text.tag_configure("google", foreground=self.theme["muted"])
        self.agenda_text.tag_configure("local", foreground=self.theme["accent"])
        self.agenda_text.tag_configure("muted", foreground=self.theme["muted"])
        self.agenda_text.tag_configure("error", foreground=self.theme["error"])
        self.agenda_text.tag_configure("private", foreground=self.theme["muted"])
        self.agenda_text.tag_configure("week_event", foreground=self.theme["error"])
        self.agenda_text.configure(state="disabled")

    def period_events(self) -> list[ReminderEvent]:
        events = [
            event
            for event in [*self.google_events, *self.local_reminders]
            if event.end > self.period_start and event.start < self.period_end
        ]
        return sorted(events, key=lambda item: (item.start, item.end, item.source, item.title.lower()))

    def next_event(self) -> ReminderEvent | None:
        now = datetime.now(self.tz)
        for event in self.period_events():
            if event.end >= now:
                return event
        return None

    def is_current_week_day(self, day: date) -> bool:
        today = datetime.now(self.tz).date()
        week_start = today - timedelta(days=today.weekday())
        week_end = week_start + timedelta(days=6)
        return week_start <= day <= week_end

    def render(self) -> None:
        self.today = datetime.now(self.tz).date()
        if hasattr(self, "privacy_button"):
            self.privacy_button.configure(text=self.privacy_button_text())
        self.render_summary()
        self.render_agenda()
        self.render_status()

    def render_summary(self) -> None:
        end_day = (self.period_end - timedelta(days=1)).date()
        total_events = len(self.period_events())
        local_visible = len(
            [
                event
                for event in self.local_reminders
                if event.end > self.period_start and event.start < self.period_end
            ]
        )
        self.range_label.configure(
            text=f"{self.period_start:%Y.%m.%d} - {end_day:%Y.%m.%d} | {total_events}개"
        )

        upcoming = self.next_event()
        if upcoming is None:
            self.next_label.configure(text="다가오는 reminder가 없습니다.")
            return

        title = self.display_event_title(upcoming)
        day_text = format_date_heading(upcoming.start.date())
        time_text = "종일" if upcoming.all_day else f"{upcoming.start:%H:%M}"
        if upcoming.source == "local":
            next_text = f"다음: [앱] {day_text} {time_text}\n{title}"
        else:
            next_text = f"다음: {day_text} {time_text}\n{title}"
        self.next_label.configure(text=next_text)

    def render_agenda(self) -> None:
        self.agenda_text.configure(state="normal")
        self.agenda_text.delete("1.0", "end")
        self.local_event_tags = {}
        self.agenda_event_tags = {}

        if self.config_error:
            self.agenda_text.insert("end", self.config_error + "\n\n", "error")

        events = self.period_events()
        if not events:
            self.agenda_text.insert("end", "앞으로 1년 동안 표시할 일정이 없습니다.\n", "muted")
            self.agenda_text.configure(state="disabled")
            return

        rendered_days: set[date] = set()
        for event in events:
            day = max(event.start.date(), self.period_start.date())
            if day not in rendered_days:
                rendered_days.add(day)
                self.agenda_text.mark_set(mark_name_for_day(day), "end")
                self.agenda_text.insert("end", format_date_heading(day) + "\n", "date")

            time_label = format_event_time(event, day)
            week_tags = ("week_event",) if self.is_current_week_day(day) else ()
            source_tag = "local" if event.source == "local" else "google"
            click_tags = self.register_agenda_event_tag(event)

            self.agenda_text.insert("end", f"  {time_label:<11}", ("time", *week_tags, *click_tags))
            if event.source == "local":
                self.agenda_text.insert("end", "[앱] ", (source_tag, *week_tags, *click_tags))
            else:
                self.agenda_text.insert("end", " ", (*week_tags, *click_tags))

            title = self.display_event_title(event)
            base_title_tags = ("private",) if self.should_mask_event(event) else ()
            self.agenda_text.insert("end", title + "\n", (*base_title_tags, *week_tags, *click_tags))

            detail = event.note if event.source == "local" else event.location
            if detail and not self.should_mask_event(event):
                self.agenda_text.insert("end", f"    {detail}\n", ("muted", *click_tags))

        if self.last_error:
            self.agenda_text.insert("end", "\n최근 새로고침 실패:\n", "error")
            self.agenda_text.insert("end", self.last_error + "\n", "muted")

        if self.local_store_error:
            self.agenda_text.insert("end", "\n로컬 reminder 저장 오류:\n", "error")
            self.agenda_text.insert("end", self.local_store_error + "\n", "muted")

        self.agenda_text.configure(state="disabled")

    def register_agenda_event_tag(self, event: ReminderEvent) -> tuple[str, ...]:
        event_tag = f"event_{event.source}_{event.id}"
        if event_tag in self.agenda_event_tags:
            return (event_tag,)

        self.agenda_event_tags[event_tag] = self.event_hidden_key(event)
        self.agenda_text.tag_bind(
            event_tag,
            "<Button-1>",
            lambda _event, selected_event=event: self.handle_event_click(selected_event),
        )
        self.agenda_text.tag_bind(
            event_tag,
            "<Enter>",
            lambda _event: self.agenda_text.configure(cursor="hand2"),
        )
        self.agenda_text.tag_bind(
            event_tag,
            "<Leave>",
            lambda _event: self.agenda_text.configure(cursor=""),
        )
        return (event_tag,)

    def event_hidden_key(self, event: ReminderEvent) -> str:
        return f"{event.source}:{event.id}"

    def handle_event_click(self, event: ReminderEvent) -> None:
        if self.privacy_select_mode:
            self.toggle_event_hidden(self.event_hidden_key(event))
            return

        if event.source == "local":
            self.confirm_delete_local_reminder(event.id)
            return

        self.set_status("상단의 선택 버튼을 누른 뒤 일정을 클릭하면 숨길 수 있습니다.")

    def privacy_button_text(self) -> str:
        return "완료" if self.privacy_select_mode else "선택"

    def toggle_privacy(self) -> None:
        self.privacy_select_mode = not self.privacy_select_mode
        self.render()

    def toggle_event_hidden(self, event_key: str) -> None:
        if event_key in self.hidden_event_keys:
            self.hidden_event_keys.remove(event_key)
        else:
            self.hidden_event_keys.add(event_key)

        self.save_hidden_events()
        self.render()

    def save_hidden_events(self) -> None:
        privacy_config = self.config.setdefault("privacy", {})
        privacy_config["hide_details"] = False
        privacy_config["hidden_events"] = sorted(self.hidden_event_keys)
        try:
            save_config(self.config)
        except OSError as exc:
            messagebox.showwarning("저장 실패", f"숨김 설정을 저장하지 못했습니다.\n{exc}")

    def insert_setup_text(self) -> None:
        self.agenda_text.insert("end", "Google Calendar iCal 설정\n", "date")
        self.agenda_text.insert(
            "end",
            (
                f"{CONFIG_PATH.name} 파일의 ical_urls 값을 설정하면 Google 일정이 함께 표시됩니다.\n\n"
            ),
            "muted",
        )

    def should_mask_event(self, event: ReminderEvent) -> bool:
        return (
            event.private
            or self.event_hidden_key(event) in self.hidden_event_keys
            or event.id in self.hidden_event_keys
        )

    def display_event_title(self, event: ReminderEvent) -> str:
        if self.should_mask_event(event):
            privacy_config = self.config.get("privacy", {})
            return str(privacy_config.get("mask_title", "비공개 일정"))
        return event.title

    def render_status(self) -> None:
        if self.loading:
            self.set_status("Google 일정 로딩 중...")
            return

        google_count = len(self.google_events)
        local_count = len(self.local_reminders)
        refresh_minutes = int(self.config.get("refresh_minutes", 30))
        hidden_count = len(self.hidden_event_keys)

        if self.privacy_select_mode:
            self.set_status(f"숨김 선택 | {hidden_count}개")
            return

        if self.config_error:
            self.set_status("설정 오류 | 앱 reminder 가능")
        elif not valid_ical_urls(self.config.get("ical_urls", [])):
            self.set_status(f"앱 {local_count}개 | 숨김 {hidden_count}개")
        else:
            self.set_status(
                f"G {google_count} | 앱 {local_count} | 숨김 {hidden_count} | {refresh_minutes}분"
            )

    def set_status(self, text: str) -> None:
        self.status_label.configure(text=text)

    def refresh_google_events(self) -> None:
        urls = valid_ical_urls(self.config.get("ical_urls", []))
        if self.loading or not urls or self.config_error is not None:
            self.render()
            return

        self.loading = True
        self.last_error = None
        self.render_status()

        worker = threading.Thread(
            target=self.fetch_worker,
            args=(urls, self.period_start, self.period_end),
            daemon=True,
        )
        worker.start()

    def fetch_worker(
        self,
        urls: list[str],
        period_start: datetime,
        period_end: datetime,
    ) -> None:
        try:
            events = fetch_year_google_events(urls, period_start, period_end, self.tz)
        except Exception:
            error = traceback.format_exc(limit=2).strip()
            self.root.after(0, lambda: self.finish_refresh([], error))
            return

        self.root.after(0, lambda: self.finish_refresh(events, None))

    def finish_refresh(
        self,
        events: list[ReminderEvent],
        error: str | None,
    ) -> None:
        self.loading = False
        if error:
            self.last_error = error
        else:
            self.google_events = events
            self.last_error = None
            if self.notifications_enabled:
                self.send_due_notifications()

        self.render()

    def open_add_dialog(self) -> None:
        dialog = tk.Toplevel(self.root)
        dialog.title("Reminder 추가")
        dialog.configure(bg=self.theme["background"])
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.resizable(False, False)

        outer = tk.Frame(dialog, bg=self.theme["background"], padx=14, pady=14)
        outer.pack(fill="both", expand=True)

        title_label = self.make_dialog_label(outer, "제목")
        title_label.grid(row=0, column=0, sticky="w", pady=(0, 6))
        title_entry = self.make_dialog_entry(outer)
        title_entry.grid(row=0, column=1, sticky="ew", pady=(0, 6))

        default_time = datetime.now(self.tz) + timedelta(minutes=30)
        date_label = self.make_dialog_label(outer, "날짜")
        date_label.grid(row=1, column=0, sticky="w", pady=(0, 6))
        date_entry = self.make_dialog_entry(outer)
        date_entry.insert(0, f"{default_time:%Y-%m-%d}")
        date_entry.grid(row=1, column=1, sticky="ew", pady=(0, 6))

        time_label = self.make_dialog_label(outer, "시간")
        time_label.grid(row=2, column=0, sticky="w", pady=(0, 6))
        time_entry = self.make_dialog_entry(outer)
        time_entry.insert(0, f"{default_time:%H:%M}")
        time_entry.grid(row=2, column=1, sticky="ew", pady=(0, 6))

        note_label = self.make_dialog_label(outer, "메모")
        note_label.grid(row=3, column=0, sticky="w", pady=(0, 6))
        note_entry = self.make_dialog_entry(outer)
        note_entry.grid(row=3, column=1, sticky="ew", pady=(0, 6))

        all_day_var = tk.BooleanVar(value=False)
        all_day_check = tk.Checkbutton(
            outer,
            text="종일",
            variable=all_day_var,
            bg=self.theme["background"],
            fg=self.theme["text"],
            selectcolor=self.theme["panel"],
            activebackground=self.theme["background"],
            activeforeground=self.theme["accent"],
            font=(FONT_FAMILY, 10),
            command=lambda: self.sync_all_day_time(all_day_var, time_entry),
        )
        all_day_check.grid(row=4, column=1, sticky="w", pady=(0, 10))

        button_row = tk.Frame(outer, bg=self.theme["background"])
        button_row.grid(row=5, column=0, columnspan=2, sticky="e")

        cancel_button = self.make_dialog_button(button_row, "취소", dialog.destroy)
        cancel_button.pack(side="left", padx=(0, 6))
        save_button = self.make_dialog_button(
            button_row,
            "저장",
            lambda: self.save_dialog_reminder(
                dialog,
                title_entry.get(),
                date_entry.get(),
                time_entry.get(),
                all_day_var.get(),
                note_entry.get(),
            ),
        )
        save_button.pack(side="left")

        outer.columnconfigure(1, weight=1)
        title_entry.focus_set()
        dialog.bind("<Return>", lambda _event: save_button.invoke())
        dialog.bind("<Escape>", lambda _event: dialog.destroy())

        self.position_dialog(dialog)

    def make_dialog_label(self, parent: tk.Widget, text: str) -> tk.Label:
        return tk.Label(
            parent,
            text=text,
            bg=self.theme["background"],
            fg=self.theme["muted"],
            font=(FONT_FAMILY, 10, "bold"),
            anchor="w",
            width=6,
        )

    def make_dialog_entry(self, parent: tk.Widget) -> tk.Entry:
        return tk.Entry(
            parent,
            bg=self.theme["panel"],
            fg=self.theme["text"],
            insertbackground=self.theme["text"],
            relief="flat",
            font=(FONT_FAMILY, 10),
            width=28,
        )

    def make_dialog_button(self, parent: tk.Widget, text: str, command) -> tk.Button:
        return tk.Button(
            parent,
            text=text,
            command=command,
            bd=0,
            relief="flat",
            bg=self.theme["panel_soft"],
            fg=self.theme["text"],
            activebackground=self.theme["today"],
            activeforeground=self.theme["accent"],
            font=(FONT_FAMILY, 10, "bold"),
            padx=12,
            pady=6,
            cursor="hand2",
            takefocus=False,
        )

    def sync_all_day_time(self, all_day_var: tk.BooleanVar, time_entry: tk.Entry) -> None:
        if all_day_var.get():
            time_entry.configure(state="disabled", disabledbackground=self.theme["panel"])
        else:
            time_entry.configure(state="normal")

    def save_dialog_reminder(
        self,
        dialog: tk.Toplevel,
        raw_title: str,
        raw_date: str,
        raw_time: str,
        all_day: bool,
        raw_note: str,
    ) -> None:
        title = clean_text(raw_title)
        if not title:
            messagebox.showwarning("입력 확인", "제목을 입력하세요.", parent=dialog)
            return

        try:
            selected_date = datetime.strptime(raw_date.strip(), "%Y-%m-%d").date()
        except ValueError:
            messagebox.showwarning("입력 확인", "날짜는 YYYY-MM-DD 형식으로 입력하세요.", parent=dialog)
            return

        if all_day or not raw_time.strip():
            start = datetime.combine(selected_date, time.min).replace(tzinfo=self.tz)
            end = start + timedelta(days=1)
            all_day = True
        else:
            try:
                selected_time = datetime.strptime(raw_time.strip(), "%H:%M").time()
            except ValueError:
                messagebox.showwarning("입력 확인", "시간은 HH:MM 형식으로 입력하세요.", parent=dialog)
                return
            start = datetime.combine(selected_date, selected_time).replace(tzinfo=self.tz)
            end = start + timedelta(hours=1)

        reminder = ReminderEvent(
            id=uuid.uuid4().hex,
            source="local",
            title=title,
            start=start,
            end=end,
            all_day=all_day,
            note=clean_text(raw_note),
        )
        self.local_reminders.append(reminder)
        self.local_reminders.sort(key=lambda item: (item.start, item.title.lower()))
        self.persist_local_reminders()
        dialog.destroy()
        self.render()
        self.scroll_to_day(max(reminder.start.date(), self.period_start.date()))

    def persist_local_reminders(self) -> None:
        try:
            save_local_reminders(self.local_reminders)
            self.local_store_error = None
        except OSError as exc:
            self.local_store_error = str(exc)

    def confirm_delete_local_reminder(self, event_id: str) -> None:
        reminder = next((item for item in self.local_reminders if item.id == event_id), None)
        if reminder is None:
            return

        if not messagebox.askyesno(
            "Reminder 삭제",
            f"'{reminder.title}' reminder를 삭제할까요?",
            parent=self.root,
        ):
            return

        self.local_reminders = [item for item in self.local_reminders if item.id != event_id]
        self.persist_local_reminders()
        self.render()

    def position_dialog(self, dialog: tk.Toplevel) -> None:
        dialog.update_idletasks()
        x = self.root.winfo_x() + max(20, (self.root.winfo_width() - dialog.winfo_width()) // 2)
        y = self.root.winfo_y() + 70
        dialog.geometry(f"+{x}+{y}")

    def scroll_to_today(self) -> None:
        self.scroll_to_day(datetime.now(self.tz).date())

    def scroll_to_day(self, day: date) -> None:
        mark = mark_name_for_day(day)
        if mark in self.agenda_text.mark_names():
            self.agenda_text.see(mark)

    def schedule_auto_refresh(self) -> None:
        refresh_minutes = max(1, int(self.config.get("refresh_minutes", 30)))
        self.root.after(refresh_minutes * 60 * 1000, self.auto_refresh)

    def auto_refresh(self) -> None:
        today = datetime.now(self.tz).date()
        if today != self.today:
            self.today = today
            self.period_start = datetime.combine(today, time.min).replace(tzinfo=self.tz)
            self.period_end = self.period_start + timedelta(days=365)
        self.refresh_google_events()
        self.schedule_auto_refresh()

    def schedule_notification_check(self) -> None:
        self.root.after(self.notification_check_seconds * 1000, self.check_event_notifications)

    def check_event_notifications(self) -> None:
        if self.notifications_enabled and self.config_error is None:
            self.send_due_notifications()
        self.schedule_notification_check()

    def send_due_notifications(self) -> None:
        events = self.period_events()
        if not events:
            return

        now = datetime.now(self.tz)
        minutes_before = self.notification_minutes_before
        for event in events:
            if event.all_day and not self.notification_include_all_day:
                continue
            if self.should_mask_event(event):
                continue

            notify_at = event.start - timedelta(minutes=minutes_before)
            if not notify_at <= now < event.start:
                continue

            notification_key = f"{event.source}:{event.id}:{event.start.isoformat()}:{minutes_before}"
            if notification_key in self.sent_notification_keys:
                continue

            if self.show_event_notification(event):
                self.sent_notification_keys.add(notification_key)

        self.prune_sent_notification_keys(now)

    def show_event_notification(self, event: ReminderEvent) -> bool:
        try:
            from winotify import Notification
        except ImportError:
            self.notification_error = "winotify is not installed"
            return False

        source = "앱 reminder" if event.source == "local" else "Google 일정"
        try:
            toast = Notification(
                app_id="Google Calendar Reminder",
                title=source,
                msg=f"{self.display_event_title(event)} 이 {self.notification_minutes_before}분 뒤에 예정되어 있습니다.",
                duration="short",
            )
            toast.show()
        except Exception as exc:
            self.notification_error = str(exc)
            return False

        self.notification_error = None
        return True

    def prune_sent_notification_keys(self, now: datetime) -> None:
        active_keys = {
            f"{event.source}:{event.id}:{event.start.isoformat()}:{self.notification_minutes_before}"
            for event in self.period_events()
            if event.start >= now - timedelta(days=1)
        }
        self.sent_notification_keys.intersection_update(active_keys)

    def start_drag(self, event) -> None:
        self.drag_offset = (event.x_root - self.root.winfo_x(), event.y_root - self.root.winfo_y())

    def drag_window(self, event) -> None:
        if self.drag_offset is None:
            return
        offset_x, offset_y = self.drag_offset
        self.root.geometry(f"+{event.x_root - offset_x}+{event.y_root - offset_y}")

    def save_window_position(self) -> None:
        if self.config_error is not None:
            return

        window_config = self.config.setdefault("window", {})
        window_config["x"] = self.root.winfo_x()
        window_config["y"] = self.root.winfo_y()
        window_config["width"] = self.root.winfo_width()
        window_config["height"] = self.root.winfo_height()
        try:
            save_config(self.config)
        except OSError as exc:
            messagebox.showwarning("저장 실패", f"창 위치를 저장하지 못했습니다.\n{exc}")

    def close(self) -> None:
        self.save_window_position()
        self.root.destroy()


def main() -> None:
    root = tk.Tk()
    ReminderApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
