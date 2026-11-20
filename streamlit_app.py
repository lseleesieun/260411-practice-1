from __future__ import annotations

import random
import time
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components


GAME_SECONDS = 60
PIZZA_DENOMINATORS = (2, 3, 4, 5, 6, 8)

st.set_page_config(page_title="분수 피자 연구소", page_icon="🍕", layout="centered")

pizza_picker = components.declare_component(
    "pizza_picker",
    path=str(Path(__file__).parent / "components" / "pizza_picker"),
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Jua&family=Noto+Sans+KR:wght@400;600;700;800&display=swap');
    .stApp { background: linear-gradient(180deg, #fff5dc, #fffdf8 48%, #fff8eb); color: #59351e; }
    html, body, [class*="css"] { font-family: 'Noto Sans KR', sans-serif; }
    h1, h2, h3 { color: #743d1f; font-family: 'Jua', 'Noto Sans KR', sans-serif; }
    .hero { border: 3px solid #ffd56c; border-radius: 26px; padding: 1.2rem;
            background: linear-gradient(135deg, #fff0bf, #fffaf0); text-align: center; }
    .hero-title { color: #9c431f; font: 2.3rem 'Jua', sans-serif; }
    .hero-subtitle { color: #dc7136; font: 1.35rem 'Jua', sans-serif; }
    .speech { background: #fff1c9; border: 2px solid #ffd878; border-radius: 20px;
              padding: 1rem 1.2rem; color: #57371f; font-size: 1.3rem; text-align: center; }
    .stButton > button { border-radius: 14px; min-height: 3rem; font-size: 1.05rem; font-weight: 800;
                         border: 2px solid #f2b84b; color: #673d20; background: #fffdf7; }
    .stButton > button:hover { border-color: #df6738; color: #a34220; background: #fff1cc; }
    [data-testid="stMetric"] { background: #fffaf0; border: 2px solid #ffe2a0; border-radius: 16px; padding: .8rem; }
    div[data-testid="stProgress"] > div > div { background-color: #ef9b36; }
    </style>
    """,
    unsafe_allow_html=True,
)


def new_order() -> tuple[int, int]:
    denominator = random.choice(PIZZA_DENOMINATORS)
    return random.randint(1, denominator), denominator


def grade_for_stars(stars: int) -> str:
    if stars <= 2:
        return "연습 중인 셰프"
    if stars <= 5:
        return "꼬마 셰프"
    if stars <= 8:
        return "실력 있는 셰프"
    return "분수 마스터"


def initialize_state() -> None:
    defaults = {
        "game_started": False,
        "game_over": False,
        "game_started_at": None,
        "orders_completed": 0,
        "stars": 0,
        "current_order": new_order(),
        "selected_slices": [],
        "order_feedback": None,
        "celebration": 0,
        "game_id": time.time_ns(),
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def render_header() -> None:
    st.markdown(
        '<div class="hero"><div style="font-size:3rem">🍕 🍅 🧀 🍕</div>'
        '<div class="hero-title">분수 피자 연구소</div>'
        '<div class="hero-subtitle">꼬마 피자 셰프의 주문 대작전!</div></div>',
        unsafe_allow_html=True,
    )


def render_home() -> None:
    st.markdown(
        '<div class="speech">어서 오세요, 꼬마 셰프! 🐻<br>'
        '손님이 원하는 분수만큼 피자를 만들어 주세요.<br>'
        f'<b>{GAME_SECONDS}초</b> 동안 주문을 많이 해결할수록 높은 점수를 얻어요!</div>',
        unsafe_allow_html=True,
    )
    st.write("")
    if st.button("🚀 주문 받기 시작!", type="primary", use_container_width=True):
        st.session_state.game_started = True
        st.session_state.game_started_at = time.time()
        st.rerun()


@st.fragment(run_every=1)
def render_live_game() -> None:
    elapsed = time.time() - st.session_state.game_started_at
    remaining = max(0, GAME_SECONDS - int(elapsed))
    if remaining == 0:
        st.session_state.game_over = True
        st.rerun(scope="app")

    time_col, order_col, star_col = st.columns(3)
    time_col.metric("⏱️ 남은 시간", f"{remaining}초")
    order_col.metric("📦 해결한 주문", f"{st.session_state.orders_completed}개")
    star_col.metric("⭐ 모은 별", f"{st.session_state.stars}개")
    st.progress(remaining / GAME_SECONDS, text="시간 안에 주문을 많이 해결해요!")

    numerator, denominator = st.session_state.current_order
    st.markdown(
        f'<div class="speech">🐻 손님: “<b>{numerator}/{denominator} 조각</b> 주세요!”</div>',
        unsafe_allow_html=True,
    )
    st.caption(f"피자를 {denominator}조각으로 나눴어요. 주문에 맞게 {numerator}조각을 눌러 주세요!")

    selected = pizza_picker(
        denominator=denominator,
        selected=st.session_state.selected_slices,
        disabled=False,
        celebration=st.session_state.celebration,
        key=f"order_pizza_{st.session_state.game_id}_{st.session_state.orders_completed}",
        default=[],
    )
    if selected is not None:
        st.session_state.selected_slices = sorted(
            {int(index) for index in selected if 0 <= int(index) < denominator}
        )

    st.info(f"선택한 조각: **{len(st.session_state.selected_slices)}개** 　·　주문 분수: **{numerator}/{denominator}**")
    if st.session_state.order_feedback:
        if st.session_state.order_feedback["correct"]:
            st.success(st.session_state.order_feedback["message"])
        else:
            st.warning(st.session_state.order_feedback["message"])

    if st.button("🍕 주문 완성!", type="primary", use_container_width=True):
        if len(st.session_state.selected_slices) == numerator:
            st.session_state.orders_completed += 1
            st.session_state.stars += 2
            st.session_state.current_order = new_order()
            st.session_state.selected_slices = []
            st.session_state.celebration += 1
            st.session_state.order_feedback = {
                "correct": True,
                "message": f"딩동댕! 주문 성공! 별 2개를 받았어요! ⭐ (총 {st.session_state.orders_completed}개 주문)",
            }
            st.balloons()
        else:
            st.session_state.order_feedback = {
                "correct": False,
                "message": "앗, 조각 수가 달라요! 주문을 다시 보고 조각을 골라 주세요.",
            }
        st.rerun()


def render_results() -> None:
    stars = st.session_state.stars
    st.balloons()
    st.header("🎉 오늘의 피자 연구 결과")
    st.write("시간 안에 멋지게 주문을 해결했어요!")
    orders, total_stars = st.columns(2)
    orders.metric("🍕 해결한 주문", f"{st.session_state.orders_completed}개")
    total_stars.metric("⭐ 획득한 별", f"{stars}개")
    st.subheader(f"최종 셰프 등급: {grade_for_stars(stars)}")
    st.info("분수에서 아래 숫자는 전체 조각 수, 위 숫자는 손님이 주문한 조각 수예요.")
    if st.button("🔁 다시 도전하기", type="primary", use_container_width=True):
        for key in (
            "game_started",
            "game_over",
            "game_started_at",
            "orders_completed",
            "stars",
            "current_order",
            "selected_slices",
            "order_feedback",
            "celebration",
            "game_id",
        ):
            del st.session_state[key]
        initialize_state()
        st.rerun()


initialize_state()
render_header()

if st.session_state.game_over:
    render_results()
elif st.session_state.game_started:
    render_live_game()
else:
    render_home()
