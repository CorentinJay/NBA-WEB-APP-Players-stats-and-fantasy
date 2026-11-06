"""
QUIZZ NBA page — difficulty menu, 10 timed questions, final score out of 100.

Questions live in quiz_questions.json (generated from the Word file).
Scoring: correct answer within 5 s = 10 pts, then -1 pt per extra second
(ceil), 0 pt for a wrong answer or when the 15 s run out.
"""
import html
import json
import math
import random
import re
import time
from pathlib import Path

import pandas as pd
import streamlit as st

QUESTIONS_FILE = Path(__file__).parent / "quiz_questions.json"

NB_QUESTIONS     = 10
TIME_LIMIT       = 15   # seconds per question
FULL_POINTS_TIME = 5    # answer validated within this delay = full points
MAX_POINTS       = 10
FEEDBACK_TIME    = 3    # seconds the correction stays on screen

BLUE = "#1D428A"
RED  = "#C8102E"

LEVELS = {
    "🟢 Facile":    [1],
    "🟡 Moyen":     [2],
    "🔴 Difficile": [3],
    "🎲 Mixte":     [1, 2, 3],
}
LEVEL_NAMES = {1: "🟢 Facile", 2: "🟡 Moyen", 3: "🔴 Difficile"}

# ─────────────────────────────────────────────
# DATA & GAME LOGIC
# ─────────────────────────────────────────────

@st.cache_data
def _load(path: str, mtime: float) -> list[dict]:
    """Cached per file version: pushing a new JSON refreshes the questions."""
    with open(path, encoding="utf-8") as f:
        return json.load(f)["questions"]

def load_questions() -> list[dict]:
    return _load(str(QUESTIONS_FILE), QUESTIONS_FILE.stat().st_mtime)

def points_for(elapsed: float) -> int:
    """Points earned by a correct answer validated after `elapsed` seconds."""
    if elapsed <= FULL_POINTS_TIME:
        return MAX_POINTS
    return max(0, MAX_POINTS - math.ceil(elapsed - FULL_POINTS_TIME))

def ordered_choices(q: dict) -> list[str]:
    """Vrai/Faux in fixed order, numbers sorted ascending, anything else shuffled."""
    choices = [q["bonne_reponse"], *q["mauvaises_reponses"]]
    if q.get("type") == "vrai_faux":
        return sorted(choices, key=lambda c: c != "Vrai")
    if all(re.match(r"\d", c) for c in choices):
        return sorted(choices, key=lambda c: int(re.sub(r"\D", "", c) or 0))
    random.shuffle(choices)
    return choices

def draw_questions(levels: list[int]) -> list[dict]:
    """Pick 10 random questions, avoiding the ones already seen in this session."""
    pool = [q for q in load_questions() if q["difficulte"] in levels]
    seen = st.session_state.setdefault("quiz_seen", set())
    fresh = [q for q in pool if q["id"] not in seen]
    already = [q for q in pool if q["id"] in seen]
    random.shuffle(fresh)
    random.shuffle(already)
    picked = (fresh + already)[:NB_QUESTIONS]
    if len(fresh) < NB_QUESTIONS:  # pool exhausted: start a new cycle
        seen.difference_update(q["id"] for q in pool)
    seen.update(q["id"] for q in picked)
    return [{**q, "choices": ordered_choices(q)} for q in picked]

# ─────────────────────────────────────────────
# STATE TRANSITIONS (button callbacks)
# ─────────────────────────────────────────────

def _quiz() -> dict:
    return st.session_state.setdefault("quiz", {"stage": "menu"})

def _start(level: str):
    st.session_state.quiz = {
        "stage": "question", "level": level, "questions": draw_questions(LEVELS[level]),
        "idx": 0, "results": [], "start": time.time(),
    }

def _record(answer: str | None):
    """Store the result of the current question and show its correction."""
    quiz = _quiz()
    if quiz["stage"] != "question":  # already recorded (double click / timer tick)
        return
    elapsed = time.time() - quiz["start"]
    q = quiz["questions"][quiz["idx"]]
    timed_out = answer is None or elapsed > TIME_LIMIT
    correct = not timed_out and answer == q["bonne_reponse"]
    quiz["results"].append({
        "question": q["question"], "answer": None if timed_out else answer,
        "good": q["bonne_reponse"], "correct": correct,
        "points": points_for(elapsed) if correct else 0,
        "time": min(elapsed, TIME_LIMIT), "timed_out": timed_out,
    })
    quiz["stage"] = "feedback"
    quiz["feedback_start"] = time.time()

def _validate():
    quiz = _quiz()
    _record(st.session_state.get(f"quiz_answer_{quiz['idx']}"))

def _next():
    quiz = _quiz()
    if quiz["stage"] != "feedback":
        return
    quiz["idx"] += 1
    if quiz["idx"] >= len(quiz["questions"]):
        quiz["stage"] = "end"
    else:
        quiz["stage"] = "question"
        quiz["start"] = time.time()

def _back_to_menu():
    st.session_state.quiz = {"stage": "menu"}

# ─────────────────────────────────────────────
# TIMERS (fragments refreshed every second)
# ─────────────────────────────────────────────

