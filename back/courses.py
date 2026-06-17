# 광운대학교 2026학년도 1학기 강의시간표 데이터
#
# 난이도(level)는 학정번호의 두 번째 자리(전체 자릿수 기준 5번째 자리) 숫자를 그대로 사용합니다.
# 예) 0000-1-0355-01 -> level = 1
#     I020-3-1647-01 -> level = 3
# 전공 과목의 경우 보통 "권장 학년"의 의미로 쓰이고, 교양 과목은 "난이도" 의미로 쓰입니다.
#
# department 값은 다음 중 하나입니다.
# 전공: 컴퓨터정보공학부 / 소프트웨어학부 / 정보융합학부 / 로봇학부 / 지능형로봇학과
# 교양: 교양(필수-AI리터러시) / 교양(대학실용영어) / 교양(언어와표현) / 교양(과학과기술) /
#       교양(인간과철학) / 교양(사회와경제) / 교양(글로벌문화와제2외국어) / 교양(예술과체육) /
#       교양(수리와자연-수학) / 교양(수리와자연-물리) / 교양(수리와자연-화학) / 교양(기초학문융합)

import re

DAY_CHARS = "월화수목금토일"

DEPARTMENTS = [
    "컴퓨터정보공학부",
    "소프트웨어학부",
    "정보융합학부",
    "로봇학부",
    "지능형로봇학과",
    "교양(필수-AI리터러시)",
    "교양(대학실용영어)",
    "교양(언어와표현)",
    "교양(과학과기술)",
    "교양(인간과철학)",
    "교양(사회와경제)",
    "교양(글로벌문화와제2외국어)",
    "교양(예술과체육)",
    "교양(수리와자연-수학)",
    "교양(수리와자연-물리)",
    "교양(수리와자연-화학)",
    "교양(기초학문융합)",
]


def parse_schedule(time_str: str):
    """'월 1 수 2', '화 0,1,2' 같은 강의시간 문자열에서 ['월1','수2'] / ['화0','화1','화2'] 형태의
    검색용 토큰 리스트를 만든다. 원격수업100% 처럼 요일/교시가 없는 경우 빈 리스트를 반환한다."""
    tokens = []
    pattern = re.compile(rf"([{DAY_CHARS}])\s*([\d,\s]+)")
    for m in pattern.finditer(time_str):
        day = m.group(1)
        nums = re.findall(r"\d+", m.group(2))
        for n in nums:
            tokens.append(f"{day}{n}")
    return tokens


