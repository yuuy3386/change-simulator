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

# セットの中身
set_items = {
    "3点セット": ["ビーフ", "メンチ", "牛すじ"],
    "4点セット": ["ビーフ", "メンチ", "牛すじ", "明太クリーミー"],
    "お得セット": ["ビーフ", "ビーフ", "ビーフ", "メンチ", "メンチ"],
    "お土産セット": ["ビーフ", "和風だし", "常総牛"],
}

# セット価格
set_prices = {
    "3点セット": 900,
    "4点セット": 1200,
    "お得セット": 1400,
    "お土産セット": 1000,
}

# -------------------------
# 初期化
# -------------------------
if "cart" not in st.session_state:
    st.session_state.cart = {}

# -------------------------
# 商品選択
# -------------------------
st.subheader("商品を選択")

product_cols = st.columns(3)
for i, (name, price) in enumerate(menu.items()):
    with product_cols[i % 3]:
        if st.button(f"{name} {price}円", key=f"product_{name}"):
            st.session_state.cart[name] = st.session_state.cart.get(name, 0) + 1

# -------------------------
# セットメニュー
# -------------------------
st.subheader("セットメニュー")

set_cols = st.columns(4)
for i, set_name in enumerate(set_items.keys()):
    with set_cols[i % 4]:
        if st.button(set_name, key=f"set_{set_name}"):
            for item in set_items[set_name]:
                st.session_state.cart[item] = st.session_state.cart.get(item, 0) + 1

# -------------------------
# レイアウト
# -------------------------
left, right = st.columns([2, 1])

# -------------------------
# 注文内容
# -------------------------
with left:
    st.subheader("注文内容")

    total = 0
    order_counts = st.session_state.cart.copy()

    if not order_counts or all(qty == 0 for qty in order_counts.values()):
        st.write("商品を選んでください")
    else:
        for item, qty in order_counts.items():
            if qty > 0:
                price = menu[item] * qty
                total += price
                st.write(f"{item} ×{qty}：{price}円")

    st.markdown("---")
    st.subheader(f"合計：{total}円")

# -------------------------
# 会計
# -------------------------
with right:
    st.subheader("お会計")

    mode = st.radio("モード選択", ["練習モード", "自動計算モード"], key="calc_mode")

    money = st.number_input("預かり金額", min_value=0, step=10, key="money_input")
    change = money - total

    st.markdown("### おつり")

    if mode == "自動計算モード":
        if money == 0:
            st.write("未入力")
        elif change < 0:
            st.error(f"{abs(change)}円 不足")
        else:
            st.success(f"{change}円")
    else:
        user_change = st.number_input("おつりを入力（10円単位）", min_value=0, step=10, key="user_change")

        if st.button("答え合わせ", key="check_change"):
            if money == 0:
                st.warning("預かり金額を入力してください")
            elif change < 0:
                st.error("金額が不足しています")
            elif user_change == change:
                st.success("正解！")
            else:
                st.error(f"不正解：正しくは {change}円")

# -------------------------
# セット提案
# -------------------------
st.markdown("---")
st.subheader("セット提案")

suggestions = []

beef = order_counts.get("ビーフ", 0)
menchi = order_counts.get("メンチ", 0)
gyusuji = order_counts.get("牛すじ", 0)
mentai = order_counts.get("明太クリーミー", 0)
wafu = order_counts.get("和風だし", 0)
hitachi = order_counts.get("常総牛", 0)

# 4点が作れる時は3点を出さない
if beef >= 1 and menchi >= 1 and gyusuji >= 1 and mentai >= 1:
    suggestions.append("4点セットにできます")
elif beef >= 1 and menchi >= 1 and gyusuji >= 1:
    suggestions.append("3点セットにできます")

if beef >= 3 and menchi >= 2:
    suggestions.append("お得セットにできます（ビーフ3・メンチ2）")

if beef >= 1 and wafu >= 1 and hitachi >= 1:
    suggestions.append("お土産セットにできます")

if suggestions:
    for s in suggestions:
        st.info(s)
else:
    st.write("該当なし")

# -------------------------
# おすすめ構成（変換後）
# -------------------------
st.markdown("---")
st.subheader("おすすめ構成（変換後）")

