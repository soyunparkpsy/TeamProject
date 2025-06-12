import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# CSV 데이터 불러오기
df = pd.read_csv("income_percentile.csv")  # 'income' 열과 'percentile' 열이 있다고 가정

# 헤더
st.title("💰 나의 소득 백분위 계산기")
st.markdown("당신의 연봉은 다른 사람들 사이에서 얼마나 높은 수준일까요? 👀")

# 드롭다운용 옵션 생성 (3,000만원 ~ 2억원까지 500만원 단위)
income_options = list(range(3000, 20001, 500))
selected_income = st.selectbox("📌 당신의 소득은 얼마인가요?", income_options)
user_income = selected_income * 10000  # 만원 → 원 변환

# 가장 가까운 소득 데이터 찾기
nearest_row = df.iloc[(df['income'] - user_income).abs().argsort()[:1]]
percentile = int(nearest_row['percentile'].values[0])

# 결과 출력
st.subheader(f"🎉 당신은 상위 **{100 - percentile}%**에 해당합니다!")
st.markdown("👏 대단해요! 전국 소득 분포에서 높은 수준이에요.")

# 시각화
fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(df['income'], df['percentile'], label="전체 소득 분포", linewidth=2)
ax.axvline(user_income, color='red', linestyle='--', label="📍 나의 위치")
ax.set_xlabel("연간 소득 (원)")
ax.set_ylabel("백분위 (%)")
ax.set_title("📊 소득 위치 시각화")
ax.legend()
st.pyplot(fig)
