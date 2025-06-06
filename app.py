from flask import Flask, render_template, request, redirect
import datetime
import json
import os
from collections import OrderedDict

app = Flask(__name__)
members = ["三森", "遠藤", "有賀", "佐藤", "粕谷", "星野", "吉川", "秦左", "内山", "峯村"]
DATA_FILE = "participants.json"
NAME_FILE = "selected_name.json"  # 名前を保存するための新しいファイル

def load_participants():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        today = datetime.date.today().isoformat()
        cleaned_data = {
            date: names for date, names in data.items()
            if date >= today
        }

        if cleaned_data != data:
            save_participants(cleaned_data)

        return cleaned_data
    return {}

def save_participants(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# 名前をファイルから読み込む
def load_selected_name():
    if os.path.exists(NAME_FILE):
        with open(NAME_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get("name", "")
    return ""

# 名前をファイルに保存
def save_selected_name(name):
    data = {"name": name}
    with open(NAME_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

participants = load_participants()

def get_upcoming_activity_dates():
    today = datetime.date.today()
    upcoming = []
    for i in range(7):
        day = today + datetime.timedelta(days=i)
        if day.weekday() in [0, 1, 3]:  # 月火木
            upcoming.append(day)
    return upcoming

@app.route("/", methods=["GET", "POST"])
def index():
    upcoming_dates = get_upcoming_activity_dates()
    selected_name = load_selected_name()  # サーバー側で名前をロード

    if request.method == "POST":
        action = request.form.get("action")
        name = request.form.get("name")
        date_str = request.form.get("date")
        if name:
            save_selected_name(name)  # 名前をサーバー側に保存

        if not (name and date_str):
            error_message = "名前と日付を選択してください"
            sorted_participants = OrderedDict(sorted(participants.items()))
            return render_template(
                "index.html",
                participants=sorted_participants,
                members=members,
                upcoming_dates=upcoming_dates,
                error_message=error_message,
                selected_name=selected_name
            )

        if action == "参加":
            if date_str not in participants:
                participants[date_str] = []
            if name not in participants[date_str]:
                participants[date_str].append(name)
        elif action == "キャンセル":
            if date_str in participants and name in participants[date_str]:
                participants[date_str].remove(name)

        save_participants(participants)
        return redirect("/")

    visible_participants = OrderedDict(
        (k, v) for k, v in sorted(participants.items())
    )

    return render_template(
        "index.html",
        participants=visible_participants,
        members=members,
        upcoming_dates=upcoming_dates,
        selected_name=selected_name
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
