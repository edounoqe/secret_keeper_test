import streamlit as st
import pandas as pd

# ==========================================
# 1. 제출자 정보 
# ==========================================
STUDENT_ID = "20240001"   # 학번을 여기에 입력하세요
STUDENT_NAME = "홍길동"      # 이름을 여기에 입력하세요

# ==========================================
# 2. 데이터 로드 및 캐싱 기능
# ==========================================
@st.cache_data
def load_quiz_data():
    """
    data/quiz_data.csv 파일에서 퀴즈 데이터를 불러옵니다.
    @st.cache_data 데코레이터를 사용하여 매번 파일을 읽지 않고 캐싱된 데이터를 반환합니다.
    """
    try:
        df = pd.read_csv("data/quiz_data.csv")
        return df
    except FileNotFoundError:
        st.error("데이터 파일을 찾을 수 없습니다. data/quiz_data.csv 파일이 있는지 확인해주세요.")
        return pd.DataFrame()

# ==========================================
# 결과 정보 (유형별 설명)
# ==========================================
RESULT_TYPES = {
    "TYPE_C": {
        "name": "공유 본능형",
        "description": "당신은 알게 된 이야기를 혼자 간직하기보다는 다른 사람들과 나누고 싶어 하는 성향이 강합니다. 사람들과 소통하는 것을 즐기고 이야기의 중심이 되는 것을 좋아합니다.",
        "advantage": "뛰어난 정보 전달력과 사교성으로 분위기 메이커 역할을 합니다.",
        "caution": "다른 사람의 민감한 정보가 퍼져나가 오해를 사거나 신뢰를 잃을 수 있습니다. 이야기하기 전에 한 번 더 생각하는 습관이 중요합니다.",
        "advice": "\"이 이야기가 당사자에게 상처가 되지는 않을까?\" 한 번 더 고민해 보세요!"
    },
    "TYPE_B": {
        "name": "상황 판단형",
        "description": "당신은 비밀을 지켜야 할 때와 그렇지 않을 때를 눈치껏 구분하는 사람입니다. 대체로 말을 아끼지만, 아주 친한 사람이나 특정 상황에서는 유연하게 대화에 참여합니다.",
        "advantage": "융통성이 있으며, 적절한 선에서 소통과 보안을 유지할 줄 압니다.",
        "caution": "본인의 기준과 당사자의 기준이 다를 때 갈등이 생길 수 있습니다. '이 정도는 괜찮겠지'라는 생각에 주의하세요.",
        "advice": "나의 판단 기준보다는 '비밀을 말한 사람'의 입장을 먼저 고려해 보세요!"
    },
    "TYPE_A": {
        "name": "신뢰 금고형",
        "description": "당신은 타인의 비밀과 개인정보를 무엇보다 중요하게 생각하는 최고의 비밀 보관자입니다. 한 번 들은 이야기는 절대 다른 곳으로 새어나가지 않습니다.",
        "advantage": "주변 사람들로부터 깊은 신뢰를 받으며, 무거운 고민도 안심하고 털어놓을 수 있는 든든한 친구입니다.",
        "caution": "타인의 무거운 비밀까지 모두 혼자 짊어지려다 보면 감정적인 스트레스가 쌓일 수 있습니다.",
        "advice": "다른 사람의 비밀을 지키는 것만큼 당신 자신의 마음 건강을 챙기는 것도 잊지 마세요!"
    }
}

def get_result_type(score):
    if score <= 35:
        return RESULT_TYPES["TYPE_C"]
    elif score <= 70:
        return RESULT_TYPES["TYPE_B"]
    else:
        return RESULT_TYPES["TYPE_A"]

