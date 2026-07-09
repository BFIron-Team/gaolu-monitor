import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_blast_furnace_data(days=7, freq='1h'):
    """
    生成高炉运行模拟数据
    
    参数:
        days: 模拟天数，默认7天
        freq: 采样频率，默认1小时
    
    返回:
        pandas.DataFrame: 包含高炉工艺参数的数据框
    """
    # 生成时间序列
    start_time = datetime.now() - timedelta(days=days)
    timestamps = pd.date_range(start=start_time, periods=days*24, freq=freq)
    
    np.random.seed(42)  # 固定随机种子，确保结果可复现
    
    # 1. 风温：围绕1180°C波动，存在日周期变化
    base_temp = 1180
    daily_cycle = 20 * np.sin(np.linspace(0, 2*np.pi*days, len(timestamps)))
    noise = np.random.normal(0, 8, len(timestamps))
    wind_temp = base_temp + daily_cycle + noise
    
    # 2. 炉压：围绕0.32MPa波动，与风温反向相关
    base_pressure = 0.32
    pressure_noise = np.random.normal(0, 0.015, len(timestamps))
    pressure = base_pressure - 0.00015 * (wind_temp - base_temp) + pressure_noise
    pressure = np.clip(pressure, 0.25, 0.40)  # 约束在合理范围
    
    # 3. 透气性指数：28-35之间波动，与炉压负相关
    base_permeability = 30
    perm_noise = np.random.normal(0, 1.5, len(timestamps))
    permeability = base_permeability - 3 * (pressure - base_pressure) + perm_noise
    permeability = np.clip(permeability, 24, 36)
    
    # 4. 富氧率：2-6%之间
    oxygen_rate = 4 + 1.5 * np.sin(np.linspace(0, np.pi, len(timestamps))) + np.random.normal(0, 0.3, len(timestamps))
    oxygen_rate = np.clip(oxygen_rate, 2, 6)
    
    # 5. 炉顶温度：80-120°C之间
    top_temp = 100 + 15 * np.sin(np.linspace(0, 2*np.pi*days, len(timestamps)) + 0.5) + np.random.normal(0, 5, len(timestamps))
    
    # 6. 生成操作建议（模拟后台算法输出）
    suggestions = []
    for i in range(len(timestamps)):
        # 当风温超过1195°C时建议下调
        if wind_temp[i] > 1195:
            suggestions.append(f"建议下调风温{int(wind_temp[i] - 1180)}°C")
        elif wind_temp[i] < 1165:
            suggestions.append(f"建议上调风温{int(1180 - wind_temp[i])}°C")
        # 当炉压超过0.37MPa时预警
        elif pressure[i] > 0.37:
            suggestions.append("⚠️ 炉压偏高，建议检查料柱透气性")
        else:
            suggestions.append("操作正常，保持当前参数")
    
    # 组装DataFrame
    df = pd.DataFrame({
        'timestamp': timestamps,
        '风温_℃': np.round(wind_temp, 1),
        '炉压_MPa': np.round(pressure, 3),
        '透气性指数': np.round(permeability, 1),
        '富氧率_%': np.round(oxygen_rate, 1),
        '炉顶温度_℃': np.round(top_temp, 1),
        '操作建议': suggestions
    })
    
    return df

# 生成7天数据（每小时一条）
if __name__ == "__main__":
    df = generate_blast_furnace_data(days=7, freq='1h')
    
    # 保存为CSV文件
    df.to_csv('blast_furnace_data.csv', index=False, encoding='utf-8-sig')
    
    # 打印前5行预览
    print("📊 高炉数据模拟器运行成功！")
    print(f"共生成 {len(df)} 条记录")
    print("\n数据预览（前5行）：")
    print(df.head())
    
    # 打印统计信息
    print("\n📈 关键指标统计：")
    print(f"风温范围: {df['风温_℃'].min()} ~ {df['风温_℃'].max()} °C")
    print(f"炉压范围: {df['炉压_MPa'].min()} ~ {df['炉压_MPa'].max()} MPa")
    print(f"透气性范围: {df['透气性指数'].min()} ~ {df['透气性指数'].max()}")