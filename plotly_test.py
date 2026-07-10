import plotly.graph_objects as go
import pandas as pd
import os

# ========== 动态数据读取函数 ==========
def create_three_line_chart(csv_file="data_stream.csv", n_points=48):
    """
    从 CSV 读取最新数据，生成三线对比图
    
    参数:
        csv_file: CSV 文件路径
        n_points: 显示最近多少条数据
    """
    # 检查文件是否存在
    if not os.path.exists(csv_file):
        # 返回一个空图表，显示提示信息
        fig = go.Figure()
        fig.add_annotation(
            text="⏳ 等待数据...<br>请先启动模拟器: python simulator.py push",
            x=0.5, y=0.5,
            showarrow=False,
            font=dict(size=16)
        )
        fig.update_layout(
            height=500,
            template='plotly_white',
            title=dict(text='高炉风温 · 三线对比图（等待数据）', font=dict(size=18))
        )
        return fig

    # 读取 CSV 数据
    df = pd.read_csv(csv_file, encoding='utf-8-sig')
    
    if len(df) == 0:
        fig = go.Figure()
        fig.add_annotation(
            text="CSV 文件为空，请检查模拟器是否正常运行",
            x=0.5, y=0.5,
            showarrow=False,
            font=dict(size=16)
        )
        fig.update_layout(height=500, template='plotly_white')
        return fig

    # 取最近 n_points 条数据
    df_plot = df.tail(n_points).copy()

    # ========== 计算"三线"数据 ==========
    # 1. 实时曲线：直接用 CSV 里的风温
    real_time = df_plot['风温'].values

    # 2. 历史基准：用整个数据集的风温均值
    historical_mean = df['风温'].mean()

    # 3. 预测曲线：在实时数据基础上做简单偏移（模拟算法预测）
    #    这里用最近5条数据的趋势做外推，更真实
    if len(df_plot) >= 5:
        # 计算最近5条的变化趋势
        recent = df_plot['风温'].tail(5).values
        trend = (recent[-1] - recent[0]) / 4  # 每步的变化量
        
        # 预测值 = 最新值 + 趋势偏移（模拟未来3步）
        last_value = df_plot['风温'].iloc[-1]
        prediction = [last_value + trend * (i + 1) * 0.5 for i in range(len(df_plot))]
        df_plot['预测_风温'] = prediction
    else:
        # 数据不足时，用简单偏移
        import numpy as np
        np.random.seed(42)
        df_plot['预测_风温'] = df_plot['风温'] + np.random.normal(2, 3, len(df_plot))

    # ========== 创建三线对比图 ==========
    fig = go.Figure()

    # 历史基准线（绿色点线）
    fig.add_trace(go.Scatter(
        x=df_plot['timestamp'],
        y=[historical_mean] * len(df_plot),
        mode='lines',
        name=f'历史均值 ({historical_mean:.1f}°C)',
        line=dict(color='#4CAF50', width=2, dash='dot')
    ))

    # 实时曲线（蓝色实线）
    fig.add_trace(go.Scatter(
        x=df_plot['timestamp'],
        y=df_plot['风温'],
        mode='lines+markers',
        name='实时风温',
        line=dict(color='#2196F3', width=2.5),
        marker=dict(size=6)
    ))

    # 预测曲线（红色虚线）
    fig.add_trace(go.Scatter(
        x=df_plot['timestamp'],
        y=df_plot['预测_风温'],
        mode='lines+markers',
        name='算法预测',
        line=dict(color='#FF5722', width=2.5, dash='dash'),
        marker=dict(size=6, symbol='diamond')
    ))

    # ========== 预警标注 ==========
    # 如果有 instruction 列，根据指令添加预警标注
    if 'instruction' in df_plot.columns:
        alert_points = df_plot[df_plot['instruction'].notna() & (df_plot['instruction'] != '')]
        if not alert_points.empty:
            fig.add_trace(go.Scatter(
                x=alert_points['timestamp'],
                y=alert_points['风温'],
                mode='markers',
                name='⚠️ 预警点',
                marker=dict(color='red', size=14, symbol='x')
            ))

    # ========== 图表布局 ==========
    fig.update_layout(
        title=dict(
            text=f'高炉风温 · 三线对比图（实时/预测/历史）',
            font=dict(size=18, color='#1a1a2e')
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

    return fig


# ========== 独立运行测试 ==========
if __name__ == "__main__":
    fig = create_three_line_chart("data_stream.csv")
    fig.show()
    
    # 保存为 HTML（可选）
    fig.write_html('三线对比图.html')
    print("✅ 三线对比图已生成")