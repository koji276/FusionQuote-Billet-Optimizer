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
    
    # --- 新機能：プロンプト自動生成機能 ---
    with st.expander("💡 Web版LLM(GPTs/Gemini)用の解析プロンプトを作成", expanded=True):
        st.write("以下のテキストをコピーし、図面(PDF)と一緒にLLMへ送信してください。")
        
        # 入力された寸法(dia, length)を自動で組み込むプロンプト
        prompt_text = f"""あなたは長山工業の熟練見積士であり、5軸切削加工のエキスパートです。
添付の図面（および写真）を解析し、以下の構造化データ(JSON)のみを出力してください。

【前提条件】
- 素材サイズ: アルミ丸棒 直径 {dia} mm x 長さ {length} mm
- 加工機: 5軸横形マシニングセンタ

【推測タスク】
1. 図面に記載されている使用工具(CUT番号など)の総数をカウントしてください。
2. 素材の体積と一般的なナックルの形状から、完成重量(kg)を推測してください。
3. 荒加工での大量の切削（ビレット加工）と、ボーリング等の仕上げ精度を考慮し、想定される総加工時間(時間)を推測してください。

【出力フォーマット（厳密に以下のJSONのみを出力）】
{{
  "total_tools": 16,
  "hours": 15.0,
  "finish_weight": 8.5
}}"""
        st.code(prompt_text, language="markdown")
    
    # 既存のJSON入力欄
    json_str = st.text_area("Web版LLMから出力されたJSONを貼り付けてください", 
                          placeholder='{"total_tools": 16, "hours": 15.0, "finish_weight": 8.5}',
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
