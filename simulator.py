import math
import random
import time
import sys          # 新增这一行
from datetime import datetime

# ============================================================
# 模式选择（命令行参数方式）
# 用法：
#   python simulator.py          → 默认 normal（平稳）
#   python simulator.py normal   → 正常平稳模式
#   python simulator.py extreme  → 剧烈波动模式（测试预警）
# ============================================================
if len(sys.argv) > 1 and sys.argv[1].lower() == "extreme":
    RUN_MODE = "extreme"
else:
    RUN_MODE = "normal"  # 默认平稳模式

# 打印当前模式，方便确认
print(f"当前模拟模式: {RUN_MODE}")
# ========== 基值设定 ==========
BASE_TEMP = 1050.0          # 风温基值 (℃)
BASE_PRESSURE = 300.0       # 炉压基值 (kPa)
BASE_PERMEABILITY = 1.0     # 透气性基值 (无量纲)

# ========== 正弦趋势参数（根据模式自动选择） ==========
if RUN_MODE == "extreme":
    TEMP_AMPLITUDE = 80.0       # 风温振幅 (℃)  — 剧烈波动
    PRESSURE_AMPLITUDE = 60.0   # 炉压振幅 (kPa) — 剧烈波动
    PERM_AMPLITUDE = 0.30       # 透气性振幅     — 剧烈波动
    TREND_PERIOD = 20.0         # 周期缩短，波动更快
else:
    TEMP_AMPLITUDE = 30.0       # 风温振幅 (℃)  — 平稳
    PRESSURE_AMPLITUDE = 20.0   # 炉压振幅 (kPa) — 平稳
    PERM_AMPLITUDE = 0.15       # 透气性振幅     — 平稳
    TREND_PERIOD = 30.0         # 周期较长

# ========== 噪声参数 ==========
TEMP_NOISE_STD = 5.0        # 风温噪声标准差 (℃)
PRESSURE_NOISE_STD = 3.0    # 炉压噪声标准差 (kPa)
PERM_NOISE_STD = 0.03       # 透气性噪声标准差

# ========== 预警阈值 ==========
PRESSURE_HIGH_THRESHOLD = 350.0       # 炉压过高阈值 (kPa)
PRESSURE_HIGH_CONSECUTIVE = 3         # 连续触发次数
TEMP_LOW_THRESHOLD = 980.0            # 风温过低阈值 (℃)

# ========== 预警指令文本 ==========
INSTR_PRESSURE_HIGH = "炉压持续偏高，建议适当下调风压操作"
INSTR_TEMP_LOW = "风温偏低，建议检查热风炉并提高燃烧强度"


class BlastFurnaceSimulator:
    """高炉数据模拟器"""

    def __init__(self):
        self.start_time = time.time()
        self.pressure_high_count = 0          # 炉压过高的连续计数
        self.current_instruction = ""

    def _generate_metrics(self, current_time: float) -> dict:
        """生成一帧工艺指标数据（内部方法）"""
        phase = 2 * math.pi * current_time / TREND_PERIOD

        # 趋势项
        temp_trend = TEMP_AMPLITUDE * math.sin(phase)
        pressure_trend = PRESSURE_AMPLITUDE * math.sin(phase)
        perm_trend = PERM_AMPLITUDE * math.sin(phase)

        # 噪声项
        temp_noise = random.gauss(0, TEMP_NOISE_STD)
        pressure_noise = random.gauss(0, PRESSURE_NOISE_STD)
        perm_noise = random.gauss(0, PERM_NOISE_STD)

        # 最终值 = 基值 + 趋势项 + 噪声项
        wind_temp = BASE_TEMP + temp_trend + temp_noise
        furnace_pressure = BASE_PRESSURE + pressure_trend + pressure_noise
        permeability = BASE_PERMEABILITY + perm_trend + perm_noise

        return {
            "风温": round(wind_temp, 2),
            "炉压": round(furnace_pressure, 2),
            "透气性": round(permeability, 3)
        }

    def _evaluate_warnings(self, metrics: dict) -> str:
        """评估预警规则，返回当前指令"""
        pressure = metrics["炉压"]
        temp = metrics["风温"]

        # ===== 规则A：炉压过高（连续3次） =====
        if pressure > PRESSURE_HIGH_THRESHOLD:
            self.pressure_high_count += 1
        else:
            self.pressure_high_count = 0

        # ===== 规则B：风温过低（单次触发） =====
        temp_low_triggered = (temp < TEMP_LOW_THRESHOLD)

        # ===== 指令更新逻辑 =====
        instruction = ""
        if self.pressure_high_count >= PRESSURE_HIGH_CONSECUTIVE:
            instruction = INSTR_PRESSURE_HIGH
        if temp_low_triggered:
            instruction = INSTR_TEMP_LOW

        return instruction

    def next_frame(self, data_type: str = "realtime") -> dict:
        """生成下一帧完整数据（含时间戳、指标、数据类型、指令）"""
        current_time = time.time() - self.start_time

        # 1. 生成工艺指标
        metrics = self._generate_metrics(current_time)

        # 2. 评估预警规则
        instruction = self._evaluate_warnings(metrics)

        # 3. 生成时间戳
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 4. 组装完整数据帧
        frame = {
            "timestamp": timestamp,
            "metrics": metrics,
            "data_type": data_type,
            "instruction": instruction
        }
        return frame


# ========== 测试代码（运行后自动执行） ==========
if __name__ == "__main__":
    simulator = BlastFurnaceSimulator()
    print(f"=== 高炉数据模拟器运行测试（模式: {RUN_MODE}）===")
    print("运行 20 秒，观察数据波动和指令触发情况...")
    print("-" * 50)
    
    for i in range(20):
        frame = simulator.next_frame(data_type="realtime")
        instr_display = frame["instruction"] if frame["instruction"] else "(无指令)"
        print(f"帧{i+1:2d}: 炉压={frame['metrics']['炉压']:6.2f}kPa, 风温={frame['metrics']['风温']:6.2f}℃, 指令={instr_display}")
        time.sleep(1)
    
    print("-" * 50)
    print("测试完成！")