import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import random
from datetime import datetime

db = sqlite3.connect("mental_wellness_os.db")
cursor = db.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS moods (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mood TEXT,
    journal TEXT,
    time TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS activity (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    screen_time INTEGER,
    stress INTEGER,
    activity INTEGER,
    time TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS apps (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    app TEXT,
    minutes INTEGER,
    time TEXT
)
""")

db.commit()

dark_mode = True
focus_mode = False
privacy_mode = True
notifications = True
screen_time = 42
stress_level = 28
activity_level = 64
wellness_score = 82
pomodoro_running = False
pomodoro_seconds = 1500
notifications_list = []


root = tk.Tk()
root.title("Mental Wellness-Aware OS")
root.geometry("1250x750")
root.minsize(1050, 650)


bg = "#10141c"
panel = "#171d27"
card_bg = "#1d2531"
text = "#f2f5f8"
muted = "#9ca8b8"
accent = "#63d6b5"
warning = "#f4c95d"
danger = "#ef7777"


style = ttk.Style()
style.theme_use("clam")

style.configure(
    "Treeview",
    background=card_bg,
    foreground=text,
    fieldbackground=card_bg,
    rowheight=34,
    borderwidth=0
)

style.configure(
    "Treeview.Heading",
    background=panel,
    foreground=text,
    font=("Segoe UI", 10, "bold")
)


sidebar = tk.Frame(root, bg=panel, width=240)
sidebar.pack(side="left", fill="y")
sidebar.pack_propagate(False)

main = tk.Frame(root, bg=bg)
main.pack(side="right", fill="both", expand=True)

header = tk.Frame(main, bg=bg, height=75)
header.pack(fill="x")
header.pack_propagate(False)

title = tk.Label(
    header,
    text="🧠  MENTAL WELLNESS OS",
    bg=bg,
    fg=text,
    font=("Segoe UI", 22, "bold")
)
title.pack(side="left", padx=30, pady=20)

system_status = tk.Label(
    header,
    text="● SYSTEM ONLINE",
    bg=bg,
    fg=accent,
    font=("Segoe UI", 10, "bold")
)
system_status.pack(side="right", padx=15)

clock = tk.Label(
    header,
    bg=bg,
    fg=muted,
    font=("Segoe UI", 10)
)
clock.pack(side="right", padx=20)

content = tk.Frame(main, bg=bg)
content.pack(fill="both", expand=True, padx=25, pady=10)


def clear_content():
    for widget in content.winfo_children():
        widget.destroy()


def update_clock():
    clock.config(
        text=datetime.now().strftime("%d %b %Y   %I:%M:%S %p")
    )
    root.after(1000, update_clock)


def show_notification(title_text, message):
    notifications_list.insert(
        0,
        f"{datetime.now().strftime('%H:%M')}  •  {title_text}: {message}"
    )

    if notifications:
        messagebox.showinfo(title_text, message)


def create_card(parent, heading, value, color=accent):
    frame = tk.Frame(
        parent,
        bg=card_bg,
        padx=20,
        pady=15
    )
    frame.pack(
        side="left",
        fill="both",
        expand=True,
        padx=6
    )

    tk.Label(
        frame,
        text=heading,
        bg=card_bg,
        fg=muted,
        font=("Segoe UI", 10)
    ).pack(anchor="w")

    value_label = tk.Label(
        frame,
        text=value,
        bg=card_bg,
        fg=color,
        font=("Segoe UI", 22, "bold")
    )
    value_label.pack(anchor="w", pady=(8, 0))

    return value_label


def dashboard():
    clear_content()

    tk.Label(
        content,
        text="Wellness Dashboard",
        bg=bg,
        fg=text,
        font=("Segoe UI", 24, "bold")
    ).pack(anchor="w")

    tk.Label(
        content,
        text="Real-time overview of your digital wellbeing",
        bg=bg,
        fg=muted,
        font=("Segoe UI", 11)
    ).pack(anchor="w", pady=(2, 20))

    cards = tk.Frame(content, bg=bg)
    cards.pack(fill="x")

    create_card(
        cards,
        "WELLNESS SCORE",
        f"{wellness_score}/100"
    )

    create_card(
        cards,
        "STRESS LEVEL",
        f"{stress_level}%",
        accent if stress_level < 50 else warning
    )

    create_card(
        cards,
        "SCREEN TIME",
        f"{screen_time} min"
    )

    create_card(
        cards,
        "ACTIVITY",
        f"{activity_level}%"
    )

    middle = tk.Frame(content, bg=bg)
    middle.pack(fill="both", expand=True, pady=20)

    left = tk.Frame(
        middle,
        bg=card_bg,
        padx=20,
        pady=20
    )
    left.pack(
        side="left",
        fill="both",
        expand=True,
        padx=(0, 10)
    )

    tk.Label(
        left,
        text="Mental Wellness Core",
        bg=card_bg,
        fg=text,
        font=("Segoe UI", 15, "bold")
    ).pack(anchor="w", pady=(0, 15))

    core_items = [
        "Activity Monitor",
        "Behavior Analyzer",
        "Wellness Engine",
        "Scheduler & Resource Manager",
        "Notification Controller"
    ]

    for item in core_items:
        row = tk.Frame(left, bg=card_bg)
        row.pack(fill="x", pady=7)

        tk.Label(
            row,
            text="●",
            bg=card_bg,
            fg=accent,
            font=("Segoe UI", 10)
        ).pack(side="left")

        tk.Label(
            row,
            text=item,
            bg=card_bg,
            fg=text,
            font=("Segoe UI", 10)
        ).pack(side="left", padx=10)

        tk.Label(
            row,
            text="RUNNING",
            bg=card_bg,
            fg=accent,
            font=("Segoe UI", 9, "bold")
        ).pack(side="right")

    right = tk.Frame(
        middle,
        bg=card_bg,
        padx=20,
        pady=20
    )
    right.pack(
        side="right",
        fill="both",
        expand=True,
        padx=(10, 0)
    )

    tk.Label(
        right,
        text="Wellness Engine",
        bg=card_bg,
        fg=text,
        font=("Segoe UI", 15, "bold")
    ).pack(anchor="w")

    if stress_level >= 70:
        recommendation = "High stress detected. Take a break."
    elif stress_level >= 45:
        recommendation = "Moderate stress. Consider a short break."
    else:
        recommendation = "Your activity currently looks balanced."

    tk.Label(
        right,
        text=recommendation,
        bg=card_bg,
        fg=text,
        wraplength=400,
        justify="left",
        font=("Segoe UI", 12)
    ).pack(anchor="w", pady=20)

    progress = ttk.Progressbar(
        right,
        maximum=100,
        value=wellness_score
    )
    progress.pack(fill="x", pady=10)

    tk.Label(
        right,
        text=f"Daily Wellness Score: {wellness_score}%",
        bg=card_bg,
        fg=muted,
        font=("Segoe UI", 10)
    ).pack(anchor="w")

    bottom = tk.Frame(content, bg=bg)
    bottom.pack(fill="x")

    tk.Button(
        bottom,
        text="🎯  Start Focus Session",
        command=focus_mode,
        bg=accent,
        fg="#0d1715",
        relief="flat",
        padx=18,
        pady=10,
        font=("Segoe UI", 10, "bold")
    ).pack(side="left", padx=5)

    tk.Button(
        bottom,
        text="☕  Take a Break",
        command=break_reminder,
        bg=card_bg,
        fg=text,
        relief="flat",
        padx=18,
        pady=10,
        font=("Segoe UI", 10)
    ).pack(side="left", padx=5)

    tk.Button(
        bottom,
        text="🧘  Relax",
        command=breathing,
        bg=card_bg,
        fg=text,
        relief="flat",
        padx=18,
        pady=10,
        font=("Segoe UI", 10)
    ).pack(side="left", padx=5)


def focus_mode():
    global focus_mode

    if focus_mode:
        focus_mode = False
        show_notification(
            "Focus Mode",
            "Focus Mode has been deactivated."
        )
    else:
        focus_mode = True
        show_notification(
            "Focus Mode",
            "Focus Mode activated. Non-essential distractions are minimized."
        )

    dashboard()


def break_reminder():
    show_notification(
        "Smart Break Reminder",
        "You've been active for a while.\n\n"
        "Take a short break, stretch, rest your eyes and hydrate."
    )


def breathing():
    clear_content()

    tk.Label(
        content,
        text="Mindfulness & Breathing",
        bg=bg,
        fg=text,
        font=("Segoe UI", 24, "bold")
    ).pack(pady=20)

    tk.Label(
        content,
        text="A short guided breathing session",
        bg=bg,
        fg=muted,
        font=("Segoe UI", 11)
    ).pack()

    instruction = tk.Label(
        content,
        text="Ready when you are",
        bg=bg,
        fg=accent,
        font=("Segoe UI", 28, "bold")
    )
    instruction.pack(pady=60)

    timer_label = tk.Label(
        content,
        text="",
        bg=bg,
        fg=muted,
        font=("Segoe UI", 15)
    )
    timer_label.pack()

    def start():
        phases = [
            ("BREATHE IN", 4),
            ("HOLD", 2),
            ("BREATHE OUT", 6)
        ]

        def run(phase=0, cycle=1, remaining=None):

            if cycle > 3:
                instruction.config(
                    text="✓ SESSION COMPLETE"
                )
                timer_label.config(
                    text="Well done. Take a moment to relax."
                )
                return

            if remaining is None:
                remaining = phases[phase][1]

            instruction.config(
                text=phases[phase][0]
            )

            timer_label.config(
                text=f"Cycle {cycle}/3     {remaining}s"
            )

            if remaining > 1:
                root.after(
                    1000,
                    lambda: run(
                        phase,
                        cycle,
                        remaining - 1
                    )
                )
            else:
                next_phase = phase + 1
                next_cycle = cycle

                if next_phase >= len(phases):
                    next_phase = 0
                    next_cycle += 1

                root.after(
                    1000,
                    lambda: run(
                        next_phase,
                        next_cycle
                    )
                )

        run()

    tk.Button(
        content,
        text="START BREATHING",
        command=start,
        bg=accent,
        fg="#0d1715",
        relief="flat",
        padx=30,
        pady=12,
        font=("Segoe UI", 11, "bold")
    ).pack(pady=30)


def mood_tracker():
    clear_content()

    tk.Label(
        content,
        text="Mood Tracker",
        bg=bg,
        fg=text,
        font=("Segoe UI", 24, "bold")
    ).pack(anchor="w")

    tk.Label(
        content,
        text="Record how you're feeling and keep a private journal",
        bg=bg,
        fg=muted,
        font=("Segoe UI", 11)
    ).pack(anchor="w", pady=(2, 25))

    form = tk.Frame(
        content,
        bg=card_bg,
        padx=25,
        pady=25
    )
    form.pack(fill="x")

    tk.Label(
        form,
        text="Current Mood",
        bg=card_bg,
        fg=text,
        font=("Segoe UI", 12, "bold")
    ).pack(anchor="w")

    mood = ttk.Combobox(
        form,
        values=[
            "😊 Excellent",
            "🙂 Good",
            "😐 Okay",
            "😔 Low",
            "😞 Very Low"
        ],
        state="readonly",
        width=30
    )
    mood.current(1)
    mood.pack(anchor="w", pady=10)

    tk.Label(
        form,
        text="Journal Entry",
        bg=card_bg,
        fg=text,
        font=("Segoe UI", 12, "bold")
    ).pack(anchor="w", pady=(15, 5))

    journal = tk.Text(
        form,
        height=7,
        width=70,
        bg="#111722",
        fg=text,
        insertbackground=text,
        relief="flat"
    )
    journal.pack(fill="x")

    def save():

        cursor.execute(
            """
            INSERT INTO moods
            (mood,journal,time)
            VALUES (?,?,?)
            """,
            (
                mood.get(),
                journal.get("1.0", "end").strip(),
                datetime.now().strftime("%Y-%m-%d %H:%M")
            )
        )

        db.commit()

        show_notification(
            "Mood Tracker",
            "Your mood entry has been saved."
        )

        dashboard()

    tk.Button(
        form,
        text="SAVE MOOD",
        command=save,
        bg=accent,
        fg="#0d1715",
        relief="flat",
        padx=25,
        pady=10,
        font=("Segoe UI", 10, "bold")
    ).pack(anchor="w", pady=15)

    history = tk.Frame(
        content,
        bg=bg
    )
    history.pack(fill="both", expand=True, pady=15)

    tk.Label(
        history,
        text="Recent Mood History",
        bg=bg,
        fg=text,
        font=("Segoe UI", 14, "bold")
    ).pack(anchor="w", pady=10)

    table = ttk.Treeview(
        history,
        columns=("mood", "journal", "time"),
        show="headings"
    )

    table.heading("mood", text="Mood")
    table.heading("journal", text="Journal")
    table.heading("time", text="Time")

    table.column("mood", width=180)
    table.column("journal", width=450)
    table.column("time", width=180)

    cursor.execute(
        "SELECT mood,journal,time FROM moods ORDER BY id DESC LIMIT 8"
    )

    for row in cursor.fetchall():
        table.insert("", "end", values=row)

    table.pack(fill="both", expand=True)


def activity_monitor():
    clear_content()

    tk.Label(
        content,
        text="Activity Monitor",
        bg=bg,
        fg=text,
        font=("Segoe UI", 24, "bold")
    ).pack(anchor="w")

    tk.Label(
        content,
        text="Sensor Input Manager",
        bg=bg,
        fg=muted,
        font=("Segoe UI", 11)
    ).pack(anchor="w", pady=(2, 25))

    sensors = [
        ("Keyboard Activity", activity_level),
        ("Mouse Activity", random.randint(30, 85)),
        ("Screen Usage", min(screen_time, 100)),
        ("Heart Rate", random.randint(65, 92))
    ]

    for name, value in sensors:

        frame = tk.Frame(
            content,
            bg=card_bg,
            padx=20,
            pady=15
        )
        frame.pack(fill="x", pady=7)

        tk.Label(
            frame,
            text=name,
            bg=card_bg,
            fg=text,
            font=("Segoe UI", 11)
        ).pack(side="left")

        tk.Label(
            frame,
            text=f"{value}%",
            bg=card_bg,
            fg=accent,
            font=("Segoe UI", 11, "bold")
        ).pack(side="right")

        bar = ttk.Progressbar(
            frame,
            maximum=100,
            value=value,
            length=300
        )
        bar.pack(side="right", padx=25)


def app_usage():
    clear_content()

    tk.Label(
        content,
        text="Application Usage",
        bg=bg,
        fg=text,
        font=("Segoe UI", 24, "bold")
    ).pack(anchor="w")

    tk.Label(
        content,
        text="App Usage Analysis Database",
        bg=bg,
        fg=muted,
        font=("Segoe UI", 11)
    ).pack(anchor="w", pady=(2, 20))

    apps = [
        ("VS Code", 124),
        ("Chrome", 91),
        ("YouTube", 38),
        ("Spotify", 27),
        ("WhatsApp", 19)
    ]

    for app, minutes in apps:

        frame = tk.Frame(
            content,
            bg=card_bg,
            padx=20,
            pady=12
        )
        frame.pack(fill="x", pady=5)

        tk.Label(
            frame,
            text=app,
            bg=card_bg,
            fg=text,
            font=("Segoe UI", 11)
        ).pack(side="left")

        tk.Label(
            frame,
            text=f"{minutes} min",
            bg=card_bg,
            fg=muted,
            font=("Segoe UI", 10)
        ).pack(side="right")

        ttk.Progressbar(
            frame,
            maximum=150,
            value=minutes,
            length=250
        ).pack(side="right", padx=25)


def reports():
    clear_content()

    tk.Label(
        content,
        text="Reports & Insights",
        bg=bg,
        fg=text,
        font=("Segoe UI", 24, "bold")
    ).pack(anchor="w")

    tk.Label(
        content,
        text="Your digital wellness trends",
        bg=bg,
        fg=muted,
        font=("Segoe UI", 11)
    ).pack(anchor="w", pady=(2, 25))

    stats = [
        ("Daily Wellness Score", "82 / 100"),
        ("Average Stress", "36%"),
        ("Screen Time", "4.2 hours"),
        ("Focus Sessions", "8"),
        ("Breaks Taken", "6"),
        ("Mood Trend", "↗ Improving")
    ]

    for name, value in stats:

        frame = tk.Frame(
            content,
            bg=card_bg,
            padx=25,
            pady=17
        )
        frame.pack(fill="x", pady=5)

        tk.Label(
            frame,
            text=name,
            bg=card_bg,
            fg=muted,
            font=("Segoe UI", 11)
        ).pack(side="left")

        tk.Label(
            frame,
            text=value,
            bg=card_bg,
            fg=accent,
            font=("Segoe UI", 12, "bold")
        ).pack(side="right")


def pomodoro():
    global pomodoro_running
    global pomodoro_seconds

    clear_content()

    tk.Label(
        content,
        text="Focus Timer",
        bg=bg,
        fg=text,
        font=("Segoe UI", 24, "bold")
    ).pack(pady=25)

    timer = tk.Label(
        content,
        text="25:00",
        bg=bg,
        fg=accent,
        font=("Segoe UI", 64, "bold")
    )
    timer.pack(pady=40)

    status = tk.Label(
        content,
        text="Ready for a focused session",
        bg=bg,
        fg=muted,
        font=("Segoe UI", 12)
    )
    status.pack()

    def tick():

        global pomodoro_seconds

        if not pomodoro_running:
            return

        minutes = pomodoro_seconds // 60
        seconds = pomodoro_seconds % 60

        timer.config(
            text=f"{minutes:02d}:{seconds:02d}"
        )

        if pomodoro_seconds > 0:

            pomodoro_seconds -= 1

            root.after(
                1000,
                tick
            )

        else:

            pomodoro_running = False

            show_notification(
                "Focus Session",
                "Your focus session is complete. Take a break."
            )

            pomodoro_seconds = 1500

    def start():

        global pomodoro_running

        if not pomodoro_running:

            pomodoro_running = True

            status.config(
                text="Focus session running..."
            )

            tick()

    def stop():

        global pomodoro_running

        pomodoro_running = False

        status.config(
            text="Focus session paused"
        )

    tk.Button(
        content,
        text="START",
        command=start,
        bg=accent,
        fg="#0d1715",
        relief="flat",
        padx=25,
        pady=10,
        font=("Segoe UI", 10, "bold")
    ).pack(side="left", padx=10)

    tk.Button(
        content,
        text="PAUSE",
        command=stop,
        bg=card_bg,
        fg=text,
        relief="flat",
        padx=25,
        pady=10
    ).pack(side="left", padx=10)


def notifications_page():
    clear_content()

    tk.Label(
        content,
        text="Notification Center",
        bg=bg,
        fg=text,
        font=("Segoe UI", 24, "bold")
    ).pack(anchor="w")

    tk.Label(
        content,
        text="Smart notifications from the Wellness Core",
        bg=bg,
        fg=muted,
        font=("Segoe UI", 11)
    ).pack(anchor="w", pady=(2, 25))

    if not notifications_list:

        tk.Label(
            content,
            text="No recent notifications",
            bg=bg,
            fg=muted,
            font=("Segoe UI", 13)
        ).pack(pady=50)

    for item in notifications_list:

        tk.Label(
            content,
            text=item,
            bg=card_bg,
            fg=text,
            anchor="w",
            padx=20,
            pady=12
        ).pack(fill="x", pady=4)


def system_services():
    clear_content()

    tk.Label(
        content,
        text="System Services",
        bg=bg,
        fg=text,
        font=("Segoe UI", 24, "bold")
    ).pack(anchor="w")

    tk.Label(
        content,
        text="OS-level services and Hardware Abstraction Layer",
        bg=bg,
        fg=muted,
        font=("Segoe UI", 11)
    ).pack(anchor="w", pady=(2, 25))

    services = [
        ("Security & Privacy Manager", "ACTIVE"),
        ("Power Manager", "ACTIVE"),
        ("Background Task Manager", "ACTIVE"),
        ("Update Manager", "ACTIVE"),
        ("Backup & Recovery", "ACTIVE"),
        ("Hardware Abstraction Layer", "ACTIVE"),
        ("Database Manager", "ACTIVE"),
        ("Scheduler", "ACTIVE")
    ]

    for service, status in services:

        frame = tk.Frame(
            content,
            bg=card_bg,
            padx=20,
            pady=15
        )
        frame.pack(fill="x", pady=5)

        tk.Label(
            frame,
            text=service,
            bg=card_bg,
            fg=text,
            font=("Segoe UI", 11)
        ).pack(side="left")

        tk.Label(
            frame,
            text="● " + status,
            bg=card_bg,
            fg=accent,
            font=("Segoe UI", 10, "bold")
        ).pack(side="right")


def settings_page():
    clear_content()

    tk.Label(
        content,
        text="System Settings",
        bg=bg,
        fg=text,
        font=("Segoe UI", 24, "bold")
    ).pack(anchor="w")

    tk.Label(
        content,
        text="Configure your Mental Wellness OS",
        bg=bg,
        fg=muted,
        font=("Segoe UI", 11)
    ).pack(anchor="w", pady=(2, 25))

    settings_frame = tk.Frame(
        content,
        bg=card_bg,
        padx=25,
        pady=25
    )
    settings_frame.pack(fill="x")

    focus_var = tk.BooleanVar(value=focus_mode)
    notify_var = tk.BooleanVar(value=notifications)
    privacy_var = tk.BooleanVar(value=privacy_mode)

    tk.Checkbutton(
        settings_frame,
        text="Enable Focus Mode",
        variable=focus_var,
        bg=card_bg,
        fg=text,
        selectcolor=panel,
        activebackground=card_bg,
        activeforeground=text,
        font=("Segoe UI", 11)
    ).pack(anchor="w", pady=8)

    tk.Checkbutton(
        settings_frame,
        text="Smart Notifications",
        variable=notify_var,
        bg=card_bg,
        fg=text,
        selectcolor=panel,
        activebackground=card_bg,
        activeforeground=text,
        font=("Segoe UI", 11)
    ).pack(anchor="w", pady=8)

    tk.Checkbutton(
        settings_frame,
        text="Privacy Protection",
        variable=privacy_var,
        bg=card_bg,
        fg=text,
        selectcolor=panel,
        activebackground=card_bg,
        activeforeground=text,
        font=("Segoe UI", 11)
    ).pack(anchor="w", pady=8)

    def save():

        global focus_mode
        global notifications
        global privacy_mode

        focus_mode = focus_var.get()
        notifications = notify_var.get()
        privacy_mode = privacy_var.get()

        show_notification(
            "System Settings",
            "Settings saved successfully."
        )

    tk.Button(
        settings_frame,
        text="SAVE SETTINGS",
        command=save,
        bg=accent,
        fg="#0d1715",
        relief="flat",
        padx=25,
        pady=10,
        font=("Segoe UI", 10, "bold")
    ).pack(anchor="w", pady=20)


def diagnostics():
    clear_content()

    tk.Label(
        content,
        text="System Diagnostics",
        bg=bg,
        fg=text,
        font=("Segoe UI", 24, "bold")
    ).pack(anchor="w")

    tk.Label(
        content,
        text="Hardware Abstraction Layer",
        bg=bg,
        fg=muted,
        font=("Segoe UI", 11)
    ).pack(anchor="w", pady=(2, 25))

    components = [
        ("CPU", random.randint(20, 70)),
        ("RAM", random.randint(35, 80)),
        ("Storage", random.randint(40, 85)),
        ("Sensors", 100),
        ("Display", 100),
        ("Network", random.randint(60, 100))
    ]

    for name, value in components:

        frame = tk.Frame(
            content,
            bg=card_bg,
            padx=20,
            pady=14
        )
        frame.pack(fill="x", pady=5)

        tk.Label(
            frame,
            text=name,
            bg=card_bg,
            fg=text,
            width=15,
            anchor="w",
            font=("Segoe UI", 11)
        ).pack(side="left")

        ttk.Progressbar(
            frame,
            maximum=100,
            value=value,
            length=400
        ).pack(side="left", padx=20)

        tk.Label(
            frame,
            text=f"{value}%",
            bg=card_bg,
            fg=accent,
            font=("Segoe UI", 10, "bold")
        ).pack(side="right")


def create_button(text_value, command):

    button = tk.Button(
        sidebar,
        text=text_value,
        command=command,
        bg=panel,
        fg=text,
        activebackground=card_bg,
        activeforeground=accent,
        relief="flat",
        borderwidth=0,
        anchor="w",
        padx=22,
        height=2,
        font=("Segoe UI", 10)
    )

    button.pack(
        fill="x",
        pady=2
    )


tk.Label(
    sidebar,
    text="MENTAL\nWELLNESS OS",
    bg=panel,
    fg=accent,
    font=("Segoe UI", 18, "bold"),
    justify="left"
).pack(
    anchor="w",
    padx=22,
    pady=(30, 25)
)

create_button("⌂   Dashboard", dashboard)
create_button("🎯   Focus Mode", focus_mode)
create_button("⏱   Focus Timer", pomodoro)
create_button("☕   Break Reminder", break_reminder)
create_button("🧘   Mindfulness", breathing)
create_button("😊   Mood Tracker", mood_tracker)
create_button("📊   Activity Monitor", activity_monitor)
create_button("📱   App Usage", app_usage)
create_button("📈   Reports & Insights", reports)
create_button("🔔   Notifications", notifications_page)
create_button("⚙   System Services", system_services)
create_button("🩺   Diagnostics", diagnostics)
create_button("🔧   Settings", settings_page)

tk.Label(
    sidebar,
    text="MENTAL WELLNESS CORE\n● RUNNING",
    bg=panel,
    fg=accent,
    font=("Segoe UI", 9, "bold"),
    justify="left"
).pack(
    side="bottom",
    anchor="w",
    padx=22,
    pady=25
)

update_clock()
dashboard()

root.mainloop()