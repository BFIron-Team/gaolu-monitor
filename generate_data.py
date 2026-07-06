import pandas as pd
import numpy as np

# 1. 生成时间序列
time_index = pd.date_range(start='2026-07-06 08:00:00', periods=100, freq='1s')

# 2. 生成模拟数据
t = np.arange(100)
风温 = 1050 + 10 * np.sin(2 * np.pi * t / 30) + np.random.normal(0, 3, 100)
炉压 = 300 + 5 * np.sin(2 * np.pi * t / 45) + np.random.normal(0, 2, 100)

# 3. 组装DataFrame表格
df = pd.DataFrame({
    '时间': time_index,
    '风温': np.round(风温, 2),
    '炉压': np.round(炉压, 2)
})

# 4. 打印前5行
print(df.head())

# 5. 保存成CSV文件
df.to_csv('模拟数据_风温炉压.csv', index=False, encoding='utf-8-sig')
print("数据已保存到 模拟数据_风温炉压.csv")