from flask import Flask, render_template, request, redirect, session
import datetime
import json
import os

app = Flask(__name__)
app.secret_key = "your_secret_key_here"  # セッションのために必要（適当な文字列に変えてください）

members = ["三森", "遠藤", "有賀", "佐藤", "粕谷", "星野", "吉川", "秦左", "内山", "峯村"]
DATA_FILE = "participants.json"

# --- データの保存・読み込み ---
def load_participants():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_participants(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

participants = load_participants()

# --- 今後の活動日を取得（月・火・木） ---
def get_upcoming_activity_dates():
    today = datetime.date.today()
    upcoming = []
    for i in range(7):
        day = today + datetime.timedelta(days=i)
        if day.weekday() in [0, 1, 3]:  # 月:0, 火:1, 木:3
            upcoming.append(day)
    return upcoming

# --- メインページ処理 ---
@app.route("/", methods=["GET", "POST"])
def index():
    upcoming_dates = get_upcoming_activity_dates()

    if request.method == "POST":
        action = request.form.get("action")
        name = request.form.get("name")
        date_str = request.form.get("date")

        if not (name and date_str):
            error_message = "名前と日付を選択してください"
            return render_template(
                "index.html",
                participants=participants,
                members=members,
                upcoming_dates=upcoming_dates,
                error_message=error_message,
                selected_name=name  # セッションに保存する名前
            )

        session["name"] = name  # セッションに名前を保存

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

    selected_name = session.get("name", "")
    return render_template(
        "index.html",
        participants=participants,
        members=members,
        upcoming_dates=upcoming_dates,
        selected_name=selected_name  # セッションから選ばれた名前を渡す
    )

if __name__ == "__main__":
    app.run(debug=True)
