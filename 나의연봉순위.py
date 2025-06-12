import streamlit as st
import pandas as pd

# 데이터 불러오기
# 'encoding'을 'utf-8'로 변경하거나, cp949 인코딩 에러 발생 시 'latin1' 등으로 시도해보세요.
# df = pd.read_csv("국세청_근로소득 백분위(천분위) 자료_20241231.csv", encoding='cp949')

# 예시 데이터 (실제 데이터와 구조가 유사하다고 가정)
# 실제 데이터를 사용할 때는 위의 주석 처리된 라인을 사용하세요.
data = {
    '구분': ['0.1%', '0.2%', '0.3%', '0.4%', '0.5%', '0.6%', '0.7%', '0.8%', '0.9%', '1.0%',
             '2%', '3%', '4%', '5%', '6%', '7%', '8%', '9%', '10%', '20%', '30%', '40%',
             '50%', '60%', '70%', '80%', '90%', '100%'],
    '근로소득금액': [3.0, 2.8, 2.6, 2.4, 2.2, 2.0, 1.8, 1.6, 1.4, 1.2,
                     1.0, 0.8, 0.7, 0.6, 0.55, 0.5, 0.45, 0.4, 0.35, 0.3, 0.25, 0.2,
                     0.15, 0.1, 0.08, 0.05, 0.03, 0.01] # 억원 단위
}
df = pd.DataFrame(data)


# '구분' 컬럼을 숫자로 변환 (예: '0.1%' -> 0.001, '10%' -> 0.1)
# 숫자로 변환할 수 없는 값 (예: '100%')은 그대로 두어 나중에 처리
def convert_percent_to_float(percent_str):
    try:
        return float(percent_str.replace('%', '')) / 100
    except ValueError:
        return percent_str # 변환할 수 없는 경우 원본 문자열 반환

df['구분_float'] = df['구분'].apply(convert_percent_to_float)


# 제목
st.title("근로소득 백분위 비교 대시보드")

# 입력 안내
st.markdown("### 📌 당신의 연간 총급여(연봉)을 입력하세요 (단위: **만원**)")
user_income_million = st.number_input("예: 5000만원", min_value=0)

# 계산
if user_income_million > 0:
    income_억 = user_income_million / 10_000  # 만원 → 억원 변환

    # 사용자의 소득이 데이터프레임의 최대 소득보다 높은 경우
    if income_억 >= df['근로소득금액'].max():
        st.success("🎉 당신은 상위 0.1%보다 높은 소득자입니다!")
    # 사용자의 소득이 데이터프레임의 최소 소득보다 낮은 경우
    elif income_억 < df['근로소득금액'].min():
        st.success("😔 당신은 하위 소득 구간에 해당합니다.")
    else:
        # 가장 가까운 상위 소득 구간 찾기 (소득금액이 높은 것부터 낮은 것으로 정렬)
        # 즉, '근로소득금액'이 사용자의 소득보다 크거나 같은 경우 중 가장 작은 값을 찾음
        df_sorted = df.sort_values(by='근로소득금액', ascending=False).reset_index(drop=True)

        found_rank = False
        for i in range(len(df_sorted)):
            # 현재 구간의 소득
            current_income_threshold = df_sorted.loc[i, '근로소득금액']
            # 현재 구간의 백분위 (숫자로 변환된 값)
            current_percentile_float = df_sorted.loc[i, '구분_float']

            # 다음 구간이 있다면 다음 구간의 소득
            next_income_threshold = None
            next_percentile_float = None
            if i + 1 < len(df_sorted):
                next_income_threshold = df_sorted.loc[i + 1, '근로소득금액']
                next_percentile_float = df_sorted.loc[i + 1, '구분_float']

            # 사용자의 소득이 현재 구간의 소득보다 크거나 같고, 다음 구간의 소득보다 작은 경우
            # (즉, 현재 구간과 다음 구간 사이에 소득이 있는 경우)
            if user_income_million >= current_income_threshold * 10000 and (next_income_threshold is None or user_income_million < next_income_threshold * 10000):
                # 백분위를 숫자로 처리할 수 있는 경우
                if isinstance(current_percentile_float, float) and isinstance(next_percentile_float, float):
                    # 선형 보간법을 사용하여 정확한 백분위 계산
                    # (user_income - next_income_threshold) / (current_income_threshold - next_income_threshold)
                    # * (current_percentile_float - next_percentile_float) + next_percentile_float

                    # 보간을 통해 정확한 백분위를 계산할 수 있도록 로직 수정
                    if current_income_threshold == next_income_threshold: # 분모가 0이 되는 경우 방지
                        exact_percentile = current_percentile_float
                    else:
                        interpolation_factor = (user_income_million - next_income_threshold * 10000) / \
                                               (current_income_threshold * 10000 - next_income_threshold * 10000)
                        exact_percentile = next_percentile_float + (interpolation_factor * (current_percentile_float - next_percentile_float))
                    
                    st.success(f"🎉 당신은 근로소득 상위 약 **{exact_percentile:.2%}** 이내의 소득자입니다.")
                    found_rank = True
                    break
                else: # '100%'와 같이 숫자로 변환되지 않는 마지막 구간
                    st.success(f"🎉 당신은 '{df_sorted.loc[i, '구분']}' 이내의 근로소득자입니다.")
                    found_rank = True
                    break

        if not found_rank:
            # 모든 구간을 찾아봤는데도 정확한 위치를 찾지 못했을 경우
            # (이 경우는 위의 `if/elif` 조건으로 대부분 커버되지만, 만약을 위해)
            st.info("입력하신 소득에 해당하는 정확한 백분위를 찾기 어렵습니다. 데이터를 다시 확인해주세요.")
