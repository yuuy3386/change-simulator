import streamlit as st
from collections import Counter
import streamlit.components.v1 as components

st.set_page_config(page_title="おつりシミュレーション", layout="wide")

# ----------------------
# タイトル（スマホ対応）
# ----------------------
st.markdown(
    "<h3 style='margin-bottom:10px;'>おつりシミュレーション</h3>",
    unsafe_allow_html=True
)

# ----------------------
# 画面幅取得（スマホ判定）
# ----------------------
components.html(
    """
    <script>
    const width = window.innerWidth;
    window.parent.postMessage({width: width}, "*");
    </script>
    """,
    height=0,
)

if "width" not in st.session_state:
    st.session_state.width = 1000

# 列数切り替え
if st.session_state.width < 768:
    cols = st.columns(1)
else:
    cols = st.columns(3)

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
# 商品選択
# ----------------------
st.subheader("商品を選択")

for i, (name, price) in enumerate(menu.items()):
    with cols[i % len(cols)]:
        if st.button(f"{name} {price}円", key=name, use_container_width=True):
            st.session_state.cart[name] = st.session_state.cart.get(name, 0) + 1

# ----------------------
# セットメニュー
# ----------------------
st.subheader("セットメニュー")

set_items = {
    "3点セット": ["ビーフ", "メンチ", "牛すじ"],
    "4点セット": ["ビーフ", "メンチ", "牛すじ", "明太クリーミー"],
    "お得セット": ["ビーフ", "ビーフ", "ビーフ", "メンチ", "メンチ"],
    "お土産セット": ["ビーフ", "和風だし", "常総牛"]
}

set_prices = {
    "3点セット": 900,
    "4点セット": 1200,
    "お得セット": 1400,
    "お土産セット": 1000
}

for i, set_name in enumerate(set_items.keys()):
    with cols[i % len(cols)]:
        if st.button(f"{set_name} {set_prices[set_name]}円", key=f"set_{set_name}", use_container_width=True):
            for item in set_items[set_name]:
                st.session_state.cart[item] = st.session_state.cart.get(item, 0) + 1

# ----------------------
# セット自動判定
# ----------------------
cart = st.session_state.cart.copy()
sets_result = []

# お得セット
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
# 表示（見やすい版）
# ----------------------
st.subheader("注文内容")

original = Counter(st.session_state.cart)

# 元注文
if any(original.values()):
    st.markdown("### 🧾 注文（入力）")
    for name, count in original.items():
        if count > 0:
            st.write(f"{name} ×{count}")

# セット
if sets_result:
    st.markdown("### 🎁 セット")
    count_sets = Counter(sets_result)

    for name, count in count_sets.items():
        if name == "お得セット":
            st.write(f"{name} ×{count}（ビーフ×3・メンチ×2）")
        elif name == "4点セット":
            st.write(f"{name} ×{count}（ビーフ・メンチ・牛すじ・明太）")
        elif name == "3点セット":
            st.write(f"{name} ×{count}（ビーフ・メンチ・牛すじ）")

# 単品
if any(cart.values()):
    st.markdown("### 🛒 単品")
    for name, count in cart.items():
        if count > 0:
            st.write(f"{name} ×{count}")

# ----------------------
# 合計
# ----------------------
total = 0

for s in sets_result:
    total += set_prices[s]

for name, count in cart.items():
    total += menu[name] * count

st.markdown("---")
st.markdown(f"## 合計：{total}円")
