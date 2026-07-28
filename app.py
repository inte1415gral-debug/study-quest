from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from pathlib import Path
app=Flask(__name__); DB=Path("/data/study.db")
def connect():
 DB.parent.mkdir(parents=True,exist_ok=True); con=sqlite3.connect(DB); con.row_factory=sqlite3.Row
 con.execute("CREATE TABLE IF NOT EXISTS records(id INTEGER PRIMARY KEY AUTOINCREMENT,subject TEXT NOT NULL,minutes INTEGER NOT NULL CHECK(minutes>0),done INTEGER NOT NULL DEFAULT 0)")
 return con
@app.get("/")
def index():
 with connect() as con: rows=con.execute("SELECT * FROM records ORDER BY id DESC").fetchall()
 total=sum(r["minutes"] for r in rows)
 # 必要XPはレベルごとに増加: Lv.1→2は60、Lv.2→3は120、以後60ずつ増える
 level=1
 current_level_start=0
 required_for_next=60
 while total >= current_level_start + required_for_next:
  current_level_start += required_for_next
  level += 1
  required_for_next = level * 60
 earned_in_level = total - current_level_start
 progress = min(100, int(earned_in_level / required_for_next * 100))
 minutes_to_next = required_for_next - earned_in_level
 rewards=[
  {"level":2,"icon":"🌱","name":"はじめの一歩"},
  {"level":3,"icon":"🔥","name":"継続の炎"},
  {"level":4,"icon":"📘","name":"学びの探検家"},
  {"level":5,"icon":"🏆","name":"学習マスター"},
  {"level":6,"icon":"⚔️","name":"課題ブレイカー"},
  {"level":8,"icon":"🧠","name":"知識の職人"},
  {"level":10,"icon":"👑","name":"知識の王冠"},
  {"level":12,"icon":"🚀","name":"成長アクセラレーター"},
  {"level":15,"icon":"💎","name":"努力の結晶"},
  {"level":20,"icon":"🌟","name":"学習の達人"},
  {"level":25,"icon":"🐉","name":"知識の守護竜"},
  {"level":30,"icon":"🏅","name":"伝説の学習者"},
  {"level":35,"icon":"🧭","name":"知識の開拓者"},
  {"level":40,"icon":"🛡️","name":"学びの守護者"},
  {"level":45,"icon":"🦅","name":"高みを望む者"},
  {"level":50,"icon":"⚡","name":"限界突破"},
  {"level":55,"icon":"🔮","name":"知識の賢者"},
  {"level":60,"icon":"🌌","name":"銀河の探究者"},
  {"level":65,"icon":"🦁","name":"不屈の学習王"},
  {"level":70,"icon":"☀️","name":"叡智の太陽"},
  {"level":75,"icon":"🪽","name":"天翔ける知性"},
  {"level":80,"icon":"🏰","name":"知識王国の主"},
  {"level":85,"icon":"🌀","name":"真理への到達者"},
  {"level":90,"icon":"🌠","name":"星界の大学者"},
  {"level":95,"icon":"♾️","name":"無限の探究心"},
  {"level":100,"icon":"✨","name":"究極の学習神"}
 ]
 next_reward=next((r for r in rewards if level<r["level"]),None)
 return render_template("index.html",records=rows,total=total,completed=sum(r["done"] for r in rows),level=level,rewards=rewards,next_reward=next_reward,progress=progress,minutes_to_next=minutes_to_next,earned_in_level=earned_in_level,required_for_next=required_for_next)
@app.post("/add")
def add():
 subject=request.form.get("subject","").strip()
 try: minutes=int(request.form.get("minutes","0"))
 except ValueError: minutes=0
 if subject and minutes>0:
  with connect() as con: con.execute("INSERT INTO records(subject,minutes) VALUES(?,?)",(subject,minutes))
 return redirect(url_for("index"))
@app.post("/toggle/<int:i>")
def toggle(i):
 with connect() as con: con.execute("UPDATE records SET done=1-done WHERE id=?",(i,))
 return redirect(url_for("index"))
@app.post("/delete/<int:i>")
def delete(i):
 with connect() as con: con.execute("DELETE FROM records WHERE id=?",(i,))
 return redirect(url_for("index"))
@app.get("/health")
def health(): return {"status":"ok"}
