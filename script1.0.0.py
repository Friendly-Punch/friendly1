import streamlit as st
import pandas as pd

st.title("資産形成シミュレーション")

# モード切替
mode = st.radio("モード選択", ["通常シミュレーション", "逆算シミュレーション"])

rate = st.slider("年率（%）", 0.0, 10.0, 5.0)
st.caption("参考：日本株の平均利回りはおおよそ3〜5％程度です "
           "（[東証統計](https://www.jpx.co.jp/markets/statistics-equities/misc/03.html)、"
           "[日経平均益利回り](https://stock-marketdata.com/earnings-yield-nikkei225.html)）")

r_month = rate / 100 / 12

# 通常シミュレーション
if mode == "通常シミュレーション":
    monthly = st.number_input("毎月の積立額（円）", min_value=1000, step=1000, value=50000)
    years = st.number_input("積立年数", min_value=1, step=1, value=30)
    start_age = st.number_input("開始年齢", min_value=18, step=1, value=30)
    months_total = years * 12

    if r_month > 0:
        future_value = monthly * ((1 + r_month) ** months_total - 1) / r_month
    else:
        future_value = monthly * months_total
    principal = monthly * months_total
    gain = future_value - principal

    st.write(f"総積立額（元本）：{principal:,.0f} 円")
    st.write(f"運用益：{gain:,.0f} 円")
    st.write(f"運用後の資産額：{future_value:,.0f} 円")

    # 年齢軸データ作成
    ages = list(range(start_age + 1, start_age + years + 1))
    principal_yearly, value_yearly = [], []
    value = 0.0
    for y in range(years):
        for _ in range(12):
            value = value * (1 + r_month) + monthly
        principal_yearly.append(monthly * 12 * (y + 1))
        value_yearly.append(value)

    df = pd.DataFrame({"年齢": ages, "元本累計": principal_yearly, "運用後資産": value_yearly})

    # 目標ライン表示オプション
    show_target = st.checkbox("目標ラインを表示する")
    if show_target:
        target_line = st.number_input("目標額（円）", min_value=100000, step=100000, value=10000000)
        df["目標ライン"] = target_line

    st.subheader("年齢ごとの資産推移")
    st.line_chart(df.set_index("年齢"))

    # 表を任意表示
    show_table = st.checkbox("年齢ごとの資産表を表示する")
    if show_table:
        st.dataframe(df.style.format({"元本累計": "{:,.0f}", "運用後資産": "{:,.0f}"}))

# 逆算シミュレーション
else:
    target = st.number_input("目標額（円）", min_value=100000, step=100000, value=10000000)
    years_target = st.number_input("目標達成までの年数", min_value=1, step=1, value=20)
    months_target = years_target * 12

    if r_month > 0:
        monthly_required = target * r_month / ((1 + r_month) ** months_target - 1)
    else:
        monthly_required = target / months_target

    st.write(f"目標額 {target:,.0f} 円 を {years_target} 年で達成するには、")
    st.write(f"毎月 **{monthly_required:,.0f} 円** の積立が必要です。")