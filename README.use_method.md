#启动模拟器
#cd D:\gaolu-monitor
python simulator.py                → 普通测试模式（normal）
python simulator.py normal         → 普通测试模式（平稳）
python simulator.py extreme        → 普通测试模式（剧烈波动）
python simulator.py push           → 持续推送模式（平稳，写入CSV）
python simulator.py push extreme   → 持续推送模式（剧烈波动，写入CSV）
运行前端
cd D:\gaolu-monitor
python -m streamlit run app.py
