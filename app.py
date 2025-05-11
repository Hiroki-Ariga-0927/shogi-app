import os
from flask import Flask, render_template, request, redirect
import datetime

app = Flask(__name__)

members = ["三森", "遠藤", "有賀", "佐藤", "粕谷","星野","吉川","秦左","内山","峯村"]  # 選択肢に出すメンバー
participants = {}

def get_upcoming_activity_dates():
    today = datetime.date.today()
    upcoming = []
    for i in range(7):
        day = today + datetime.timedelta(days=i)
        if day.weekday() in [0, 1, 3]:
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
            return render_template("index.html", participants=participants, members=members, upcoming_dates=upcoming_dates, error_message=error_message)

        if action == "参加":
            if date_str not in participants:
                participants[date_str] = []
            if name not in participants[date_str]:
                participants[date_str].append(name)
        elif action == "キャンセル":
            if date_str in participants and name in participants[date_str]:
                participants[date_str].remove(name)

        return redirect("/")

    return render_template("index.html", participants=participants, members=members, upcoming_dates=upcoming_dates)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Renderの環境変数PORTを使ってポート番号を設定
    app.run(host="0.0.0.0", port=port, debug=True)  # ポート番号を指定してFlaskを起動
