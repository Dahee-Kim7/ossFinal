import os
import requests
import streamlit as st

API_URL = os.environ.get("FASTAPI_URL", "http://localhost:8000")

# 로그인 여부에 따라 layout 동적 전환
if "username" not in st.session_state:
    st.session_state.username = None
if "auth_mode" not in st.session_state:
    st.session_state.auth_mode = "login"
if "levels" not in st.session_state:
    st.session_state.levels = []
if "search_result" not in st.session_state:
    st.session_state.search_result = None
if "page" not in st.session_state:
    st.session_state.page = "search"
if "saved_codes" not in st.session_state:
    st.session_state.saved_codes = set()

is_logged_in = st.session_state.username is not None

st.set_page_config(
    page_title="강의 추천 시스템",
    page_icon="",
    layout="wide" if is_logged_in else "centered",
)

# ── 공통 CSS ──────────────────────────────────────────────────
st.markdown("""
<style>
[data-testid="stAppViewContainer"] { background: #f5f6f8; }
[data-testid="stHeader"] { display: none; }
#MainMenu { display: none; }
footer { display: none; }
.block-container { padding-top: 3rem !important; }

/* ── 로그인 ── */
.logo-box {
    background: #660418;
    color: #ffffff;
    font-size: 16px;
    font-weight: 700;
    text-align: center;
    padding: 16px;
    border-radius: 12px;
    margin-bottom: 1.5rem;
}
.auth-title { font-size: 18px; font-weight: 600; color: #1a1d23; margin: 0 0 4px; }
.auth-sub   { font-size: 13px; color: #9ca3af; margin: 0 0 1.25rem; }

/* ── 사이드바 ── */
[data-testid="stSidebar"] { background: #ffffff; border-right: 1px solid #e8e9ec; }
[data-testid="stSidebar"] > div:first-child { padding-top: 1.5rem; }
.sb-user { display: flex; align-items: center; gap: 10px; padding: 0 0 1rem; }
.sb-avatar {
    width: 38px; height: 38px; border-radius: 50%;
    background: #fdf2f4; color: #660418;
    font-size: 15px; font-weight: 700;
    display: flex; align-items: center; justify-content: center;
}
.sb-name  { font-size: 14px; font-weight: 600; color: #1a1d23; }
.sb-label { font-size: 12px; color: #9ca3af; }
.sb-divider { border: none; border-top: 1px solid #e8e9ec; margin: 0 0 1rem; }

/* ── 섹션 레이블 ── */
.filter-label {
    font-size: 11px; font-weight: 600; color: #9ca3af;
    letter-spacing: 0.07em; text-transform: uppercase;
    margin: 1.25rem 0 0.4rem;
}

/* ── 난이도 칩 ── */
.chip {
    display: inline-block; padding: 4px 14px;
    border-radius: 20px; border: 1.5px solid #d1d5db;
    font-size: 13px; font-weight: 500; color: #374151;
    background: #ffffff; margin-right: 6px;
}
.chip.on { background: #660418; border-color: #660418; color: #ffffff; }

/* ── 결과/목록 카드 ── */
.course-card, .list-card {
    background: #ffffff; border: 1px solid #e8e9ec;
    border-radius: 12px; padding: 1rem 1.25rem; margin-bottom: 0.6rem;
}
.course-name, .list-name { font-size: 15px; font-weight: 600; color: #1a1d23; margin: 0 0 5px; }
.course-meta, .list-meta { font-size: 13px; color: #6b7280; margin: 0 0 2px; }
.course-code, .list-dept { font-size: 11px; color: #c4c9d4; font-family: monospace; margin-top: 5px; display: block; }
.level-badge {
    display: inline-block; font-size: 11px; font-weight: 600;
    padding: 2px 8px; border-radius: 10px;
    background: #fdf2f4; color: #660418;
    margin-left: 8px; vertical-align: middle;
}

/* ── 페이지 헤더 ── */
.page-title { font-size: 20px; font-weight: 700; color: #1a1d23; margin: 0 0 2px; }
.page-sub   { font-size: 13px; color: #9ca3af; margin: 0 0 1.25rem; }
.page-divider { border: none; border-top: 1px solid #e8e9ec; margin-bottom: 1.25rem; }

/* ── 버튼 컬러 오버라이드 ── */
[data-testid="stSidebar"] button[kind="secondary"] {
    color: #374151 !important;
    background: transparent !important;
    border: 1px solid #e8e9ec !important;
    font-weight: 400 !important;
}
[data-testid="stSidebar"] button[kind="primary"] {
    background: #660418 !important;
    border-color: #660418 !important;
    color: #ffffff !important;
}
button[kind="primary"] {
    background: #660418 !important;
    border-color: #660418 !important;
}
button[kind="primary"]:hover {
    background: #4d0312 !important;
    border-color: #4d0312 !important;
}

/* ── 저장된 카드 강조 ── */
.course-card.saved {
    background: #fdf2f4 !important;
    border-color: #660418 !important;
}

/* ── 빈 상태 ── */
.empty-state { text-align: center; padding: 3rem 1rem; color: #c4c9d4; font-size: 14px; }
</style>
""", unsafe_allow_html=True)