# ---------------------------------------------------------------
# 전공 과목
# ---------------------------------------------------------------
MAJOR_COURSES = [
    # ===== 컴퓨터정보공학부 (I020) =====
    {"code": "I020-1-8101-01", "name": "컴퓨터공학입문세미나", "department": "컴퓨터정보공학부",
     "level": 1, "professor": "신동화", "time": "화 7,8 (세미나강의)"},
    {"code": "I020-2-0453-01", "name": "디지털논리회로1", "department": "컴퓨터정보공학부",
     "level": 2, "professor": "유지현", "time": "월 4 (원격50%이상)"},
    {"code": "I020-2-1994-01", "name": "회로이론", "department": "컴퓨터정보공학부",
     "level": 2, "professor": "황호영", "time": "월 5 수 6"},
    {"code": "I020-2-8086-01", "name": "컴퓨터공학기초실험1", "department": "컴퓨터정보공학부",
     "level": 2, "professor": "장진곤", "time": "화 0,1,2"},
    {"code": "I020-2-8481-01", "name": "객체지향프로그래밍설계", "department": "컴퓨터정보공학부",
     "level": 2, "professor": "심동규", "time": "화 6 목 5 (PBL강의)"},
    {"code": "I020-2-8482-01", "name": "객체지향프로그래밍실습", "department": "컴퓨터정보공학부",
     "level": 2, "professor": "신동화", "time": "월 7,8"},
    {"code": "I020-3-0922-01", "name": "시스템프로그래밍", "department": "컴퓨터정보공학부",
     "level": 3, "professor": "김태석", "time": "월 6 수 5"},
    {"code": "I020-3-1647-01", "name": "컴퓨터구조", "department": "컴퓨터정보공학부",
     "level": 3, "professor": "장진곤", "time": "월 2 수 1"},
    {"code": "I020-3-1654-01", "name": "컴퓨터네트워크", "department": "컴퓨터정보공학부",
     "level": 3, "professor": "이혁준", "time": "화 4 목 3"},
    {"code": "I020-3-2004-01", "name": "신호및시스템", "department": "컴퓨터정보공학부",
     "level": 3, "professor": "최상호", "time": "목 4 (원격50%이상)"},
    {"code": "I020-3-3704-01", "name": "시스템프로그래밍실습", "department": "컴퓨터정보공학부",
     "level": 3, "professor": "김태석", "time": "목 3,4"},
    {"code": "I020-3-3831-01", "name": "컴퓨터구조실험", "department": "컴퓨터정보공학부",
     "level": 3, "professor": "장진곤", "time": "월 3,4"},
    {"code": "I020-4-0846-01", "name": "소프트웨어공학", "department": "컴퓨터정보공학부",
     "level": 4, "professor": "이우신", "time": "금 3,4"},
    {"code": "I020-4-4136-01", "name": "컴퓨터비전", "department": "컴퓨터정보공학부",
     "level": 4, "professor": "심동규", "time": "화 5 목 6"},
    {"code": "I020-4-5466-01", "name": "무선모바일네트워크", "department": "컴퓨터정보공학부",
     "level": 4, "professor": "이형근", "time": "월 6 수 5"},
    {"code": "I020-4-5467-01", "name": "산학협력캡스톤설계", "department": "컴퓨터정보공학부",
     "level": 4, "professor": "이형근", "time": "월 5 수 6 (TBL강의)"},
    {"code": "I020-4-5468-01", "name": "정보보호이론", "department": "컴퓨터정보공학부",
     "level": 4, "professor": "유지현", "time": "금 1,2"},
    {"code": "I020-4-5861-01", "name": "임베디드시스템S/W설계", "department": "컴퓨터정보공학부",
     "level": 4, "professor": "김태석", "time": "월 4 수 3"},
    {"code": "I020-4-8483-01", "name": "머신러닝", "department": "컴퓨터정보공학부",
     "level": 4, "professor": "박철수, 이혁준", "time": "화 6 목 5 (팀티칭강의)"},
    {"code": "I020-4-9615-01", "name": "GPU컴퓨팅", "department": "컴퓨터정보공학부",
     "level": 4, "professor": "신동화", "time": "목 3 (원격50%이상)"},

    # ===== 소프트웨어학부 (I030) =====
    {"code": "I030-1-8998-01", "name": "소프트웨어입문세미나", "department": "소프트웨어학부",
     "level": 1, "professor": "문승현", "time": "화 6"},
    {"code": "I030-2-0448-01", "name": "디지털논리", "department": "소프트웨어학부",
     "level": 2, "professor": "(분반별 상이)", "time": "월 5,6"},
    {"code": "I030-2-3403-01", "name": "고급프로그래밍", "department": "소프트웨어학부",
     "level": 2, "professor": "최영근", "time": "월 1,2"},
    {"code": "I030-2-5409-01", "name": "웹프로그래밍", "department": "소프트웨어학부",
     "level": 2, "professor": "김우생", "time": "화 2 목 1"},
    {"code": "I030-2-5952-01", "name": "파이썬기반인공지능기초", "department": "소프트웨어학부",
     "level": 2, "professor": "김종국", "time": "금 3,4"},
    {"code": "I030-2-8484-01", "name": "리눅스활용실습", "department": "소프트웨어학부",
     "level": 2, "professor": "김용혁", "time": "목 1,2"},
    {"code": "I030-3-0969-01", "name": "알고리즘", "department": "소프트웨어학부",
     "level": 3, "professor": "박병준", "time": "화 5 (원격50%이상, PBL강의)"},
    {"code": "I030-3-1110-01", "name": "운영체제", "department": "소프트웨어학부",
     "level": 3, "professor": "안우현", "time": "월 3 수 4"},
    {"code": "I030-3-1647-01", "name": "컴퓨터구조", "department": "소프트웨어학부",
     "level": 3, "professor": "이윤구", "time": "화 1 목 2"},
    {"code": "I030-3-3663-01", "name": "데이터베이스", "department": "소프트웨어학부",
     "level": 3, "professor": "문승현", "time": "월 1 수 2"},
    {"code": "I030-3-4534-01", "name": "데이터통신", "department": "소프트웨어학부",
     "level": 3, "professor": "최웅철", "time": "월 5 수 6"},
    {"code": "I030-3-8485-01", "name": "응용소프트웨어실습", "department": "소프트웨어학부",
     "level": 3, "professor": "임재한", "time": "수 0,1,2"},
    {"code": "I030-4-0846-01", "name": "소프트웨어공학", "department": "소프트웨어학부",
     "level": 4, "professor": "이윤구", "time": "목 4 (원격50%이상)"},
    {"code": "I030-4-3683-01", "name": "딥러닝실습", "department": "소프트웨어학부",
     "level": 4, "professor": "문승현", "time": "화 1,2"},
    {"code": "I030-4-3684-01", "name": "정보시스템응용", "department": "소프트웨어학부",
     "level": 4, "professor": "최웅철", "time": "월 6 수 5"},
    {"code": "I030-4-3685-01", "name": "컴퓨터애니메이션실습", "department": "소프트웨어학부",
     "level": 4, "professor": "최민규", "time": "화 5 목 6"},
    {"code": "I030-4-3830-01", "name": "네트워크보안", "department": "소프트웨어학부",
     "level": 4, "professor": "(소프트웨어학부)", "time": "수 1,2"},
    {"code": "I030-4-4535-01", "name": "무선네트워크", "department": "소프트웨어학부",
     "level": 4, "professor": "최웅철", "time": "월 4 수 3"},
    {"code": "I030-4-8995-01", "name": "산학협력캡스톤설계1", "department": "소프트웨어학부",
     "level": 4, "professor": "이동호", "time": "금 3,4"},
    {"code": "I030-4-9151-01", "name": "기계학습", "department": "소프트웨어학부",
     "level": 4, "professor": "박병준", "time": "화 6 (원격50%이상)"},

    # ===== 정보융합학부 (I040) =====
    {"code": "I040-2-1234-01", "name": "진로탐색및설계", "department": "정보융합학부",
     "level": 2, "professor": "조민수", "time": "화 10,11 (원격100%)"},
    {"code": "I040-2-3688-01", "name": "AI수학", "department": "정보융합학부",
     "level": 2, "professor": "조민수", "time": "목 4 (원격50%이상)"},
    {"code": "I040-2-7777-01", "name": "객체지향프로그래밍", "department": "정보융합학부",
     "level": 2, "professor": "김준석", "time": "화 1 목 2"},
    {"code": "I040-2-9157-01", "name": "오픈소스소프트웨어실습", "department": "정보융합학부",
     "level": 2, "professor": "박규동", "time": "원격수업100%"},
    {"code": "I040-3-3663-01", "name": "데이터베이스", "department": "정보융합학부",
     "level": 3, "professor": "임동혁", "time": "월 4 수 3"},
    {"code": "I040-3-3951-01", "name": "컴퓨터그래픽스", "department": "정보융합학부",
     "level": 3, "professor": "김동준", "time": "화 3 목 4"},
    {"code": "I040-3-4139-01", "name": "텍스트마이닝", "department": "정보융합학부",
     "level": 3, "professor": "조민수", "time": "월 3 수 4 (PBL강의)"},
    {"code": "I040-3-5474-01", "name": "컴퓨터비전", "department": "정보융합학부",
     "level": 3, "professor": "김수환", "time": "화 4 목 3"},
    {"code": "I040-3-7737-01", "name": "UX/UI디자인", "department": "정보융합학부",
     "level": 3, "professor": "박규동", "time": "수 5,6"},
    {"code": "I040-3-9151-01", "name": "기계학습", "department": "정보융합학부",
     "level": 3, "professor": "이상민", "time": "수 2 (원격50%이상)"},
    {"code": "I040-4-5471-01", "name": "영상AI생성모델", "department": "정보융합학부",
     "level": 4, "professor": "김동준", "time": "화 4 목 3"},
    {"code": "I040-4-6414-01", "name": "네트워크데이터분석", "department": "정보융합학부",
     "level": 4, "professor": "김준석", "time": "화 5 목 6"},
    {"code": "I040-4-6415-01", "name": "MLOps엔지니어링", "department": "정보융합학부",
     "level": 4, "professor": "이상민", "time": "월 4 수 3"},
    {"code": "I040-4-8995-01", "name": "산학협력캡스톤설계1", "department": "정보융합학부",
     "level": 4, "professor": "(정보융합학부)", "time": "월 5,6"},
    {"code": "I040-4-9925-01", "name": "데이터시각화", "department": "정보융합학부",
     "level": 4, "professor": "조재희", "time": "수 5,6"},

    # ===== 로봇학부 (I050) =====
    {"code": "I050-2-0444-01", "name": "디지털공학", "department": "로봇학부",
     "level": 2, "professor": "박일우", "time": "화 5 목 6"},
    {"code": "I050-2-1234-01", "name": "진로탐색및설계", "department": "로봇학부",
     "level": 2, "professor": "남재광", "time": "화 8,9 (원격100%)"},
    {"code": "I050-2-1410-01", "name": "전자기학", "department": "로봇학부",
     "level": 2, "professor": "남재광", "time": "화 4 목 3"},
    {"code": "I050-2-1995-01", "name": "회로이론1", "department": "로봇학부",
     "level": 2, "professor": "조영진", "time": "화 1 목 2"},
    {"code": "I050-2-2865-01", "name": "기초역학", "department": "로봇학부",
     "level": 2, "professor": "조황", "time": "금 5,6 (원격100%)"},
    {"code": "I050-2-5473-01", "name": "AI로봇실험1", "department": "로봇학부",
     "level": 2, "professor": "박일우", "time": "수 0,1,2"},
    {"code": "I050-2-6154-01", "name": "로봇학실험1", "department": "로봇학부",
     "level": 2, "professor": "최용훈", "time": "월 0,1,2"},
    {"code": "I050-3-0492-01", "name": "마이크로프로세서", "department": "로봇학부",
     "level": 3, "professor": "박일우", "time": "화 6 목 5"},
    {"code": "I050-3-1236-01", "name": "자동제어1", "department": "로봇학부",
     "level": 3, "professor": "백주훈", "time": "화 5 목 6"},
    {"code": "I050-3-5481-01", "name": "로봇운동학", "department": "로봇학부",
     "level": 3, "professor": "남재광", "time": "금 3,4"},
    {"code": "I050-3-6336-01", "name": "AI로봇실험3", "department": "로봇학부",
     "level": 3, "professor": "정문호", "time": "수 5,6,7"},
    {"code": "I050-3-6538-01", "name": "로봇학실험3", "department": "로봇학부",
     "level": 3, "professor": "박광현", "time": "월 5,6,7"},
    {"code": "I050-3-9151-01", "name": "기계학습", "department": "로봇학부",
     "level": 3, "professor": "박광현", "time": "월 4 수 3"},
    {"code": "I050-4-1462-01", "name": "전자회로", "department": "로봇학부",
     "level": 4, "professor": "서한석", "time": "화 5,6,7"},
    {"code": "I050-4-4163-01", "name": "캡스톤설계", "department": "로봇학부",
     "level": 4, "professor": "남재광", "time": "목 7,8,9 (PBL강의)"},
    {"code": "I050-4-6338-01", "name": "피지컬AI", "department": "로봇학부",
     "level": 4, "professor": "최용훈", "time": "월 3 수 4"},
    {"code": "I050-4-6907-01", "name": "로봇응용시스템", "department": "로봇학부",
     "level": 4, "professor": "양우성", "time": "화 3 목 4"},

    # ===== 지능형로봇학과 (I060) =====
    {"code": "I060-1-4278-01", "name": "지능형로봇의이해", "department": "지능형로봇학과",
     "level": 1, "professor": "최용훈", "time": "금 5,6 (원격100%)"},
    {"code": "I060-1-4287-01", "name": "로봇명사와의만남", "department": "지능형로봇학과",
     "level": 1, "professor": "정문호", "time": "금 1,2 (원격100%)"},
    {"code": "I060-2-4483-01", "name": "로봇과상상", "department": "지능형로봇학과",
     "level": 2, "professor": "김율희", "time": "금 5,6 (TBL강의)"},
    {"code": "I060-2-4484-01", "name": "로봇기초실습", "department": "지능형로봇학과",
     "level": 2, "professor": "이기백", "time": "수 5,6,7"},
    {"code": "I060-2-4485-01", "name": "모바일로봇의이해", "department": "지능형로봇학과",
     "level": 2, "professor": "박수한", "time": "금 3,4 (TBL강의)"},
    {"code": "I060-2-5716-01", "name": "기초로봇설계", "department": "지능형로봇학과",
     "level": 2, "professor": "남재광", "time": "화 6 목 5"},
    {"code": "I060-3-4286-01", "name": "마이크로프로세서응용설계", "department": "지능형로봇학과",
     "level": 3, "professor": "이기백", "time": "수 3 (원격50%이상, PBL강의)"},
    {"code": "I060-3-4301-01", "name": "로봇프로그래밍", "department": "지능형로봇학과",
     "level": 3, "professor": "이예솝", "time": "월 6 수 5"},
    {"code": "I060-3-6110-01", "name": "기술과경영", "department": "지능형로봇학과",
     "level": 3, "professor": "한상휘", "time": "금 3,4"},
    {"code": "I060-4-4026-01", "name": "로봇비전응용", "department": "지능형로봇학과",
     "level": 4, "professor": "정문호", "time": "월 3 수 4 (PBL강의)"},
    {"code": "I060-4-5718-01", "name": "자연어처리기초및응용", "department": "지능형로봇학과",
     "level": 4, "professor": "임동혁", "time": "월 2 (원격50%이상, PBL강의)"},
]


