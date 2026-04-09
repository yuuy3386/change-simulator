import streamlit as st

st.set_page_config(page_title="おつりシミュレーション", layout="wide")

st.title("おつりシミュレーション")

# -------------------------
# 商品データ
# -------------------------
menu = {
    "ビーフ": 230,
    "メンチ": 380,
    "牛すじ": 300,
    "和風だし": 180,
    "明太クリーミー": 300,
    "チーズ": 300,
    "かにクリーム": 300,
    "かぼちゃ": 270,
    "常総牛": 630,
}

# -------------------------
# セット価格（固定）
# -------------------------
set_prices = {
    "3点セット": 900,
    "4点セット": 1200,
    "お得セット": 1400,
    "お土産セット": 1000
}

# 初期化
if "cart" not in st.session_state:
    st.session_state.cart = {}

# -------------------------
# 商品選択（スマホ対応2列）
# -------------------------
st.subheader("商品を選択")

cols = st.columns(2)

for i, (name, price) in enumerate(menu.items()):
    with cols[i % 2]:
        if st.button(f"{name} {price}円", use_container_width=True):
            st.session_state.cart[name] = st.session_state.cart.get(name, 0) + 1

# -------------------------
# セットメニュー
# -------------------------
st.subheader("セットメニュー")

cols = st.columns(2)

for i, set_name in enumerate(set_prices.keys()):
    with cols[i % 2]:
        if st.button(f"{set_name} {set_prices[set_name]}円", use_container_width=True):
            st.session_state.cart[set_name] = set_prices[set_name]

# -------------------------
# 注文内容
# -------------------------
st.subheader("注文内容")

total = 0

for item, value in st.session_state.cart.items():
    if item in menu:
        price = menu[item]
        subtotal = price * value
        st.write(f"{item} ×{value}：{subtotal}円")
        total += subtotal
    else:
        st.write(f"{item}：{value}円")
        total += value

st.write("---")
st.subheader(f"合計：{total}円")

# -------------------------
# お会計
# -------------------------
st.subheader("お会計")

mode = st.radio("モード選択", ["練習モード", "自動計算モード"])

money = st.number_input("預かり金額", min_value=0, step=10)

if mode == "自動計算モード":
    change = money - total
    st.subheader(f"おつり：{change}円")
