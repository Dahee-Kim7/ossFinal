# 전공/교양 과목 추천 웹 애플리케이션

광운대학교 2026-1학기 강의시간표 데이터를기반으로, 
5개 학과/교양 영역과 난이도, 요일·교시를 입력하면 해당하는 과목들을 보여주는
Streamlit + FastAPI 기반 웹 애플리케이션입니다. 
회원가입/로그인, 이미 수강한 과목 관리, 저장한 강의(찜 목록) 기능을 포함합니다.

## 구조
 
+ back                
  + main.py           
  + db.py             
  + courses.py        
  + requirements.txt
  + Dockerfile
  + data            
+ front              
  + app.py            
  + requirements.txt
  + Dockerfile
+ docker-compose.yml
+ .gitignore
