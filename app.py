import streamlit as st
from core.calculator import calculate_billet_costs
import json

st.title("FusionQuote: Billet Optimizer")
st.markdown("### 長山工業：米国向け超速見積エンジン")

# サイドバー：基本設定
with st.sidebar:
    st.header("Global Settings")
    rate = st.number_input("Hourly Rate (JPY)", value=8000) # 日本拠点想定
    mat_price = st.number_input("Material Price (JPY/kg)", value=1200)

# メインパネル：データ入力
col1, col2 = st.columns(2)
with col1:
    st.subheader("1. Billet Dimensions")
    dia = st.number_input("Diameter (mm)", value=320) # フロントナックル素材 
    length = st.number_input("Length (mm)", value=640)

with col2:
    st.subheader("2. AI Analysis Data")
    # Web版LLMで解析したJSONをここに貼り付ける
    json_input = st.text_area("Paste JSON from Web LLM (GPTs/Gemini)", height=150)

if st.button("Generate Quote"):
    # ダミー値またはJSON解析値を使用
    res = calculate_billet_costs(dia, length, 10.0, mat_price, rate, 15.0)
    
    # 現場への「警告」と「納得」の表示
    st.error(f"⚠️ 素材重量: {res['raw_weight']} kg / 除去率: {res['removal_rate']}%")
    st.metric("Total Material Cost", f"¥{res['material_cost']:,.0f}")
    
    st.success("Billet Advantage: No Tooling Cost / 2-Week Lead Time")