# ==========================================
# 메인 애플리케이션 함수
# ==========================================
def main():
    # 1. 첫 화면 구성
    st.title("비밀 보관력 테스트")
    st.subheader("나는 얼마나 신중하게 말을 아끼는 사람일까?")
    
    st.markdown(f"**제출자:** {STUDENT_ID} {STUDENT_NAME}")
    st.markdown("이 앱은 다양한 상황에서 당신이 어떻게 반응하는지를 통해 **비밀 보관 능력**을 진단해 주는 테스트입니다. 간단한 퀴즈를 풀고 나의 유형을 알아보세요!")
    st.divider()

    # 2. 로그인 기능
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    if not st.session_state["logged_in"]:
        st.markdown("### 로그인")
        with st.form("login_form"):
            username = st.text_input("아이디")
            password = st.text_input("비밀번호", type="password")
            submitted = st.form_submit_button("로그인")
            
            if submitted:
                # 미리 정의된 로그인 정보와 비교
                if username == "student" and password == "1234":
                    st.session_state["logged_in"] = True
                    st.success("로그인 성공!")
                    st.rerun()
                else:
                    st.error("오류: 아이디 또는 비밀번호가 일치하지 않습니다.")
        return  # 로그인 전에는 퀴즈가 보이지 않게 처리

    # 로그인 후 화면 (로그아웃 처리)
    st.sidebar.success("로그인 상태입니다.")
    if st.sidebar.button("로그아웃"):
        st.session_state.clear()
        st.rerun()

    # 데이터 로드 및 캐싱 안내 멘트
    st.info("퀴즈 데이터는 캐싱을 통해 불러옵니다.")
    
    df = load_quiz_data()
    if df.empty:
        return

    # 결과 분석 상태 보존 (퀴즈 제출 후 결과창 유지)
    if "quiz_submitted" not in st.session_state:
        st.session_state["quiz_submitted"] = False
    
    # 4. 퀴즈 기능
    if not st.session_state["quiz_submitted"]:
        st.markdown("### 📝 모든 질문에 답하고 제출해주세요")
        
        # 사용자 응답을 저장할 딕셔너리
        user_answers = {}
        
        with st.form("quiz_form"):
            for idx, row in df.iterrows():
                question_num = idx + 1
                question_text = row["question"]
                
                # 선택지와 점수 매핑을 위해 튜플 리스트 형성
                options = [
                    (row["option_1"], row["score_1"]),
                    (row["option_2"], row["score_2"]),
                    (row["option_3"], row["score_3"])
                ]
                
                # 선택지만 추출하여 라디오 버튼 생성
                option_texts = [opt[0] for opt in options]
                
                st.markdown(f"**Q{question_num}. {question_text}**")
                # 사용자가 선택한 라디오 버튼의 값 저장
                selected_option = st.radio(
                    f"Q{question_num} options", 
                    option_texts, 
                    index=None,
                    label_visibility="collapsed",
                    key=f"q_{question_num}"
                )
                
                # 선택된 텍스트로 어떤 점수인지 파악을 위해 저장
                user_answers[question_num] = {
                    "selected": selected_option,
                    "options": options
                }
                st.write("") # 간격 띄우기
                
            submitted = st.form_submit_button("제출")
            
            if submitted:
                # 모든 항목을 선택했는지 검증
                unanswered = [str(q) for q, data in user_answers.items() if data["selected"] is None]
                if unanswered:
                    st.warning(f"아직 답변하지 않은 문항이 있습니다. (문항: {', '.join(unanswered)})")
                else:
                    # 총점 계산
                    total_score = 0
                    for q, data in user_answers.items():
                        selected_text = data["selected"]
                        # 선택된 텍스트와 매칭되는 점수 찾기
                        for opt_text, opt_score in data["options"]:
                            if opt_text == selected_text:
                                total_score += int(opt_score)
                                break
                    
                    st.session_state["total_score"] = total_score
                    st.session_state["quiz_submitted"] = True
                    st.rerun()
    
    # 5 & 6. 결과 화면
    else:
        st.markdown("### 📊 테스트 결과")
        
        score = st.session_state["total_score"]
        result = get_result_type(score)
        
        # 총점 및 유형명 표시
        st.success(f"당신의 총점: **{score}점** / 100점")
        st.subheader(f"유형명: {result['name']}")
        
        # 결과 상세 정보
        st.markdown(f"**유형 설명:** {result['description']}")
        
        col1, col2 = st.columns(2)
        with col1:
            st.info(f"**장점:** {result['advantage']}")
        with col2:
            st.warning(f"**조심할 점:** {result['caution']}")
            
        st.markdown(f"> **한 줄 조언:** {result['advice']}")
        st.write("")
        
        # 다시 하기 버튼
        if st.button("다시 테스트하기"):
            st.session_state.clear()
            st.rerun()

if __name__ == "__main__":
    main()
