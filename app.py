import streamlit as st
import pandas as pd
import os
from streamlit_autorefresh import st_autorefresh
from plotly_test import create_three_line_chart

st.set_page_config(page_title="炼铁工艺仪表盘", page_icon="🏭", layout="wide")

DATA_FILE = "data_stream.csv"

def get_latest_data():
    if not os.path.exists(DATA_FILE):
        return None
    df = pd.read_csv(DATA_FILE, encoding='utf-8-sig')
    if len(df) == 0:
        return None
    latest = df.iloc[-1]
    instr = latest["instruction"]
    if pd.isna(instr) or str(instr).strip() == "" or str(instr).lower() == "nan":
        instr = ""
    return {
        "timestamp": latest["timestamp"],
        "风温": latest["风温"],
        "炉压": latest["炉压"],
        "透气性": latest["透气性"],
        "instruction": instr
    }

def get_history(n=20):
    if not os.path.exists(DATA_FILE):
        return pd.DataFrame()
    df = pd.read_csv(DATA_FILE, encoding='utf-8-sig')
    return df.tail(n) if len(df) > 0 else pd.DataFrame()

st.title("🏭 炼铁工艺关键控制指标")
st.markdown("---")

# ===== 侧边栏 =====
with st.sidebar:
    st.header("🎛️ 控制面板")
    interval = st.slider("刷新间隔（秒）", min_value=1, max_value=10, value=3)
    st.caption(f"当前间隔: {interval} 秒")
    st.divider()
    st.caption("模拟器: `python simulator.py push extreme`")

# ===== 自动刷新（不阻塞交互） =====
st_autorefresh(interval=interval * 1000, key="auto_refresh")

# ===== 主内容 =====
latest = get_latest_data()

if latest is not None:
    col1, col2, col3 = st.columns(3)
    col1.metric("🔥 风温", f"{latest['风温']} °C")
    col2.metric("📊 炉压", f"{latest['炉压']} kPa")
    col3.metric("💨 透气性", f"{latest['透气性']}")
    
    instr = latest.get("instruction", "")
    if instr and str(instr).strip():
        st.error(f"⚠️ {instr}")
    else:
        st.success("✅ 系统运行正常，无操作指令")
    
    st.caption(f"📅 更新时间: {latest['timestamp']} | 刷新间隔: {interval}s")
    
    # ===== 三线图 =====
    st.markdown("---")
    st.subheader("📈 三线对比图（实时/预测/历史）")
    fig = create_three_line_chart(DATA_FILE)
    st.plotly_chart(fig, use_container_width=True)
    
    # ===== 历史表格 =====
    history_df = get_history(20)
    if not history_df.empty:
        st.subheader("📋 最近数据记录")
        history_df_display = history_df.copy()
        if "instruction" in history_df_display.columns:
            history_df_display["instruction"] = history_df_display["instruction"].fillna("").replace("nan", "")
        st.dataframe(
            history_df_display[["timestamp", "风温", "炉压", "透气性", "instruction"]],
            use_container_width=True
        )
else:
    st.warning("⏳ 等待数据... 请确保模拟器正在运行")
    st.info("启动: `python simulator.py push extreme`")

st.markdown("---")
st.caption("北京交通大学 · 数统学院 · 炼铁工艺大创项目 | 自动刷新模式 (无阻塞)")