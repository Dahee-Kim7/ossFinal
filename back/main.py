import re
from typing import List, Optional

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import db
from courses import COURSES, DEPARTMENTS, DAY_CHARS

app = FastAPI(title="전공/교양 과목 추천 API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

COURSE_BY_CODE = {c["code"]: c for c in COURSES}


@app.on_event("startup")
def on_startup():
    db.init_db()


def _course_brief(code: str):
    c = COURSE_BY_CODE.get(code)
    if not c:
        return None
    return {
        "code": c["code"],
        "name": c["name"],
        "department": c["department"],
        "level": c["level"],
        "professor": c["professor"],
        "time": c["time"],
    }


@app.get("/")
def root():
    return {"message": "전공/교양 과목 추천 API가 정상적으로 동작 중입니다."}


@app.get("/departments")
def get_departments():
    return {"departments": DEPARTMENTS}


@app.get("/courses")
def get_courses(department: Optional[str] = Query(default=None)):
    """학과/영역별 과목 목록. '이미 들은 과목' 선택용으로 (이름, 학정번호)를 함께 반환."""
    items = [
        {"code": c["code"], "name": c["name"]}
        for c in COURSES
        if department is None or c["department"] == department
    ]
    return {"courses": items}


# ---------------------------------------------------------------
# 회원가입 / 로그인
# ---------------------------------------------------------------
class AuthRequest(BaseModel):
    username: str
    password: str


@app.post("/register")
def register(req: AuthRequest):
    username = req.username.strip()
    password = req.password

    if not username or not password:
        return {"success": False, "message": "아이디와 비밀번호를 모두 입력해주세요."}

    if db.get_user(username) is not None:
        return {"success": False, "message": "이미 존재하는 아이디입니다."}

    db.create_user(username, password)
    return {"success": True, "message": "회원가입이 완료되었습니다. 로그인해주세요."}


@app.post("/login")
def login(req: AuthRequest):
    username = req.username.strip()
    password = req.password

    if db.get_user(username) is None:
        return {"success": False, "message": "존재하지 않는 아이디입니다."}

    if not db.verify_user(username, password):
        return {"success": False, "message": "비밀번호가 일치하지 않습니다."}

    return {"success": True, "message": "로그인 성공"}


def _require_user(username: str):
    if db.get_user(username) is None:
        raise HTTPException(status_code=404, detail="존재하지 않는 사용자입니다.")


# ---------------------------------------------------------------
# 이미 들은 과목
# ---------------------------------------------------------------
class CourseCodeRequest(BaseModel):
    course_code: str


@app.get("/users/{username}/taken")
def get_taken(username: str):
    _require_user(username)
    codes = db.get_taken_codes(username)
    courses = [b for b in (_course_brief(code) for code in codes) if b]
    courses.sort(key=lambda c: (c["department"], c["level"], c["name"]))
    return {"taken": courses}


@app.post("/users/{username}/taken")
def add_taken(username: str, req: CourseCodeRequest):
    _require_user(username)
    if req.course_code not in COURSE_BY_CODE:
        raise HTTPException(status_code=404, detail="존재하지 않는 과목입니다.")
    db.add_taken_code(username, req.course_code)
    return {"success": True}


@app.delete("/users/{username}/taken/{course_code}")
def remove_taken(username: str, course_code: str):
    _require_user(username)
    db.remove_taken_code(username, course_code)
    return {"success": True}


# ---------------------------------------------------------------
# 저장한 강의 (찜 목록)
# ---------------------------------------------------------------
@app.get("/users/{username}/saved")
def get_saved(username: str):
    _require_user(username)
    codes = db.get_saved_codes(username)
    courses = [b for b in (_course_brief(code) for code in codes) if b]
    courses.sort(key=lambda c: (c["department"], c["level"], c["name"]))
    return {"saved": courses}


@app.post("/users/{username}/saved")
def add_saved(username: str, req: CourseCodeRequest):
    _require_user(username)
    if req.course_code not in COURSE_BY_CODE:
        raise HTTPException(status_code=404, detail="존재하지 않는 과목입니다.")
    db.add_saved_code(username, req.course_code)
    return {"success": True}


@app.delete("/users/{username}/saved/{course_code}")
def remove_saved(username: str, course_code: str):
    _require_user(username)
    db.remove_saved_code(username, course_code)
    return {"success": True}


# ---------------------------------------------------------------
# 추천(필터링)
# ---------------------------------------------------------------
class RecommendRequest(BaseModel):
    department: str
    levels: List[int] = []
    day_time: Optional[str] = None
    credit: Optional[int] = None  # 1, 2, 3 중 하나. None이면 전체
    username: Optional[str] = None


def _normalize_day_time(text: str) -> Optional[str]:
    if not text:
        return None
    cleaned = re.sub(r"\s+", "", text)
    m = re.fullmatch(rf"([{DAY_CHARS}])(\d+)", cleaned)
    if not m:
        return None
    return f"{m.group(1)}{m.group(2)}"


@app.post("/recommend")
def recommend(req: RecommendRequest):
    day_time_token = _normalize_day_time(req.day_time) if req.day_time else None

    taken_codes = set()
    if req.username:
        taken_codes = db.get_taken_codes(req.username)

    results = []
    for c in COURSES:
        if c["department"] != req.department:
            continue
        if c["code"] in taken_codes:
            continue
        if req.levels and c["level"] not in req.levels:
            continue
        if day_time_token and day_time_token not in c["schedule"]:
            continue
        if req.credit is not None and c.get("credit", 3) != req.credit:
            continue

        reasons = [f"{req.department} 소속 과목"]
        if req.levels:
            reasons.append(f"난이도 {c['level']} (선택한 난이도에 포함)")
        if day_time_token:
            reasons.append(f"{day_time_token} 시간에 강의 진행")
        if req.credit is not None:
            reasons.append(f"{req.credit}학점 과목")

        results.append({
            "code": c["code"],
            "name": c["name"],
            "department": c["department"],
            "level": c["level"],
            "credit": c.get("credit", 3),
            "professor": c["professor"],
            "time": c["time"],
            "reason": " / ".join(reasons),
        })

    results.sort(key=lambda x: (x["level"], x["name"]))

    return {
        "total": len(results),
        "recommendations": results,
        "day_time_query": day_time_token,
    }