def api_get(path, params=None):
    return requests.get(f"{API_URL}{path}", params=params, timeout=5)

def api_post(path, json=None):
    return requests.post(f"{API_URL}{path}", json=json, timeout=5)

def api_delete(path):
    return requests.delete(f"{API_URL}{path}", timeout=5)

@st.cache_data(show_spinner=False)
def get_departments():
    try:
        return api_get("/departments").json().get("departments", [])
    except Exception:
        return []


# ── 로그인 / 회원가입 ──────────────────────────────────────────
def show_auth():
    mode = st.session_state.auth_mode

    st.markdown('<div class="logo-box">강의 추천 시스템</div>', unsafe_allow_html=True)

    if mode == "login":
        st.markdown('<p class="auth-title">로그인</p><p class="auth-sub">아이디와 비밀번호를 입력하세요</p>',
                    unsafe_allow_html=True)
        with st.form("login_form"):
            username = st.text_input("아이디", placeholder="아이디를 입력하세요")
            password = st.text_input("비밀번호", type="password", placeholder="비밀번호를 입력하세요")
            submitted = st.form_submit_button("로그인", use_container_width=True, type="primary")
        if submitted:
            try:
                data = api_post("/login", json={"username": username, "password": password}).json()
                if data["success"]:
                    st.session_state.username = username
                    st.rerun()
                else:
                    st.error(data["message"])
            except Exception as e:
                st.error(f"서버 연결 실패: {e}")
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("계정이 없으신가요? 회원가입", use_container_width=True):
            st.session_state.auth_mode = "register"
            st.rerun()

    else:
        st.markdown('<p class="auth-title">회원가입</p><p class="auth-sub">아이디와 비밀번호를 설정하세요</p>',
                    unsafe_allow_html=True)
        with st.form("register_form"):
            username = st.text_input("아이디", placeholder="영문/숫자 조합 권장")
            password = st.text_input("비밀번호", type="password", placeholder="비밀번호를 입력하세요")
            submitted = st.form_submit_button("가입하기", use_container_width=True, type="primary")
        if submitted:
            try:
                data = api_post("/register", json={"username": username, "password": password}).json()
                if data["success"]:
                    st.success(data["message"])
                else:
                    st.error(data["message"])
            except Exception as e:
                st.error(f"서버 연결 실패: {e}")
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("로그인으로 돌아가기", use_container_width=True):
            st.session_state.auth_mode = "login"
            st.rerun()


# ── 사이드바 ───────────────────────────────────────────────────
def show_sidebar(username):
    with st.sidebar:
        initial = username[0].upper() if username else "?"
        st.markdown(
            f'<div class="sb-user">'
            f'<div class="sb-avatar">{initial}</div>'
            f'<div><div class="sb-name">{username}</div>'
            f'<div class="sb-label">로그인됨</div></div>'
            f'</div><hr class="sb-divider">',
            unsafe_allow_html=True,
        )

        pages = [("search", "과목 검색"), ("saved", "저장한 강의"), ("taken", "수강한 강의")]
        for key, label in pages:
            active = st.session_state.page == key
            if st.button(
                label,
                key=f"nav_{key}",
                use_container_width=True,
                type="primary" if active else "secondary",
            ):
                st.session_state.page = key
                st.rerun()

        st.markdown("<hr class='sb-divider' style='margin-top:1rem'>", unsafe_allow_html=True)
        if st.button("로그아웃", use_container_width=True):
            st.session_state.username = None
            st.session_state.search_result = None
            st.session_state.levels = []
            st.session_state.page = "search"
            st.rerun()