# ---------------------------------------------------------------
# 교양 과목
# ---------------------------------------------------------------
GENERAL_COURSES = [
    # ===== 필수교양(AI리터러시) =====
    {"code": "0000-1-6453-01", "name": "AI리터러시", "department": "교양(필수-AI리터러시)",
     "level": 1, "professor": "이강성 외", "time": "원격수업100%"},

    # ===== 대학실용영어 =====
    {"code": "0000-1-1078-01", "name": "영어회화1", "department": "교양(대학실용영어)",
     "level": 1, "professor": "브라이언", "time": "월 3 수 4"},
    {"code": "0000-1-3362-02", "name": "대학영어", "department": "교양(대학실용영어)",
     "level": 1, "professor": "손영희", "time": "월 4 수 3"},
    {"code": "0000-1-4067-01", "name": "기초영작문", "department": "교양(대학실용영어)",
     "level": 1, "professor": "손영희", "time": "월 6 수 5"},
    {"code": "0000-2-1079-01", "name": "영어회화2", "department": "교양(대학실용영어)",
     "level": 2, "professor": "에이미", "time": "월 3 수 4"},
    {"code": "0000-2-5839-01", "name": "영어발표연습", "department": "교양(대학실용영어)",
     "level": 2, "professor": "목승혜", "time": "금 1,2"},
    {"code": "0000-3-0910-01", "name": "시사영어", "department": "교양(대학실용영어)",
     "level": 3, "professor": "고현아", "time": "월 3 수 4"},
    {"code": "0000-3-8596-01", "name": "영미문화읽기", "department": "교양(대학실용영어)",
     "level": 3, "professor": "박소현", "time": "월 1 수 2"},
    {"code": "0000-4-5842-01", "name": "취업실용영어", "department": "교양(대학실용영어)",
     "level": 4, "professor": "김보식", "time": "금 1,2"},

    # ===== 언어와표현 =====
    {"code": "0000-1-3095-01", "name": "융합적사고와글쓰기", "department": "교양(언어와표현)",
     "level": 1, "professor": "신정은 외", "time": "금 3,4"},
    {"code": "0000-1-5845-01", "name": "발표와설득전략", "department": "교양(언어와표현)",
     "level": 1, "professor": "김학현", "time": "화 1 목 2"},
    {"code": "0000-1-5849-01", "name": "웹소설창작기초", "department": "교양(언어와표현)",
     "level": 1, "professor": "신승일", "time": "금 5,6"},
    {"code": "0000-1-5852-01", "name": "자기성찰과치유적글쓰기", "department": "교양(언어와표현)",
     "level": 1, "professor": "이미진", "time": "화 3 목 4"},
    {"code": "0000-1-6523-01", "name": "말하기와소통", "department": "교양(언어와표현)",
     "level": 1, "professor": "김광섭", "time": "화 2 목 1"},

    # ===== 과학과기술 =====
    {"code": "0000-1-0019-01", "name": "C프로그래밍", "department": "교양(과학과기술)",
     "level": 1, "professor": "조영진 외", "time": "월 1 수 2"},
    {"code": "0000-1-5470-01", "name": "파이썬프로그래밍", "department": "교양(과학과기술)",
     "level": 1, "professor": "김수영 외", "time": "금 1,2"},
    {"code": "0000-1-5819-01", "name": "AI빅데이터의이해", "department": "교양(과학과기술)",
     "level": 1, "professor": "정태원", "time": "화 1 목 2"},
    {"code": "0000-1-5820-01", "name": "AI사무업무활용", "department": "교양(과학과기술)",
     "level": 1, "professor": "서창옥", "time": "월 3 수 4"},
    {"code": "0000-1-5924-01", "name": "스마트사회와인공지능", "department": "교양(과학과기술)",
     "level": 1, "professor": "스레스터바누", "time": "화 1 목 2"},
    {"code": "0000-2-5925-01", "name": "공학과파이썬", "department": "교양(과학과기술)",
     "level": 2, "professor": "민영호", "time": "화 4 목 3"},
    {"code": "0000-2-5926-01", "name": "업무자동화와파이썬", "department": "교양(과학과기술)",
     "level": 2, "professor": "이강성", "time": "월 1 수 2"},
    {"code": "0000-2-5927-01", "name": "데이터분석과파이썬", "department": "교양(과학과기술)",
     "level": 2, "professor": "이강성", "time": "월 3 수 4"},

    # ===== 인간과철학 =====
    {"code": "0000-1-0221-01", "name": "과학철학의이해", "department": "교양(인간과철학)",
     "level": 1, "professor": "우호용", "time": "금 3,4"},
    {"code": "0000-1-2959-01", "name": "인간존재의이해", "department": "교양(인간과철학)",
     "level": 1, "professor": "이지영", "time": "목 7,8,9"},
    {"code": "0000-1-8085-01", "name": "논리적으로사고하기", "department": "교양(인간과철학)",
     "level": 1, "professor": "황순호", "time": "금 5,6"},
    {"code": "0000-2-3932-01", "name": "한국근현대사", "department": "교양(인간과철학)",
     "level": 2, "professor": "김정권", "time": "월 1 수 2"},

    # ===== 사회와경제 =====
    {"code": "0000-1-0806-01", "name": "생활속의경제", "department": "교양(사회와경제)",
     "level": 1, "professor": "이수욱", "time": "월 5 수 6"},
    {"code": "0000-1-3928-01", "name": "성과심리학", "department": "교양(사회와경제)",
     "level": 1, "professor": "이정은", "time": "금 1,2"},
    {"code": "0000-1-5901-01", "name": "기술경영과마케팅", "department": "교양(사회와경제)",
     "level": 1, "professor": "이은정", "time": "화 1 목 2"},
    {"code": "0000-2-3008-01", "name": "조직과리더쉽", "department": "교양(사회와경제)",
     "level": 2, "professor": "손주영", "time": "월 4 수 3"},
    {"code": "0000-3-9448-01", "name": "스타트업과고객발굴전략", "department": "교양(사회와경제)",
     "level": 3, "professor": "이경학", "time": "수 5,6"},

    # ===== 글로벌문화와제2외국어 =====
    {"code": "0000-1-3593-01", "name": "초급일본어1", "department": "교양(글로벌문화와제2외국어)",
     "level": 1, "professor": "이승영", "time": "월 3 수 4"},
    {"code": "0000-1-2950-01", "name": "초급중국어1", "department": "교양(글로벌문화와제2외국어)",
     "level": 1, "professor": "곡효운", "time": "월 2 수 1"},
    {"code": "0000-1-3812-01", "name": "스페인어1", "department": "교양(글로벌문화와제2외국어)",
     "level": 1, "professor": "조지 부르고스", "time": "금 5,6"},
    {"code": "0000-1-5688-01", "name": "일본문화읽기", "department": "교양(글로벌문화와제2외국어)",
     "level": 1, "professor": "권혁인", "time": "화 6 목 5 (TBL강의)"},

    # ===== 예술과체육 =====
    {"code": "0000-1-1618-01", "name": "축구", "department": "교양(예술과체육)",
     "level": 1, "professor": "선세영", "time": "월 1,2 (소규모강의)"},
    {"code": "0000-1-5683-01", "name": "요가", "department": "교양(예술과체육)",
     "level": 1, "professor": "문경림", "time": "금 3,4 (소규모강의)"},
    {"code": "0000-1-3814-01", "name": "영화의이해", "department": "교양(예술과체육)",
     "level": 1, "professor": "유창연", "time": "월 1 수 2"},
    {"code": "0000-2-5902-01", "name": "디자인과창의성", "department": "교양(예술과체육)",
     "level": 2, "professor": "이보용", "time": "금 1,2"},
    {"code": "0000-3-3200-01", "name": "운동과건강", "department": "교양(예술과체육)",
     "level": 3, "professor": "김혜련", "time": "목 3,4"},

    # ===== 수리와자연(수학) =====
    {"code": "0000-1-4625-01", "name": "대학수학및연습1", "department": "교양(수리와자연-수학)",
     "level": 1, "professor": "김순영 외", "time": "월 3 (원격50%이상)"},
    {"code": "0000-1-5928-01", "name": "인문사회계를위한미분적분학", "department": "교양(수리와자연-수학)",
     "level": 1, "professor": "김소영", "time": "금 3,4"},
    {"code": "0000-2-4969-01", "name": "공학수학1", "department": "교양(수리와자연-수학)",
     "level": 2, "professor": "돌지", "time": "월 3 수 4"},
    {"code": "0000-3-0819-03", "name": "선형대수학", "department": "교양(수리와자연-수학)",
     "level": 3, "professor": "박철수", "time": "월 5 수 6"},
    {"code": "0000-3-1942-02", "name": "확률및통계", "department": "교양(수리와자연-수학)",
     "level": 3, "professor": "김계완", "time": "월 2 수 1"},

    # ===== 수리와자연(물리) =====
    {"code": "0000-1-3414-01", "name": "대학물리및실험1", "department": "교양(수리와자연-물리)",
     "level": 1, "professor": "김성현", "time": "월 2 수 1,2"},
    {"code": "0000-1-9753-01", "name": "대학물리학1", "department": "교양(수리와자연-물리)",
     "level": 1, "professor": "박미은", "time": "원격수업100%"},

    # ===== 수리와자연(화학) =====
    {"code": "0000-1-1223-01", "name": "일반화학및실험1", "department": "교양(수리와자연-화학)",
     "level": 1, "professor": "손성윤", "time": "월 4 수 3"},
    {"code": "0000-1-7466-01", "name": "대학화학", "department": "교양(수리와자연-화학)",
     "level": 1, "professor": "사영진", "time": "원격수업100%"},

    # ===== 기초학문융합 =====
    {"code": "0000-2-6454-01", "name": "데이터과학을위한이산수학", "department": "교양(기초학문융합)",
     "level": 2, "professor": "최윤철", "time": "월 5 (원격50%이상)"},
    {"code": "0000-3-7728-01", "name": "디지털사회를위한데이터분석", "department": "교양(기초학문융합)",
     "level": 3, "professor": "민영호", "time": "화 5 목 6"},
    {"code": "0000-3-8120-01", "name": "정보사회와수학", "department": "교양(기초학문융합)",
     "level": 3, "professor": "김영희", "time": "월 2 (원격50%이상)"},
]


COURSES = MAJOR_COURSES + GENERAL_COURSES

# 학점 예외 목록 (기본값 3학점)
_CREDIT_EXCEPTIONS = {
    "I020-1-8101-01": 2, "I020-2-8086-01": 2,
    "I020-2-8482-01": 1, "I020-3-3704-01": 1, "I020-3-3831-01": 1,
    "I030-1-8998-01": 1, "I030-2-8484-01": 2,
    "I030-4-3683-01": 2, "I030-4-3685-01": 2,
    "I060-1-4278-01": 2, "I060-1-4287-01": 2,
}

# 각 과목에 검색용 요일/교시 토큰 및 학점을 미리 계산해서 추가
for _course in COURSES:
    _course["schedule"] = parse_schedule(_course["time"])
    _course["credit"] = _CREDIT_EXCEPTIONS.get(_course["code"], 3)
