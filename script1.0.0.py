import streamlit as st
import pandas as pd

# タイトル
st.title("資産形成シミュレーション")

# ユーザー入力
monthly = st.number_input("毎月の積立額（円）", min_value=1000, step=1000, value=50000)
years = st.number_input("積立年数", min_value=1, step=1, value=30)

rate = st.slider("年率（%）", 0.0, 10.0, 5.0)
# 投資初心者向けの参考情報を追加
st.caption(
    "参考：日本株の平均利回りはおおよそ3〜5％程度です "
    "（[東証統計](https://www.jpx.co.jp/markets/statistics-equities/misc/03.html)、"
    "[日経平均益利回り](https://stock-marketdata.com/earnings-yield-nikkei225.html)）"
)

# 計算処理
months_total = int(years * 12)
r_month = rate / 100 / 12

if r_month > 0:
    future_value = monthly * ((1 + r_month) ** months_total - 1) / r_month
else:
    future_value = monthly * months_total
principal = monthly * months_total
gain = future_value - principal

# 結果表示
st.write(f"総積立額（元本）：{principal:,.0f} 円")
st.write(f"運用益：{gain:,.0f} 円")
st.write(f"運用後の資産額：{future_value:,.0f} 円")

# 年次データ作成
years_list = list(range(1, int(years) + 1))
principal_yearly, value_yearly = [], []
value = 0.0
for y in years_list:
    for _ in range(12):
        value = value * (1 + r_month) + monthly
    principal_yearly.append(monthly * 12 * y)
    value_yearly.append(value)

df = pd.DataFrame({
    "年数": years_list,
    "元本累計": principal_yearly,
    "運用後資産": value_yearly
})

# グラフ表示
st.subheader("年ごとの資産推移")
st.line_chart(df.set_index("年数"))

# 詳細データを展開表示
with st.expander("年次データの詳細を見る"):
    st.dataframe(df.style.format({"元本累計": "{:,.0f}", "運用後資産": "{:,.0f}"}))