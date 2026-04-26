import streamlit as st
import pandas as pd

# ==========================================
# 필수 조건 1. 학번과 이름 (코드 상단에서 쉽게 수정 가능)
# ==========================================
STUDENT_ID = "20240001"
STUDENT_NAME = "홍길동"

# ==========================================
# 필수 조건 3. Streamlit 캐싱을 활용한 데이터 로드
# ==========================================
@st.cache_data
def load_data():
    try:
        # data/quiz_data.csv 파일을 불러옵니다.
        df = pd.read_csv("data/quiz_data.csv")
        return df
    except FileNotFoundError:
        st.error("데이터 파일을 찾을 수 없습니다. data/quiz_data.csv 파일이 있는지 확인해주세요.")
        return pd.DataFrame()

# ==========================================
# 필수 조건 2. 로그인 기능
# ==========================================
def login():
    st.subheader("로그인")
    
    # 아이디 / 비밀번호 입력
    username = st.text_input("아이디")
    password = st.text_input("비밀번호", type="password")
    
    if st.button("로그인"):
        # 간단한 로그인 성공/실패 처리
        if username == "admin" and password == "1234":
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
            st.success("로그인 성공!")
            st.rerun()
        else:
            st.error("로그인 실패: 아이디 또는 비밀번호가 올바르지 않습니다.")

# ==========================================
# 필수 조건 4. 퀴즈 기능 및 메인 앱 로직
# ==========================================
def main():
    # 필수 조건 1. 첫 화면에 학번과 이름 명시
    st.title("비밀 보관력 테스트 🤫")
    st.markdown(f"**학번:** {STUDENT_ID} | **이름:** {STUDENT_NAME}")
    st.divider()

    # 로그인 상태 구분 (세션 상태 관리)
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    if not st.session_state["logged_in"]:
        login()
        return

    # 로그인 성공 후 화면
    st.sidebar.success(f"환영합니다, {st.session_state['username']}님!")
    if st.sidebar.button("로그아웃"):
        st.session_state["logged_in"] = False
        st.rerun()

    # 퀴즈 데이터 불러오기
    df = load_data()
    if df.empty:
        return

    # 퀴즈 진행 상태 관리를 위한 세션 초기화
    if "current_q" not in st.session_state:
        st.session_state["current_q"] = 0
    if "total_score" not in st.session_state:
        st.session_state["total_score"] = 0

    # 문제 제시 및 사용자 응답 입력
    if st.session_state["current_q"] < len(df):
        row = df.iloc[st.session_state["current_q"]]
        st.subheader(f"Q{row['id']}. {row['question']}")
        
        # 3가지 옵션 보기
        options = [row['option1'], row['option2'], row['option3']]
        choice = st.radio("당신의 선택은?", options, index=None)
        
        if st.button("다음 문제로"):
            if choice is None:
                st.warning("선택지를 골라주세요!")
            else:
                # 점수 계산 후 세션에 저장
                idx = options.index(choice)
                score_col = f"score{idx+1}"
                st.session_state["total_score"] += row[score_col]
                st.session_state["current_q"] += 1
                st.rerun()
    else:
        # 최종 결과 확인 (점수 합산 및 3가지 유형 분류)
        st.subheader("테스트 결과")
        final_score = st.session_state["total_score"]
        st.write(f"당신의 총 점수는 **{final_score}점** 입니다!")
        
        if final_score >= 25:
            st.success("유형 A: 무덤까지 가져가는 '비밀 금고' 🔒")
            st.info("당신은 친구들이 가장 믿고 의지할 수 있는 최고의 비밀 보관자입니다!")
        elif final_score >= 15:
            st.warning("유형 B: 적당히 지키는 '필터형 보관자' 🤔")
            st.info("비밀을 잘 지키려 노력하지만, 때로는 친한 사람에게 흘리기도 하네요.")
        else:
            st.error("유형 C: 동네방네 소문내는 '인간 확성기' 📢")
            st.info("당신에게 비밀을 말하는 건 위험할지도 모르겠어요! 입단속이 필요합니다.")
            
        # 다시하기 버튼
        if st.button("처음부터 다시 하기"):
            st.session_state["current_q"] = 0
            st.session_state["total_score"] = 0
            st.rerun()

if __name__ == "__main__":
    main()
