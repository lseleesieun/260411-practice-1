from __future__ import annotations

import random
from pathlib import Path
from typing import Any

import streamlit as st
import streamlit.components.v1 as components


st.set_page_config(
    page_title="분수 피자 연구소",
    page_icon="🍕",
    layout="centered",
)

_pizza_picker = components.declare_component(
    "pizza_picker",
    path=str(Path(__file__).parent / "components" / "pizza_picker"),
)


st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Jua&family=Noto+Sans+KR:wght@400;600;700;800&display=swap');
    :root { --tomato: #df6738; --cheese: #ffc94d; --cream: #fff8e9; --ink: #59351e; }
    .stApp { background: linear-gradient(180deg, #fff7e7 0%, #fffdf8 42%, #fff8eb 100%); color: var(--ink); }
    html, body, [class*="css"] { font-family: 'Noto Sans KR', sans-serif; }
    h1, h2, h3 { color: #743d1f; font-family: 'Jua', 'Noto Sans KR', sans-serif; }
    h1 { font-size: 2.45rem !important; }
    .hero { border: 3px solid #ffd56c; border-radius: 26px; padding: 1.4rem 1.5rem;
            background: linear-gradient(135deg, #fff0bf, #fffaf0); text-align: center; }
    .hero-title { color: #9c431f; font: 2.35rem 'Jua', sans-serif; margin: .15rem 0; }
    .hero-subtitle { color: #dc7136; font: 1.4rem 'Jua', sans-serif; }
    .speech { background: #fff1c9; border: 2px solid #ffd878; border-radius: 20px;
              padding: 1rem 1.2rem; color: #57371f; font-size: 1.15rem; }
    .tip { background: #fff8e9; border-left: 6px solid #f3a43b; border-radius: 10px;
           padding: .8rem 1rem; font-size: 1rem; }
    .stButton > button { border-radius: 14px; min-height: 3rem; font-size: 1rem; font-weight: 700;
                         border: 2px solid #f2b84b; color: #673d20; background: #fffdf7; }
    .stButton > button:hover { border-color: #df6738; color: #a34220; background: #fff1cc; }
    [data-testid="stMetric"] { background: #fffaf0; border: 2px solid #ffe2a0; border-radius: 16px; padding: .8rem; }
    div[data-testid="stProgress"] > div > div { background-color: #ef9b36; }
    .small-note { color: #795b43; font-size: .95rem; }
    </style>
    """,
    unsafe_allow_html=True,
)


ACTIVITIES = [
    ("🍕", "피자 나누기", "조각을 눌러 분수를 만들어 봐요!", "split"),
    ("⚖️", "분수 비교하기", "두 피자 중 더 큰 분수를 찾아요!", "compare"),
    ("🧑‍🍳", "손님 주문 만들기", "손님이 원하는 피자를 만들어 줘요!", "orders"),
    ("🏆", "분수 미션 도전하기", "열 가지 미션에 도전해요!", "mission"),
]

MISSION_QUESTIONS: list[dict[str, Any]] = [
    {"kind": "make", "denominator": 4, "numerator": 2, "hint": "4조각 중 2조각을 골라 보세요."},
    {"kind": "compare", "left": (3, 4), "right": (1, 4), "answer": "A", "hint": "같은 크기의 4조각이에요. 색칠된 조각 수를 세어 보세요."},
    {"kind": "picture", "numerator": 5, "denominator": 8, "answer": "5/8", "hint": "전체 조각 수가 분모, 색칠된 조각 수가 분자예요."},
    {"kind": "choice", "prompt": "분모가 4인 분수 중 2/4보다 큰 분수는 무엇일까요?", "options": ["1/4", "2/4", "3/4"], "answer": "3/4", "hint": "4조각 중 2조각보다 더 많이 색칠된 분수를 찾아요."},
    {"kind": "make", "denominator": 2, "numerator": 1, "hint": "2조각 중 1조각을 골라 보세요."},
    {"kind": "compare", "left": (2, 8), "right": (6, 8), "answer": "B", "hint": "두 피자의 조각 크기는 같아요. 색칠된 조각 수를 비교해요."},
    {"kind": "picture", "numerator": 1, "denominator": 4, "answer": "1/4", "hint": "4조각 중 몇 조각이 색칠되었나요?"},
    {"kind": "choice", "prompt": "피자를 8조각으로 나누고 3조각을 골랐어요. 알맞은 분수는 무엇일까요?", "options": ["3/8", "8/3", "3/3"], "answer": "3/8", "hint": "분모는 전체 8조각, 분자는 고른 3조각이에요."},
    {"kind": "make", "denominator": 8, "numerator": 3, "hint": "8조각 중 3조각을 골라 보세요."},
    {"kind": "compare", "left": (2, 4), "right": (1, 4), "answer": "A", "hint": "분모가 같을 때는 분자가 큰 분수가 더 커요."},
]


def grade_for_stars(stars: int) -> str:
    if stars <= 2:
        return "연습 중인 셰프"
    if stars <= 5:
        return "꼬마 셰프"
    if stars <= 8:
        return "실력 있는 셰프"
    return "분수 마스터"


def init_game() -> None:
    defaults: dict[str, Any] = {
        "stars": 0,
        "started": False,
        "page": "home",
        "completed": [],
        "split_awarded": False,
        "split_round": 0,
        "compare_round": 0,
        "compare_correct": 0,
        "compare_question": None,
        "compare_answered": False,
        "compare_feedback": None,
        "orders_completed": 0,
        "order_round": 0,
        "order_prompt": None,
        "order_feedback": None,
        "mission_index": 0,
        "mission_score": 0,
        "mission_solved": [],
        "mission_feedback": None,
        "mission_questions": random.sample(MISSION_QUESTIONS, len(MISSION_QUESTIONS)),
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def award_stars(count: int) -> None:
    st.session_state.stars += count


def mark_complete(activity: str) -> None:
    if activity not in st.session_state.completed:
        st.session_state.completed.append(activity)


def picker_selection(
    component_key: str,
    state_key: str,
    denominator: int,
    *,
    selected: list[int] | None = None,
    disabled: bool = False,
) -> list[int]:
    saved = st.session_state.get(state_key, []) if selected is None else selected
    result = _pizza_picker(
        denominator=denominator,
        selected=saved,
        disabled=disabled,
        key=component_key,
        default=saved,
    )
    if result is not None:
        valid = sorted({int(item) for item in result if 0 <= int(item) < denominator})
        st.session_state[state_key] = valid
        return valid
    return saved


def new_compare_question() -> None:
    denominator = random.choice([2, 4, 8])
    first, second = random.sample(range(1, denominator + 1), 2)
    st.session_state.compare_question = {
        "denominator": denominator,
        "left": first,
        "right": second,
    }
    st.session_state.compare_answered = False


def new_order() -> None:
    denominator = random.choice([2, 4, 8])
    numerator = random.randint(1, denominator)
    st.session_state.order_prompt = (numerator, denominator)
    st.session_state.order_round += 1


def start_game() -> None:
    st.session_state.started = True
    st.session_state.page = "menu"


def go_to(page: str) -> None:
    st.session_state.page = page


def reset_game() -> None:
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    init_game()


def show_top_status() -> None:
    stars, grade = st.columns(2)
    stars.metric("⭐ 나의 별", f"{st.session_state.stars}개")
    grade.metric("👩‍🍳 현재 셰프 등급", grade_for_stars(st.session_state.stars))


def show_header() -> None:
    st.markdown(
        '<div class="hero"><div style="font-size:3rem">🍕 🍅 🧀 🍕</div>'
        '<div class="hero-title">분수 피자 연구소</div>'
        '<div class="hero-subtitle">꼬마 피자 셰프의 주문 대작전!</div></div>',
        unsafe_allow_html=True,
    )


def show_menu() -> None:
    st.subheader("오늘은 어떤 활동을 해 볼까요?")
    for start in range(0, len(ACTIVITIES), 2):
        columns = st.columns(2)
        for column, (emoji, name, description, page) in zip(columns, ACTIVITIES[start:start + 2]):
            with column:
                st.markdown(f"### {emoji} {name}")
                st.write(description)
                if st.button(f"{name} 시작하기", key=f"menu_{page}", use_container_width=True):
                    go_to(page)
                    st.rerun()
    if len(st.session_state.completed) == len(ACTIVITIES):
        st.success("모든 활동을 마쳤어요! 결과를 확인해 보세요.")
        if st.button("🎉 학습 결과 보기", use_container_width=True):
            go_to("results")
            st.rerun()


def show_split_activity() -> None:
    st.header("🍕 피자 나누기")
    st.write("피자를 똑같은 크기의 조각으로 나누고, 먹고 싶은 조각을 눌러 보세요.")
    denominator = st.selectbox("피자를 몇 조각으로 나눌까요?", [2, 4, 8], key="split_denominator")
    state_key = f"split_selection_{denominator}_{st.session_state.split_round}"
    selected = picker_selection(
        f"split_picker_{denominator}_{st.session_state.split_round}",
        state_key,
        denominator,
    )
    st.info(f"선택한 조각: **{len(selected)}개** / 전체 조각: **{denominator}개** 　➡️　현재 분수: **{len(selected)}/{denominator}**")
    st.markdown(
        '<div class="tip"><b>분모</b>는 피자를 똑같이 나눈 전체 조각 수, '
        '<b>분자</b>는 그중에서 선택한 조각 수예요.</div>',
        unsafe_allow_html=True,
    )
    if not st.session_state.split_awarded and st.button("연습 완료하고 별 받기 ⭐", use_container_width=True):
        award_stars(1)
        st.session_state.split_awarded = True
        mark_complete("split")
        st.success("잘했어요! 피자를 똑같이 나누는 연습을 마쳤어요. 별 1개를 받았어요!")
        st.rerun()
    elif st.session_state.split_awarded:
        st.success("피자 나누기 활동을 완료했어요! 별 1개를 받았어요.")


def show_compare_activity() -> None:
    st.header("⚖️ 분수 비교하기")
    st.write("두 피자에서 색칠된 조각 수를 비교해 더 큰 분수를 찾아요.")
    if st.session_state.compare_question is None:
        new_compare_question()
    question = st.session_state.compare_question
    denominator = question["denominator"]
    left, right = st.columns(2)
    with left:
        st.subheader(f"A 피자: {question['left']}/{denominator}")
        picker_selection(
            f"compare_A_{st.session_state.compare_round}",
            f"compare_A_state_{st.session_state.compare_round}",
            denominator,
            selected=list(range(question["left"])),
            disabled=True,
        )
    with right:
        st.subheader(f"B 피자: {question['right']}/{denominator}")
        picker_selection(
            f"compare_B_{st.session_state.compare_round}",
            f"compare_B_state_{st.session_state.compare_round}",
            denominator,
            selected=list(range(question["right"])),
            disabled=True,
        )
    choice_columns = st.columns(2)
    for column, answer in zip(choice_columns, ["A", "B"]):
        with column:
            if st.button(f"{answer} 피자가 더 커요", key=f"compare_choice_{answer}_{st.session_state.compare_round}", disabled=st.session_state.compare_answered):
                correct = "A" if question["left"] > question["right"] else "B"
                if answer == correct:
                    award_stars(1)
                    st.session_state.compare_correct += 1
                    st.session_state.compare_answered = True
                    st.session_state.compare_feedback = (
                        f"정답이에요! {question['left']}/{denominator}와 "
                        f"{question['right']}/{denominator}는 조각 크기가 같고, "
                        "더 많은 조각을 가진 분수가 더 커요. 별 1개를 받았어요!"
                    )
                    if st.session_state.compare_correct >= 3:
                        mark_complete("compare")
                    st.rerun()
                else:
                    st.warning("아직 정답이 아니에요. 피자의 색칠된 조각을 다시 세어 보세요!")
    if st.session_state.compare_answered:
        st.success(st.session_state.compare_feedback)
        st.caption(f"지금까지 맞힌 문제: {st.session_state.compare_correct}개")
        if st.button("다음 비교 문제", use_container_width=True):
            st.session_state.compare_round += 1
            new_compare_question()
            st.session_state.compare_feedback = None
            st.rerun()
    if "compare" in st.session_state.completed:
        st.success("비교 문제 3개를 맞혀 활동을 완료했어요!")
    else:
        st.caption(f"활동 완료까지 {max(0, 3 - st.session_state.compare_correct)}문제 남았어요.")


def show_orders_activity() -> None:
    st.header("🧑‍🍳 손님 주문 만들기")
    st.write("손님의 주문대로 피자를 나누고 조각을 골라 주세요. 주문 3개를 해결하면 활동이 끝나요.")
    if st.session_state.order_prompt is None:
        new_order()
    numerator, requested_denominator = st.session_state.order_prompt
    if st.session_state.order_feedback:
        st.success(st.session_state.order_feedback)
    st.markdown(
        f'<div class="speech">🐻 손님 곰돌이<br><br>“안녕하세요! 피자를 '
        f'<b>{requested_denominator}조각</b>으로 똑같이 나눠서 '
        f'<b>{numerator}조각</b>만 주세요!”</div>',
        unsafe_allow_html=True,
    )
    denominator = st.selectbox(
        "피자를 몇 조각으로 나눌까요?",
        [2, 4, 8],
        index=[2, 4, 8].index(requested_denominator),
        key=f"order_denominator_{st.session_state.order_round}",
    )
    state_key = f"order_selection_{st.session_state.order_round}_{denominator}"
    selected = picker_selection(
        f"order_picker_{st.session_state.order_round}_{denominator}",
        state_key,
        denominator,
    )
    st.info(f"고른 조각: **{len(selected)}개** / 전체 조각: **{denominator}개**")
    if st.button("주문 완료!", type="primary", use_container_width=True):
        if denominator == requested_denominator and len(selected) == numerator:
            award_stars(2)
            st.session_state.orders_completed += 1
            if st.session_state.orders_completed >= 3:
                mark_complete("orders")
            st.session_state.order_feedback = (
                f"주문 성공! 손님이 맛있게 먹었어요. 별 2개를 받았어요! "
                f"(해결한 주문 {st.session_state.orders_completed}개)"
            )
            st.session_state.order_prompt = None
            st.rerun()
        else:
            st.error("주문과 달라요. 손님의 말을 다시 읽고 피자 조각을 골라 주세요!")
    if "orders" in st.session_state.completed:
        st.success("손님 주문 3개를 해결해 활동을 완료했어요!")
    else:
        st.caption(f"활동 완료까지 {max(0, 3 - st.session_state.orders_completed)}개 주문 남았어요.")


def show_mission_question(question_index: int, question: dict[str, Any]) -> None:
    kind = question["kind"]
    submitted_answer: str | None = None
    selected_answer: str | None = None
    if kind == "make":
        denominator = question["denominator"]
        st.write(f"피자를 **{denominator}등분**하고 **{question['numerator']}조각**을 선택하세요.")
        selected = picker_selection(
            f"mission_picker_{question_index}_{denominator}",
            f"mission_selection_{question_index}_{denominator}",
            denominator,
        )
        st.info(f"선택한 분수: **{len(selected)}/{denominator}**")
        if st.button("정답 확인", key=f"mission_check_{question_index}"):
            submitted_answer = "맞음" if len(selected) == question["numerator"] else "틀림"
    elif kind == "compare":
        denominator = question["left"][1]
        left, right = st.columns(2)
        with left:
            st.subheader(f"A: {question['left'][0]}/{denominator}")
            picker_selection(
                f"mission_compare_A_{question_index}",
                f"mission_compare_A_state_{question_index}",
                denominator,
                selected=list(range(question["left"][0])),
                disabled=True,
            )
        with right:
            st.subheader(f"B: {question['right'][0]}/{denominator}")
            picker_selection(
                f"mission_compare_B_{question_index}",
                f"mission_compare_B_state_{question_index}",
                denominator,
                selected=list(range(question["right"][0])),
                disabled=True,
            )
        selected_answer = st.radio(
            "더 큰 피자를 골라요.",
            ["A", "B"],
            horizontal=True,
            key=f"mission_compare_answer_{question_index}",
        )
        if st.button("정답 확인", key=f"mission_check_{question_index}"):
            if selected_answer == question["answer"]:
                submitted_answer = "맞음"
            else:
                submitted_answer = "틀림"
    elif kind == "picture":
        st.write("색칠된 피자를 보고 알맞은 분수를 골라요.")
        picker_selection(
            f"mission_picture_{question_index}",
            f"mission_picture_state_{question_index}",
            question["denominator"],
            selected=list(range(question["numerator"])),
            disabled=True,
        )
        options = [f"{question['numerator']}/{question['denominator']}", f"1/{question['denominator']}", f"{question['denominator']}/{question['denominator']}"]
        options = list(dict.fromkeys(options))
        selected_answer = st.radio("이 피자를 나타내는 분수는?", options, horizontal=True, key=f"mission_picture_answer_{question_index}")
        if st.button("정답 확인", key=f"mission_check_{question_index}"):
            submitted_answer = "맞음" if selected_answer == question["answer"] else "틀림"
    else:
        st.write(question["prompt"])
        selected_answer = st.radio("정답을 골라요.", question["options"], horizontal=True, key=f"mission_choice_{question_index}")
        if st.button("정답 확인", key=f"mission_check_{question_index}"):
            submitted_answer = "맞음" if selected_answer == question["answer"] else "틀림"

    if submitted_answer is not None:
        if submitted_answer == "맞음":
            st.session_state.mission_feedback = {"index": question_index, "correct": True}
            if question_index not in st.session_state.mission_solved:
                st.session_state.mission_solved.append(question_index)
                st.session_state.mission_score += 1
                award_stars(1)
            if question_index == len(st.session_state.mission_questions) - 1:
                mark_complete("mission")
        else:
            st.session_state.mission_feedback = {"index": question_index, "correct": False}

    feedback = st.session_state.mission_feedback
    if feedback and feedback["index"] == question_index:
        if feedback["correct"]:
            st.success("정답이에요! 별 1개를 받았어요. ⭐")
            if st.button("다음 미션", key=f"mission_next_{question_index}", use_container_width=True):
                st.session_state.mission_index += 1
                st.session_state.mission_feedback = None
                st.rerun()
        else:
            st.warning(f"힌트: {question['hint']}")
            retry, skip = st.columns(2)
            with retry:
                if st.button("다시 풀어 보기", key=f"mission_retry_{question_index}"):
                    st.session_state.mission_feedback = None
                    st.rerun()
            with skip:
                if st.button("힌트 보고 다음 미션", key=f"mission_skip_{question_index}"):
                    st.session_state.mission_index += 1
                    st.session_state.mission_feedback = None
                    st.rerun()


def show_mission_activity() -> None:
    st.header("🏆 분수 미션 도전하기")
    total = len(st.session_state.mission_questions)
    index = st.session_state.mission_index
    if index >= total:
        mark_complete("mission")
        st.success("미션 10개를 모두 풀었어요!")
        st.metric("미션 정답 개수", f"{st.session_state.mission_score} / {total}")
        st.metric("정답률", f"{st.session_state.mission_score * 10}%")
        st.info(f"현재 셰프 등급: **{grade_for_stars(st.session_state.stars)}**")
        return
    st.progress(index / total, text=f"미션 {index + 1} / {total}")
    show_mission_question(index, st.session_state.mission_questions[index])
    if index == total - 1 and st.session_state.mission_feedback and st.session_state.mission_feedback.get("correct"):
        st.caption("마지막 미션을 마쳤어요. 다음 미션을 누르면 최종 결과를 확인할 수 있어요.")


def show_results() -> None:
    st.header("🎉 학습 결과")
    st.write("분수 피자 연구소에서 멋진 셰프가 되었어요!")
    columns = st.columns(3)
    columns[0].metric("⭐ 획득한 별", f"{st.session_state.stars}개")
    columns[1].metric("🧑‍🍳 해결한 주문", f"{st.session_state.orders_completed}개")
    columns[2].metric("🏆 미션 정답", f"{st.session_state.mission_score} / 10")
    st.metric("미션 정답률", f"{st.session_state.mission_score * 10}%")
    st.subheader(f"최종 셰프 등급: {grade_for_stars(st.session_state.stars)}")
    st.markdown(
        '<div class="tip"><b>오늘 배운 분수 개념</b><br>'
        '• 분모는 똑같이 나눈 전체 조각 수예요.<br>'
        '• 분자는 그중에서 선택하거나 색칠한 조각 수예요.<br>'
        '• 분모가 같은 분수는 분자가 클수록 더 커요.</div>',
        unsafe_allow_html=True,
    )
    st.write(f"완료한 활동: {len(st.session_state.completed)} / 4")
    if st.button("🔁 다시 도전하기", type="primary", use_container_width=True):
        reset_game()
        st.rerun()


init_game()
show_header()
show_top_status()

if not st.session_state.started:
    st.markdown(
        '<div class="speech">어서 오세요, 꼬마 셰프! 🍕<br>'
        '피자를 똑같이 나누고, 분수를 비교하고, 손님의 주문을 해결해 보세요.<br>'
        '활동을 하며 별을 모으면 셰프 등급이 올라가요!</div>',
        unsafe_allow_html=True,
    )
    st.write("")
    if st.button("🚀 게임 시작!", type="primary", use_container_width=True):
        start_game()
        st.rerun()
else:
    page = st.session_state.page
    if page == "menu":
        show_menu()
    elif page == "split":
        if st.button("⬅️ 활동 메뉴로"):
            go_to("menu")
            st.rerun()
        show_split_activity()
    elif page == "compare":
        if st.button("⬅️ 활동 메뉴로"):
            go_to("menu")
            st.rerun()
        show_compare_activity()
    elif page == "orders":
        if st.button("⬅️ 활동 메뉴로"):
            go_to("menu")
            st.rerun()
        show_orders_activity()
    elif page == "mission":
        if st.button("⬅️ 활동 메뉴로"):
            go_to("menu")
            st.rerun()
        show_mission_activity()
    elif page == "results":
        show_results()
        if st.button("⬅️ 활동 메뉴로"):
            go_to("menu")
            st.rerun()
