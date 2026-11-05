"""
AeroGuardAI - Stage 1: MALE UAV Aero Piston Engine Telemetry Simulator
Uses only Python standard libraries, NumPy, and Pandas.
"""

import numpy as np
import pandas as pd


def generate_engine_telemetry(
    duration_seconds: int = 300,
    sampling_rate_hz: int = 1,
    scenario: str = "normal",
    random_seed: int = 42
) -> pd.DataFrame:
    """
    Simulates real-time telemetry for a turbocharged 4-stroke aero piston engine
    (similar to Rotax 914 used in MALE UAVs such as MQ-1 Predator / Heron).

    Flight profile:
      0 - 40s   : Takeoff & Initial Climb (Full throttle 100%, high MAP, high RPM)
      40 - 100s : Continuous Climb (85% throttle)
      100 - 240s: High-altitude Cruise / Loiter (70% throttle)
      240 - 300s: Descent & Return to Base (45% throttle)

    Scenarios:
      - 'normal': Healthy engine within safe operating envelope
      - 'turbo_failure': Wastegate/Turbo leak at t > 120s (Drop in MAP, loss of power)
      - 'oil_leak': Loss of lubrication pressure at t > 130s (Rapid oil pressure drop, oil temp rise)
      - 'cht_overheat': Coolant/baffle failure at t > 110s (CHT exceeds redline limit)
      - 'fuel_clog': Injector/line clog at t > 140s (EGT anomaly, RPM fluctuation)
    """
    np.random.seed(random_seed)
    time_steps = np.arange(0, duration_seconds, 1 / sampling_rate_hz)
    n = len(time_steps)

    # 1. Mission Flight Dynamics Profile
    throttle = np.zeros(n)
    altitude = np.zeros(n)

    for i, t in enumerate(time_steps):
        if t < 40:
            # Takeoff
            throttle[i] = 100.0
            altitude[i] = 100 + (t / 40.0) * 1500
        elif t < 100:
            # Climb
            throttle[i] = 85.0
            altitude[i] = 1600 + ((t - 40) / 60.0) * 8400
        elif t < 240:
            # Cruise / Loiter at 10,000 - 12,000 ft
            throttle[i] = 70.0
            altitude[i] = 10000 + 200 * np.sin(t / 20.0)
        else:
            # Descent
            throttle[i] = 45.0
            altitude[i] = max(1000, 10000 - ((t - 240) / 60.0) * 8000)

    # 2. Physics Baseline Generation (Nominal Engine Performance)
    # RPM: Idle ~2200, Cruise ~4800, Max Takeoff ~5800
    rpm_base = 2200 + (throttle / 100.0) * 3600
    rpm = rpm_base + np.random.normal(0, 15, n)

    # Manifold Absolute Pressure (MAP) in inHg: Atmospheric at sea level is ~29.92
    # Turbo boost reaches up to 39.5 inHg at full throttle
    map_base = 26.0 + (throttle / 100.0) * 13.5 - (altitude / 20000.0) * 1.5
    manifold_pressure = map_base + np.random.normal(0, 0.15, n)

    # Cylinder Head Temperature (CHT in °C): Normal range 90°C - 130°C. Redline ~135°C
    cht_base = 80.0 + (throttle / 100.0) * 38.0 + (rpm / 5800.0) * 12.0
    cht = cht_base + np.random.normal(0, 0.8, n)

    # Exhaust Gas Temperature (EGT in °C): Normal range 750°C - 880°C. Redline ~900°C
    egt_base = 730.0 + (throttle / 100.0) * 130.0
    egt = egt_base + np.random.normal(0, 2.5, n)

    # Oil Pressure (bar): Normal range 2.0 - 5.0 bar. Redline < 1.5 bar
    oil_press_base = 2.5 + (rpm / 5800.0) * 2.2
    oil_pressure = oil_press_base + np.random.normal(0, 0.04, n)

    # Oil Temperature (°C): Normal range 70°C - 110°C. Redline > 130°C
    oil_temp_base = 75.0 + (rpm / 5800.0) * 28.0
    oil_temp = oil_temp_base + np.random.normal(0, 0.5, n)

    # Vibration (g RMS): Normal < 1.2 g. Anomaly > 2.0 g
    vibration_base = 0.4 + (rpm / 5800.0) * 0.6
    vibration = vibration_base + np.random.normal(0, 0.05, n)

    # Fuel Flow (Litres / Hour): 12 - 32 L/h
    fuel_flow_base = 8.0 + (throttle / 100.0) * 22.0
    fuel_flow = fuel_flow_base + np.random.normal(0, 0.3, n)

    # 3. Fault Injections for Demo Scenarios
    fault_labels = ["Nominal"] * n

    if scenario == "turbo_failure":
        fault_start = int(120 * sampling_rate_hz)
        for i in range(fault_start, n):
            decay = min(1.0, (i - fault_start) / (60 * sampling_rate_hz))
            # Loss of turbo boost pressure
            manifold_pressure[i] -= decay * 8.5
            # Engine struggles, RPM drops slightly
            rpm[i] -= decay * 350
            # EGT increases due to leaner mixture / higher thermal load
            egt[i] += decay * 45
            fault_labels[i] = "Turbocharger Pressure Loss (MAP Drop)"

    elif scenario == "oil_leak":
        fault_start = int(130 * sampling_rate_hz)
        for i in range(fault_start, n):
            decay = min(1.0, (i - fault_start) / (50 * sampling_rate_hz))
            # Critical loss of oil pressure
            oil_pressure[i] = max(0.4, oil_pressure[i] - decay * 3.2)
            # Friction heats up remaining oil
            oil_temp[i] += decay * 35.0
            # Friction causes mechanical vibration
            vibration[i] += decay * 1.4
            fault_labels[i] = "Critical Oil Leakage / Lubrication Failure"

    elif scenario == "cht_overheat":
        fault_start = int(110 * sampling_rate_hz)
        for i in range(fault_start, n):
            decay = min(1.0, (i - fault_start) / (70 * sampling_rate_hz))
            # Cooling duct blockage or thermal runaway
            cht[i] += decay * 38.0
            oil_temp[i] += decay * 18.0
            fault_labels[i] = "Cylinder Head Overheat (Cooling Failure)"

    elif scenario == "fuel_clog":
        fault_start = int(140 * sampling_rate_hz)
        for i in range(fault_start, n):
            decay = min(1.0, (i - fault_start) / (40 * sampling_rate_hz))
            fuel_flow[i] = max(6.0, fuel_flow[i] - decay * 10.0)
            # Lean combustion causes sporadic EGT spikes and RPM flutter
            egt[i] += decay * 65.0 + np.random.normal(0, 8.0)
            rpm[i] -= decay * 250.0 + np.random.normal(0, 35.0)
            vibration[i] += decay * 0.8
            fault_labels[i] = "Fuel Line Restriction / Injector Clog"

    # 4. Construct Telemetry DataFrame
    telemetry_df = pd.DataFrame({
        "timestamp_s": np.round(time_steps, 2),
        "altitude_ft": np.round(altitude, 1),
        "throttle_pct": np.round(throttle, 1),
        "rpm": np.round(rpm, 1),
        "manifold_pressure_inHg": np.round(manifold_pressure, 2),
        "cht_celsius": np.round(cht, 1),
        "egt_celsius": np.round(egt, 1),
        "oil_pressure_bar": np.round(oil_pressure, 2),
        "oil_temp_celsius": np.round(oil_temp, 1),
        "fuel_flow_lph": np.round(fuel_flow, 2),
        "vibration_g": np.round(vibration, 3),
        "scenario_status": fault_labels
    })

    return telemetry_df


if __name__ == "__main__":
    df_normal = generate_engine_telemetry(duration_seconds=300, scenario="normal")
    print("Generated Normal Telemetry Shape:", df_normal.shape)
    print("First 3 rows:\n", df_normal.head(3))

    df_fault = generate_engine_telemetry(duration_seconds=300, scenario="turbo_failure")
    print("\nGenerated Turbo Fault Telemetry Shape:", df_fault.shape)
    print("Fault occurrences count:\n", df_fault["scenario_status"].value_counts())

