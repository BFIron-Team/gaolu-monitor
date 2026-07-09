import math
import random
import time
import sys
from datetime import datetime
import csv
import os

# ============================================================
# 模式选择（命令行参数方式）
# 用法：
#   python simulator.py                → 普通测试模式（normal）
#   python simulator.py normal         → 普通测试模式（平稳）
#   python simulator.py extreme        → 普通测试模式（剧烈波动）
#   python simulator.py push           → 持续推送模式（平稳，写入CSV）
#   python simulator.py push extreme   → 持续推送模式（剧烈波动，写入CSV）
# ============================================================

# 解析命令行参数
args = sys.argv[1:]
is_push_mode = "push" in args
is_extreme = "extreme" in args

if is_extreme:
    RUN_MODE = "extreme"
else:
    RUN_MODE = "normal"

print(f"当前模式: {'推送' if is_push_mode else '测试'}模式 | 波动: {RUN_MODE}")

# ========== 基值设定 ==========
BASE_TEMP = 1050.0
BASE_PRESSURE = 300.0
BASE_PERMEABILITY = 1.0

# ========== 正弦趋势参数（根据模式自动选择） ==========
if RUN_MODE == "extreme":
    TEMP_AMPLITUDE = 80.0
    PRESSURE_AMPLITUDE = 60.0
    PERM_AMPLITUDE = 0.30
    TREND_PERIOD = 20.0
else:
    TEMP_AMPLITUDE = 30.0
    PRESSURE_AMPLITUDE = 20.0
    PERM_AMPLITUDE = 0.15
    TREND_PERIOD = 30.0

# ========== 噪声参数 ==========
TEMP_NOISE_STD = 5.0
PRESSURE_NOISE_STD = 3.0
PERM_NOISE_STD = 0.03

# ========== 预警阈值 ==========
PRESSURE_HIGH_THRESHOLD = 350.0
PRESSURE_HIGH_CONSECUTIVE = 3
TEMP_LOW_THRESHOLD = 980.0

# ========== 预警指令文本 ==========
INSTR_PRESSURE_HIGH = "炉压持续偏高，建议适当下调风压操作"
INSTR_TEMP_LOW = "风温偏低，建议检查热风炉并提高燃烧强度"

# ========== 数据文件路径 ==========
DATA_FILE = "data_stream.csv"


class BlastFurnaceSimulator:
    """高炉数据模拟器"""

    def __init__(self):
        self.start_time = time.time()
        self.pressure_high_count = 0

    def _generate_metrics(self, current_time: float) -> dict:
        phase = 2 * math.pi * current_time / TREND_PERIOD

        temp_trend = TEMP_AMPLITUDE * math.sin(phase)
        pressure_trend = PRESSURE_AMPLITUDE * math.sin(phase)
        perm_trend = PERM_AMPLITUDE * math.sin(phase)

        temp_noise = random.gauss(0, TEMP_NOISE_STD)
        pressure_noise = random.gauss(0, PRESSURE_NOISE_STD)
        perm_noise = random.gauss(0, PERM_NOISE_STD)

        wind_temp = BASE_TEMP + temp_trend + temp_noise
        furnace_pressure = BASE_PRESSURE + pressure_trend + pressure_noise
        permeability = BASE_PERMEABILITY + perm_trend + perm_noise

        return {
            "风温": round(wind_temp, 2),
            "炉压": round(furnace_pressure, 2),
            "透气性": round(permeability, 3)
        }

    def _evaluate_warnings(self, metrics: dict) -> str:
        pressure = metrics["炉压"]
        temp = metrics["风温"]

        if pressure > PRESSURE_HIGH_THRESHOLD:
            self.pressure_high_count += 1
        else:
            self.pressure_high_count = 0

        temp_low_triggered = (temp < TEMP_LOW_THRESHOLD)

        instruction = ""
        if self.pressure_high_count >= PRESSURE_HIGH_CONSECUTIVE:
            instruction = INSTR_PRESSURE_HIGH
        if temp_low_triggered:
            instruction = INSTR_TEMP_LOW

        return instruction

    def next_frame(self, data_type: str = "realtime") -> dict:
        current_time = time.time() - self.start_time

        metrics = self._generate_metrics(current_time)
        instruction = self._evaluate_warnings(metrics)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        frame = {
            "timestamp": timestamp,
            "metrics": metrics,
            "data_type": data_type,
            "instruction": instruction
        }
        return frame


def push_to_file(simulator: BlastFurnaceSimulator, filename: str = DATA_FILE, interval: float = 1.0):
    """持续运行模拟器，将数据写入CSV文件"""
    if not os.path.exists(filename):
        with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            writer.writerow(["timestamp", "风温", "炉压", "透气性", "data_type", "instruction"])

    print(f"开始持续推送数据到文件: {filename}")
    print(f"当前波动模式: {RUN_MODE} (normal=平稳, extreme=剧烈)")
    print("按 Ctrl+C 停止")
    print("-" * 50)

    try:
        while True:
            frame = simulator.next_frame(data_type="realtime")
            metrics = frame["metrics"]

            with open(filename, 'a', newline='', encoding='utf-8-sig') as f:
                writer = csv.writer(f)
                writer.writerow([
                    frame["timestamp"],
                    metrics["风温"],
                    metrics["炉压"],
                    metrics["透气性"],
                    frame["data_type"],
                    frame["instruction"]
                ])

            instr = frame["instruction"] if frame["instruction"] else "无"
            print(f"[{frame['timestamp']}] 风温={metrics['风温']}℃ 炉压={metrics['炉压']}kPa 指令={instr}")

            time.sleep(interval)

    except KeyboardInterrupt:
        print("\n已停止数据推送")


# ========== 主入口 ==========
if __name__ == "__main__":
    simulator = BlastFurnaceSimulator()

    if is_push_mode:
        # 推送模式
        push_to_file(simulator)
    else:
        # 普通测试模式：运行20帧
        print(f"=== 高炉数据模拟器运行测试（模式: {RUN_MODE}）===")
        print("-" * 50)

        for i in range(20):
            frame = simulator.next_frame(data_type="realtime")
            instr_display = frame["instruction"] if frame["instruction"] else "(无指令)"
            print(f"帧{i+1:2d}: 炉压={frame['metrics']['炉压']:6.2f}kPa, 风温={frame['metrics']['风温']:6.2f}℃, 指令={instr_display}")
            time.sleep(1)

        print("-" * 50)
        print("测试完成！")