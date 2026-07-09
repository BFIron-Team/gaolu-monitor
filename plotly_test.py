import plotly.graph_objects as go
import pandas as pd
import numpy as np

# 1. 加载模拟数据
df = pd.read_csv('blast_furnace_data.csv', encoding='utf-8-sig')
print(f"✅ 加载数据成功，共 {len(df)} 条记录")

# 取最近48个数据点（便于显示）
df_plot = df.tail(48).copy()

# 2. 计算"三线"数据
# 实时曲线：直接使用实际数据
real_time = df_plot['风温_℃'].values

# 历史基准：整体均值（模拟"历史同期"）
historical_mean = df['风温_℃'].mean()

# 预测曲线：在实时数据基础上偏移（模拟算法预测）
np.random.seed(42)
df_plot['预测_风温_℃'] = df_plot['风温_℃'] + np.random.normal(3, 4, len(df_plot))

# 3. 创建"三线对比图"
fig = go.Figure()

# 实时曲线（蓝色实线）
fig.add_trace(go.Scatter(
    x=df_plot['timestamp'],
    y=df_plot['风温_℃'],
    mode='lines+markers',
    name='实时风温',
    line=dict(color='#2196F3', width=2.5),
    marker=dict(size=6)
))

# 预测曲线（红色虚线）
fig.add_trace(go.Scatter(
    x=df_plot['timestamp'],
    y=df_plot['预测_风温_℃'],
    mode='lines+markers',
    name='算法预测',
    line=dict(color='#FF5722', width=2.5, dash='dash'),
    marker=dict(size=6, symbol='diamond')
))

# 历史基准线（绿色点线）
fig.add_trace(go.Scatter(
    x=df_plot['timestamp'],
    y=[historical_mean] * len(df_plot),
    mode='lines',
    name=f'历史均值 ({historical_mean:.1f}°C)',
    line=dict(color='#4CAF50', width=2, dash='dot')
))

# 4. 添加预警标注（风温 > 1195°C）
alert_points = df_plot[df_plot['风温_℃'] > 1195]
if not alert_points.empty:
    fig.add_trace(go.Scatter(
        x=alert_points['timestamp'],
        y=alert_points['风温_℃'],
        mode='markers',
        name='⚠️ 预警点',
        marker=dict(color='red', size=14, symbol='x')
    ))

# 5. 图表布局
fig.update_layout(
    title=dict(
        text='高炉风温 · 三线对比图（实时/预测/历史）',
        font=dict(size=20, color='#1a1a2e')
    ),
    xaxis_title='时间',
    yaxis_title='风温 (°C)',
    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=1.02,
        xanchor='right',
        x=1
    ),
    hovermode='x unified',
    template='plotly_white',
    height=500,
    margin=dict(l=50, r=50, t=80, b=50)
)

# 显示图表
fig.show()

# 6. 保存为HTML文件（方便分享）
fig.write_html('三线对比图.html')
print("✅ 三线对比图已生成，并保存为 三线对比图.html")