# ── 과목 검색 페이지 ───────────────────────────────────────────
def page_search(username):
    st.markdown('<p class="page-title">과목 검색</p><p class="page-sub">2026학년도 1학기 · 학과/교양 과목</p>',
                unsafe_allow_html=True)
    st.markdown('<hr class="page-divider">', unsafe_allow_html=True)

    departments = get_departments()
    st.markdown('<p class="filter-label">학과 / 교양 영역</p>', unsafe_allow_html=True)
    department = st.selectbox("학과선택", departments, label_visibility="collapsed")

    st.markdown('<p class="filter-label">난이도 (복수 선택 가능 · 미선택 시 전체)</p>', unsafe_allow_html=True)
    cols = st.columns(4)
    for i, (col, label) in enumerate(zip(cols, ["1학년", "2학년", "3학년", "4학년"]), start=1):
        with col:
            checked = i in st.session_state.levels
            if st.button(
                label,
                key=f"lv_{i}",
                use_container_width=True,
                type="primary" if checked else "secondary",
            ):
                if checked:
                    st.session_state.levels.remove(i)
                else:
                    st.session_state.levels.append(i)
                st.rerun()
    selected_levels = st.session_state.levels

    st.markdown('<p class="filter-label">요일 / 교시 (선택사항)</p>', unsafe_allow_html=True)
    day_time_input = st.text_input("요일교시", placeholder="예: 화1  (화요일 1교시)",
                                   label_visibility="collapsed")

    st.markdown('<p class="filter-label">학점 (미선택 시 전체)</p>', unsafe_allow_html=True)
    credit_cols = st.columns(3)
    credit_labels = ["1학점", "2학점", "3학점"]
    if "credit" not in st.session_state:
        st.session_state.credit = None
    for i, (col, label) in enumerate(zip(credit_cols, credit_labels), start=1):
        with col:
            selected = st.session_state.credit == i
            if st.button(
                label,
                key=f"credit_{i}",
                use_container_width=True,
                type="primary" if selected else "secondary",
            ):
                st.session_state.credit = None if selected else i
                st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("과목 검색", type="primary", use_container_width=True):
        try:
            res = api_post("/recommend", json={
                "department": department,
                "levels": selected_levels,
                "day_time": day_time_input.strip() or None,
                "credit": st.session_state.credit,
                "username": username,
            })
            st.session_state.search_result = res.json()
        except Exception as e:
            st.error(f"서버 연결 실패: {e}")
            st.session_state.search_result = None

    result = st.session_state.search_result
    if result is None:
        return

    if day_time_input and result.get("day_time_query") is None:
        st.warning("요일/교시 형식을 인식하지 못했습니다. '화1', '월3' 형태로 입력해주세요.")

    recommendations = result.get("recommendations", [])
    if not recommendations:
        st.markdown('<div class="empty-state">조건에 맞는 과목이 없습니다.<br>필터를 조정해보세요.</div>',
                    unsafe_allow_html=True)
        return

    st.markdown(f"<br>**검색 결과 {result['total']}개**", unsafe_allow_html=True)
    st.markdown("<hr style='margin:0.4rem 0 0.8rem;border:none;border-top:1px solid #e8e9ec'>",
                unsafe_allow_html=True)

    # 저장된 강의 코드 동기화
    if result:
        try:
            saved_list = api_get(f"/users/{username}/saved").json().get("saved", [])
            st.session_state.saved_codes = {c["code"] for c in saved_list}
        except Exception:
            pass

    for c in recommendations:
        is_saved = c["code"] in st.session_state.saved_codes
        col_info, col_btn = st.columns([6, 1])
        with col_info:
            card_class = "course-card saved" if is_saved else "course-card"
            st.markdown(
                f'<div class="{card_class}">'
                f'<p class="course-name">{c["name"]}'
                f'<span class="level-badge">난이도 {c["level"]}</span>'
                f'<span class="level-badge">{c.get("credit", 3)}학점</span></p>'
                f'<p class="course-meta">{c["professor"]}</p>'
                f'<p class="course-meta">{c["time"]}</p>'
                f'<span class="course-code">{c["code"]}</span>'
                f'</div>',
                unsafe_allow_html=True,
            )
        with col_btn:
            st.markdown("<br><br>", unsafe_allow_html=True)
            if not is_saved:
                if st.button("+", key=f"save_{c['code']}", help="저장한 강의에 추가"):
                    r = api_post(f"/users/{username}/saved", json={"course_code": c["code"]})
                    if r.ok:
                        st.session_state.saved_codes.add(c["code"])
                        st.toast(f"'{c['name']}' 추가되었습니다.")
                        st.rerun()
                    else:
                        st.error("저장에 실패했습니다.")
            else:
                st.markdown("<p style='text-align:center;color:#660418;font-size:18px;margin-top:8px'>✓</p>",
                            unsafe_allow_html=True)