@st.fragment(run_every=1)
def _question_timer():
    quiz = _quiz()
    if quiz["stage"] != "question":
        return
    elapsed = time.time() - quiz["start"]
    if elapsed >= TIME_LIMIT:
        _record(None)
        st.rerun()
    remaining = TIME_LIMIT - elapsed
    st.progress(max(0.0, remaining / TIME_LIMIT),
                text=f"⏱️ **{math.ceil(remaining)} s** — 🏀 {points_for(elapsed)} pts en jeu")

@st.fragment(run_every=1)
def _feedback_timer():
    quiz = _quiz()
    if quiz["stage"] != "feedback":
        return
    if time.time() - quiz["feedback_start"] >= FEEDBACK_TIME:
        _next()
        st.rerun()

# ─────────────────────────────────────────────
# SCREENS
# ─────────────────────────────────────────────

def _question_card(i: int, n: int, q: dict):
    st.markdown(
        f"<p style='margin:0;color:#888;font-weight:600;'>Question {i + 1}/{n} · "
        f"{LEVEL_NAMES.get(q['difficulte'], '')}</p>"
        f"<div style='border:2px solid {BLUE};border-radius:12px;padding:18px 22px;margin:10px 0 14px 0;'>"
        f"<p style='font-size:1.3rem;font-weight:700;margin:0;'>{html.escape(q['question'])}</p></div>",
        unsafe_allow_html=True,
    )

def _menu():
    st.title("🧠 Quizz NBA")
    st.markdown(
        f"**{NB_QUESTIONS} questions** tirées au hasard, **{TIME_LIMIT} secondes** par question.  \n"
        f"Bonne réponse validée en moins de {FULL_POINTS_TIME} s : **{MAX_POINTS} points**, "
        f"puis 1 point de moins par seconde. Mauvaise réponse ou temps écoulé : 0 point."
    )
    st.markdown("---")
    st.markdown("### Choisis ta difficulté")
    level = st.radio("Difficulté", list(LEVELS), key="quiz_level", label_visibility="collapsed")
    st.markdown("")
    col, _ = st.columns([1, 2])
    with col:
        st.button("START", key="quiz_start", on_click=_start, args=(level,))

def _question(quiz: dict):
    i, questions = quiz["idx"], quiz["questions"]
    q = questions[i]
    _question_card(i, len(questions), q)
    _question_timer()
    answer = st.radio("Réponse", q["choices"], index=None,
                      key=f"quiz_answer_{i}", label_visibility="collapsed")
    col, _ = st.columns([1, 2])
    with col:
        st.button("VALIDER", key=f"quiz_validate_{i}", on_click=_validate, disabled=answer is None)

def _feedback(quiz: dict):
    i, questions = quiz["idx"], quiz["questions"]
    r = quiz["results"][-1]
    _question_card(i, len(questions), questions[i])
    good = html.escape(r["good"])
    if r["correct"]:
        st.success(f"✅ Bonne réponse ! **+{r['points']} pts** (en {r['time']:.1f} s)")
    elif r["timed_out"]:
        st.warning(f"⏰ Temps écoulé ! La bonne réponse était : **{good}**")
    else:
        st.error(f"❌ Raté ! La bonne réponse était : **{good}**")
    total = sum(x["points"] for x in quiz["results"])
    st.markdown(f"**Score : {total} pts**")
    col, _ = st.columns([1, 2])
    with col:
        last = i + 1 >= len(questions)
        st.button("VOIR MON SCORE ➜" if last else "SUIVANTE ➜", key=f"quiz_next_{i}", on_click=_next)
    _feedback_timer()

def _end(quiz: dict):
    results = quiz["results"]
    total = sum(r["points"] for r in results)
    max_total = MAX_POINTS * len(results)
    nb_good = sum(r["correct"] for r in results)
    ratio = total / max_total if max_total else 0
    verdict = ("🐐 Niveau GOAT !" if ratio >= 0.9 else "🔥 All-Star !" if ratio >= 0.7
               else "💪 Bon rotation player" if ratio >= 0.5 else "🪑 Bout de banc… retente ta chance !")

    st.title("🏁 Fin du quizz")
    st.markdown(
        f"<div style='background:{BLUE};border-radius:12px;padding:28px;text-align:center;margin-bottom:12px;'>"
        f"<p style='color:white;font-size:3.2rem;font-weight:800;margin:0;'>{total} / {max_total}</p>"
        f"<p style='color:white;font-size:1.2rem;margin:6px 0 0 0;'>{nb_good} bonne(s) réponse(s) sur "
        f"{len(results)} · {html.escape(quiz['level'])}</p>"
        f"<p style='color:white;font-size:1.3rem;font-weight:700;margin:8px 0 0 0;'>{verdict}</p></div>",
        unsafe_allow_html=True,
    )
    recap = pd.DataFrame([{
        "": "✅" if r["correct"] else ("⏰" if r["timed_out"] else "❌"),
        "Question": r["question"],
        "Ta réponse": r["answer"] or "—",
        "Bonne réponse": r["good"],
        "Points": r["points"],
    } for r in results])
    st.dataframe(recap, hide_index=True)
    col, _ = st.columns([1, 2])
    with col:
        st.button("OK", key="quiz_ok", on_click=_back_to_menu)

# ─────────────────────────────────────────────
# ENTRY POINT
# ─────────────────────────────────────────────

def render_quiz_page():
    quiz = _quiz()
    stage = quiz["stage"]
    if stage == "question":
        _question(quiz)
    elif stage == "feedback":
        _feedback(quiz)
    elif stage == "end":
        _end(quiz)
    else:
        _menu()
