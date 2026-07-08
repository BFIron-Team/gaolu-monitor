import streamlit as st

# ========== 页面配置 ==========
st.set_page_config(
    page_title="炼铁工艺仪表盘",
    page_icon="🏭",
    layout="wide"
)

# ========== 页面标题 ==========
st.title("🏭 炼铁工艺关键控制指标")
st.markdown("---")  # 分割线

# ========== 三列布局显示核心指标 ==========
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("🔥 风温", "1180 °C", "▲ +15 °C")

with col2:
    st.metric("📊 炉压", "0.32 MPa", "▼ -0.02 MPa")

with col3:
    st.metric("💨 透气性指数", "82.6%", "▲ +2.1%")


# ========== 第二行：状态卡片 ==========
st.markdown("---")
st.subheader("📋 当前运行状态")

col4, col5 = st.columns(2)

with col4:
    st.info(
        "✅ 高炉运行平稳\n\n"
        "· 风温处于合理区间\n"
        "· 炉压波动正常"
    )

with col5:
    st.warning(
        "⚠️ 操作建议\n\n"
        "· 风温可适当上调 5~10°C\n"
        "· 注意观察透气性变化趋势"
    )

# ========== 页脚 ==========
st.markdown("---")
st.caption("北京交通大学 · 数统学院 · 炼铁工艺大创项目")