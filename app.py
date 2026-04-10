import streamlit as st
from collections import Counter

st.set_page_config(page_title="おつりシミュレーション", layout="wide")

st.title("おつりシミュレーション")

# ----------------------
# 商品データ
# ----------------------
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

# ----------------------
# セッション初期化
# ----------------------
if "cart" not in st.session_state:
    st.session_state.cart = {}

# ----------------------
# 商品選択（3列）
# ----------------------
st.subheader("商品を選択")

cols = st.columns(3)

for i, (name, price) in enumerate(menu.items()):
    with cols[i % 3]:
        if st.button(f"{name} {price}円", key=name, use_container_width=True):
            st.session_state.cart[name] = st.session_state.cart.get(name, 0) + 1

# ----------------------
# セット自動判定
# ----------------------
cart = st.session_state.cart.copy()
sets_result = []

# お得セット（ビーフ3＋メンチ2）
while cart.get("ビーフ", 0) >= 3 and cart.get("メンチ", 0) >= 2:
    cart["ビーフ"] -= 3
    cart["メンチ"] -= 2
    sets_result.append("お得セット")

# 4点セット
while (
    cart.get("ビーフ", 0) >= 1 and
    cart.get("メンチ", 0) >= 1 and
    cart.get("牛すじ", 0) >= 1 and
    cart.get("明太クリーミー", 0) >= 1
):
    cart["ビーフ"] -= 1
    cart["メンチ"] -= 1
    cart["牛すじ"] -= 1
    cart["明太クリーミー"] -= 1
    sets_result.append("4点セット")

# 3点セット
while (
    cart.get("ビーフ", 0) >= 1 and
    cart.get("メンチ", 0) >= 1 and
    cart.get("牛すじ", 0) >= 1
):
    cart["ビーフ"] -= 1
    cart["メンチ"] -= 1
    cart["牛すじ"] -= 1
    sets_result.append("3点セット")

# ----------------------
# 表示
# ----------------------
st.subheader("注文内容")

# セット表示
if sets_result:
    count_sets = Counter(sets_result)
    for name, count in count_sets.items():
        st.write(f"{name} ×{count}")

# 単品表示
for name, count in cart.items():
    if count > 0:
        st.write(f"{name} ×{count}")

# ----------------------
# 合計金額
# ----------------------
total = 0

# セット価格
set_prices = {
　　　"3点セット": 900,
    "4点セット": 1200,
     "お得セット": 1400,
    
}

for s in sets_result:
    total += set_prices[s]

# 単品
for name, count in cart.items():
    total += menu[name] * count

st.markdown("---")
st.markdown(f"## 合計：{total}円")
