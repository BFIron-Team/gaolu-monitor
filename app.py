import streamlit as st
import plotly.express as px
import pandas as pd

# 页面配置
st.set_page_config(page_title="炼铁工艺仪表盘", layout="wide")

st.title("🔥 炼铁工艺关键控制指标")
st.markdown("---")

# 三列指标卡
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("风温", "1180 °C", "+15 °C")
with col2:
    st.metric("炉压", "0.32 MPa", "-0.02 MPa")
with col3:
    st.metric("透气性", "28.5", "+2.1")

st.markdown("---")

# 生成模拟数据
data = {
    '日期': ['第1天', '第2天', '第3天', '第4天', '第5天', '第6天', '第7天'],
    '风温 (℃)': [1050, 1060, 1045, 1070, 1080, 1090, 1085]
}
df = pd.DataFrame(data)

# 绘制折线图
fig = px.line(df, x='日期', y='风温 (℃)', title='高炉风温一周变化趋势')
st.plotly_chart(fig, use_container_width=True)