import streamlit as st
import pandas as pd

# 데이터 불러오기
df = pd.read_csv("국세청_근로소득 백분위(천분위) 자료_20241231.csv", encoding='cp949')

# 사용자 입력
st.title("근로소득 백분위 비교 대시보드")
user_income = st.number_input("당신의 연간 근로소득 (단위: 원)", min_value=0)

if user_income > 0:
    income_억 = user_income / 100_000_000

    # 해당 소득 이하인 구간 찾기
    match = df[df['근로소득금액'] <= income_억].head(1)

    if not match.empty:
        rank = match.iloc[0]['구분']
        st.success(f"당신은 '{rank}' 이내의 근로소득자입니다.")
    else:
        st.success("당신은 상위 0.1%보다 높은 소득자입니다.")