# ── 저장한 강의 페이지 ─────────────────────────────────────────
def page_saved(username):
    st.markdown('<p class="page-title">저장한 강의</p><p class="page-sub">관심 있는 강의를 모아보세요</p>',
                unsafe_allow_html=True)
    st.markdown('<hr class="page-divider">', unsafe_allow_html=True)

    try:
        saved = api_get(f"/users/{username}/saved").json().get("saved", [])
    except Exception as e:
        st.error(f"서버 연결 실패: {e}")
        return

    if not saved:
        st.markdown('<div class="empty-state">저장한 강의가 없습니다.<br>과목 검색에서 + 버튼으로 추가해보세요.</div>',
                    unsafe_allow_html=True)
        return

    st.markdown(f"**총 {len(saved)}개**", unsafe_allow_html=True)
    st.markdown("<hr style='margin:0.4rem 0 0.8rem;border:none;border-top:1px solid #e8e9ec'>",
                unsafe_allow_html=True)

    for c in saved:
        col_info, col_btn = st.columns([6, 1])
        with col_info:
            st.markdown(
                f'<div class="list-card">'
                f'<p class="list-name">{c["name"]}'
                f'<span class="level-badge">난이도 {c["level"]}</span></p>'
                f'<p class="list-meta">{c["professor"]}</p>'
                f'<p class="list-meta">{c["time"]}</p>'
                f'<span class="list-dept">{c["department"]} · {c["code"]}</span>'
                f'</div>',
                unsafe_allow_html=True,
            )
        with col_btn:
            st.markdown("<br><br>", unsafe_allow_html=True)
            if st.button("삭제", key=f"del_{c['code']}"):
                api_delete(f"/users/{username}/saved/{c['code']}")
                st.rerun()


# ── 수강한 강의 페이지 ─────────────────────────────────────────
def page_taken(username):
    st.markdown('<p class="page-title">수강한 강의</p><p class="page-sub">이미 들은 과목은 검색 결과에서 제외됩니다</p>',
                unsafe_allow_html=True)
    st.markdown('<hr class="page-divider">', unsafe_allow_html=True)

    # ── 수강 과목 등록 (학과 선택 → 해당 학과 과목 목록에서 선택) ──
    departments = get_departments()
    st.markdown('<p class="filter-label">학과 / 교양 영역 선택</p>', unsafe_allow_html=True)
    department = st.selectbox("학과선택", departments, label_visibility="collapsed", key="taken_dept")

    try:
        dept_courses = api_get("/courses", params={"department": department}).json().get("courses", [])
        taken_all = {c["code"] for c in api_get(f"/users/{username}/taken").json().get("taken", [])}
    except Exception:
        dept_courses, taken_all = [], set()

    code_to_name = {c["code"]: c["name"] for c in dept_courses}
    name_to_code = {v: k for k, v in code_to_name.items()}
    dept_codes = set(code_to_name.keys())
    default_names = [code_to_name[c] for c in taken_all if c in code_to_name]

    st.markdown('<p class="filter-label">수강 완료 과목 선택</p>', unsafe_allow_html=True)
    selected_names = st.multiselect(
        "수강 완료 과목", options=list(code_to_name.values()),
        default=default_names, key=f"taken_{department}",
        label_visibility="collapsed", placeholder="과목을 선택하세요",
    )
    if st.button("저장", key=f"save_taken_{department}", type="primary"):
        new_codes = {name_to_code[n] for n in selected_names}
        for code in (new_codes - (taken_all & dept_codes)):
            api_post(f"/users/{username}/taken", json={"course_code": code})
        for code in ((taken_all & dept_codes) - new_codes):
            api_delete(f"/users/{username}/taken/{code}")
        st.success("저장되었습니다.")
        st.rerun()

    # ── 전체 수강 목록 ──
    try:
        taken = api_get(f"/users/{username}/taken").json().get("taken", [])
    except Exception as e:
        st.error(f"서버 연결 실패: {e}")
        return

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<p class="filter-label">등록된 수강 과목 전체 목록</p>', unsafe_allow_html=True)
    st.markdown("<hr style='margin:0.4rem 0 0.8rem;border:none;border-top:1px solid #e8e9ec'>",
                unsafe_allow_html=True)

    if not taken:
        st.markdown('<div class="empty-state">등록된 수강 과목이 없습니다.<br>위에서 학과를 선택하고 과목을 추가해보세요.</div>',
                    unsafe_allow_html=True)
        return

    st.markdown(f"**총 {len(taken)}개**", unsafe_allow_html=True)

    for c in taken:
        col_info, col_btn = st.columns([6, 1])
        with col_info:
            st.markdown(
                f'<div class="list-card">'
                f'<p class="list-name">{c["name"]}'
                f'<span class="level-badge">난이도 {c["level"]}</span></p>'
                f'<p class="list-meta">{c["professor"]}</p>'
                f'<p class="list-meta">{c["time"]}</p>'
                f'<span class="list-dept">{c["department"]} · {c["code"]}</span>'
                f'</div>',
                unsafe_allow_html=True,
            )
        with col_btn:
            st.markdown("<br><br>", unsafe_allow_html=True)
            if st.button("삭제", key=f"taken_del_{c['code']}"):
                api_delete(f"/users/{username}/taken/{c['code']}")
                st.rerun()


# ── 메인 ──────────────────────────────────────────────────────
if not is_logged_in:
    show_auth()
else:
    show_sidebar(st.session_state.username)
    page = st.session_state.page
    if page == "search":
        page_search(st.session_state.username)
    elif page == "saved":
        page_saved(st.session_state.username)
    elif page == "taken":
        page_taken(st.session_state.username)
