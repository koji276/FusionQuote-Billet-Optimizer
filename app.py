import streamlit as st
import json
from logic import calculate_billet_costs

st.set_page_config(page_title="FusionQuote MVP", layout="wide")

st.title("🚀 FusionQuote: Billet Machining Optimizer")
st.caption("長山工業：米国市場向け超速見積エンジン（試作・ビレット特化型）")

# --- サイドバー：基本設定 ---
with st.sidebar:
    st.header("⚙️ Global Settings")
    hourly_rate = st.number_input("Hourly Rate (JPY/h)", value=8000, help="日本拠点の標準賃率") #
    mat_unit_price = st.number_input("Material Price (JPY/kg)", value=1200, help="アルミ6061-T6相場")
    margin_rate = st.slider("Target Margin (%)", 10, 50, 25)

# --- メイン：データ入力 ---
col_in1, col_in2 = st.columns(2)

with col_in1:
    st.subheader("1. Billet Dimensions")
    dia = st.number_input("Diameter (mm)", value=320) # 
    length = st.number_input("Length (mm)", value=640) # 
    st.info(f"素材サイズ: φ{dia} x {length}")

with col_in2:
    st.subheader("2. AI Analysis (Paste JSON)")
    # Web版LLM（MyGPTs等）で図面を解析させた結果をここに貼る
    json_str = st.text_area("Web版LLMからコピーしたJSONを貼り付けてください", 
                          placeholder='{"total_tools": 16, "hours": 15, "finish_weight": 8.5}',
                          height=150)

# --- 実行ボタン ---
if st.button("Generate Strategic Quote"):
    if json_str:
        try:
            data = json.loads(json_str)
            # 計算実行
            res = calculate_billet_costs(
                dia, length, data.get("finish_weight", 10.0), 
                mat_unit_price, hourly_rate, data.get("hours", 10.0)
            )
            
            # --- 結果表示 ---
            st.divider()
            
            # A. 現場の衝撃（英一郎インパクト）
            col_res1, col_res2, col_res3 = st.columns(3)
            with col_res1:
                st.metric("Raw Material Weight", f"{res['raw_weight']} kg")
            with col_res2:
                st.error(f"Chip Waste: {res['chip_weight']} kg")
            with col_res3:
                st.warning(f"Removal Rate: {res['removal_rate']}%")
            
            # B. コスト内訳
            total_cost = (res['material_cost'] + res['processing_cost']) * (1 + margin_rate/100)
            
            col_cost1, col_cost2 = st.columns(2)
            with col_cost1:
                st.subheader("Cost Breakdown")
                st.write(f"Net Material Cost: ¥{res['material_cost']:,.0f}")
                st.write(f"Machining Cost: ¥{res['processing_cost']:,.0f}")
                st.header(f"Total Quote: ¥{total_cost:,.0f}")
                st.caption(f"Approx: ${total_cost/150:,.0f} (at 150 JPY/USD)") #
                
            with col_cost2:
                st.subheader("Strategic Advantage (for US Client)")
                st.success("✅ NO TOOLING COST (Saved ~$50,000)") #
                st.success("✅ 2-WEEK LEAD TIME (Saved ~3 Months)") #
                st.write("この見積もりは「金型製作」を介さない「ビレット削り出し」の即応価値を反映しています。")
                
        except Exception as e:
            st.error(f"JSON解析エラー: {e}")
    else:
        st.warning("JSONデータを入力してください。")
