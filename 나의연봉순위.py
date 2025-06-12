import streamlit as st
import pandas as pd

# 데이터 불러오기
df = pd.read_csv("국세청_근로소득 백분위(천분위) 자료_20241231.csv", encoding='cp949')

# 제목
st.title("근로소득 백분위 비교 대시보드")

# 입력 안내
st.markdown("### 📌 당신의 연간 총급여(연봉)을 입력하세요 (단위: **만원**)")
user_income_million = st.number_input("예: 5000만원", min_value=0)

# 계산
if user_income_million > 0:
    income_억 = user_income_million / 10_000  # 만원 → 억원 변환

    match = df[df['근로소득금액'] <= income_억].head(1)

    if not match.empty:
        rank = match.iloc[0]['구분']
        st.success(f"🎉 당신은 '{rank}' 이내의 근로소득자입니다.")
    else:
        st.success("🎉 당신은 상위 0.1%보다 높은 소득자입니다.")
