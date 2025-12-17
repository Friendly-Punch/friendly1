import streamlit as st
import pandas as pd

# タイトル
st.title("資産形成シミュレーション")

# ユーザー入力
monthly = st.number_input("毎月の積立額（円）", min_value=1000, step=1000, value=50000)
years = st.number_input("積立年数", min_value=1, step=1, value=30)
rate = st.slider("年率（%）", 0.0, 10.0, 5.0)

# 計算処理（年次で集計）
months_total = int(years * 12)
r_month = rate / 100 / 12  # 月利

# 最終値（表示用）
if r_month > 0:
    future_value = monthly * ((1 + r_month) ** months_total - 1) / r_month
else:
    future_value = monthly * months_total
principal = monthly * months_total
gain = future_value - principal

st.write(f"総積立額（元本）：{principal:,.0f} 円")
st.write(f"運用後の資産額：{future_value:,.0f} 円")

# 年次データの作成（複利は月次で更新 → 毎年末だけ抜き出し）
years_list = list(range(1, int(years) + 1))
principal_yearly = []
value_yearly = []

value = 0.0
for y in years_list:
    # その年の12か月分を月次で更新
    for _ in range(12):
        value = value * (1 + r_month) + monthly
    principal_yearly.append(monthly * 12 * y)
    value_yearly.append(value)

df = pd.DataFrame({
    "年数": years_list,
    "元本累計": principal_yearly,
    "運用後資産": value_yearly
})

st.subheader("年ごとの資産推移")
st.line_chart(df.set_index("年数"))

# 参考：表も見たい場合
with st.expander("年次データの詳細を見る"):
    st.dataframe(df.style.format({"元本累計": "{:,.0f}", "運用後資産": "{:,.0f}"}))