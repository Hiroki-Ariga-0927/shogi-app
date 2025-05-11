from flask import Flask, render_template, request, redirect
import datetime
import json
import os
from collections import OrderedDict

app = Flask(__name__)
app.secret_key = "your_secret_key_here"

members = ["三森", "遠藤", "有賀", "佐藤", "粕谷", "星野", "吉川", "秦左", "内山", "峯村"]
DATA_FILE = "participants.json"

# --- データの保存・読み込み ---
def load_participants():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        # 今日より過去のデータを削除
        today = datetime.date.today().isoformat()
        cleaned_data = {
            date: names for date, names in data.items()
            if date >= today
        }

        # 更新があれば保存
        if cleaned_data != data:
            save_participants(cleaned_data)

        return cleaned_data

    return {}

def save_participants(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

participants = load_participants()

# --- 今後の活動日（月・火・木） ---
def get_upcoming_activity_dates():
    today = datetime.date.today()
    upcoming = []
    for i in range(7):
        day = today + datetime.timedelta(days=i)
        if day.weekday() in [0, 1, 3]:  # 月:0, 火:1, 木:3
            upcoming.append(day)
    return upcoming

@app.route("/", methods=["GET", "POST"])
def index():
    upcoming_dates = get_upcoming_activity_dates()

    if request.method == "POST":
        action = request.form.get("action")
        name = request.form.get("name")
        date_str = request.form.get("date")

        if not (name and date_str):
            error_message = "名前と日付を選択してください"
            sorted_participants = OrderedDict(
                sorted(participants.items(), key=lambda item: item[0])
            )
            return render_template(
                "index.html",
                participants=sorted_participants,
                members=members,
                upcoming_dates=upcoming_dates,
                error_message=error_message,
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

    sorted_participants = OrderedDict(
        sorted(participants.items(), key=lambda item: item[0])
    )

    return render_template(
        "index.html",
        participants=sorted_participants,
        members=members,
        upcoming_dates=upcoming_dates
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