remaining = order_counts.copy()
converted = []

# お得セットを最優先
count_otokuset = min(remaining.get("ビーフ", 0) // 3, remaining.get("メンチ", 0) // 2)
if count_otokuset > 0:
    converted.append(f"お得セット ×{count_otokuset}")
    remaining["ビーフ"] -= 3 * count_otokuset
    remaining["メンチ"] -= 2 * count_otokuset

# 4点セット
count_4 = min(
    remaining.get("ビーフ", 0),
    remaining.get("メンチ", 0),
    remaining.get("牛すじ", 0),
    remaining.get("明太クリーミー", 0),
)
if count_4 > 0:
    converted.append(f"4点セット ×{count_4}")
    remaining["ビーフ"] -= count_4
    remaining["メンチ"] -= count_4
    remaining["牛すじ"] -= count_4
    remaining["明太クリーミー"] -= count_4

# 3点セット
count_3 = min(
    remaining.get("ビーフ", 0),
    remaining.get("メンチ", 0),
    remaining.get("牛すじ", 0),
)
if count_3 > 0:
    converted.append(f"3点セット ×{count_3}")
    remaining["ビーフ"] -= count_3
    remaining["メンチ"] -= count_3
    remaining["牛すじ"] -= count_3

# お土産セット
count_omiyage = min(
    remaining.get("ビーフ", 0),
    remaining.get("和風だし", 0),
    remaining.get("常総牛", 0),
)
if count_omiyage > 0:
    converted.append(f"お土産セット ×{count_omiyage}")
    remaining["ビーフ"] -= count_omiyage
    remaining["和風だし"] -= count_omiyage
    remaining["常総牛"] -= count_omiyage

# 残り単品
for item, qty in remaining.items():
    if qty > 0:
        converted.append(f"{item} ×{qty}")

if converted:
    for c in converted:
        st.write(c)
else:
    st.write("なし")

# -------------------------
# 確定
# -------------------------
if st.button("この内容で確定", key="confirm_converted"):
    new_cart = {}

    for line in converted:
        name, qty_text = line.split(" ×")
        qty = int(qty_text)

        if name in set_items:
            # セットなら中身に分解して再格納
            for _ in range(qty):
                for item in set_items[name]:
                    new_cart[item] = new_cart.get(item, 0) + 1
        else:
            # 単品
            new_cart[name] = new_cart.get(name, 0) + qty

    st.session_state.cart = new_cart
    st.rerun()

# -------------------------
# おつり予測（2列×3件）
# -------------------------
st.markdown("---")
st.subheader("おつり予測一覧")

patterns = set()

# 客のクセ
for target in [50, 100, 500, 550]:
    pay = total + target
    if pay > total:
        patterns.add((pay, target))

# キリのいい支払い
p100 = ((total + 99) // 100) * 100
p1000 = ((total + 999) // 1000) * 1000

for pay in [p100, p1000]:
    if pay > total:
        patterns.add((pay, pay - total))

# ソート
patterns = sorted(patterns)

# 左右に分割
left = patterns[:3]
right = patterns[3:6]

col1, col2 = st.columns(2)

def format_line(pay, change):
    return f"{pay}円 → {change}円"

style = """
font-size:24px;
font-weight:600;
font-family:monospace;
margin-bottom:10px;
display:flex;
justify-content:flex-start;
"""

with col1:
    for pay, change in left:
        st.markdown(
            f"""
            <div style="{style}">
                <span style="width:120px; display:inline-block; text-align:right;">{pay}円</span>
                <span style="margin:0 10px;">→</span>
                <span style="width:80px; display:inline-block; text-align:right;">{change}円</span>
            </div>
            """,
            unsafe_allow_html=True
        )

with col2:
    for pay, change in right:
        st.markdown(
            f"""
            <div style="{style}">
                <span style="width:120px; display:inline-block; text-align:right;">{pay}円</span>
                <span style="margin:0 10px;">→</span>
                <span style="width:80px; display:inline-block; text-align:right;">{change}円</span>
            </div>
            """,
            unsafe_allow_html=True
        )
# -------------------------
# リセット
# -------------------------
st.markdown("---")
if st.button("リセット", key="reset_cart"):
    st.session_state.cart = {}
    st.rerun()
