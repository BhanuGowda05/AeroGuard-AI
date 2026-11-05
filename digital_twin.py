"""
AeroGuardAI - Stage 2: Digital Twin Baseline & Diagnostic Logic
Uses only Python standard library, NumPy, and Pandas.
"""

from typing import Dict, Any, Tuple
import numpy as np
import pandas as pd


class AeroPistonDigitalTwin:
    """
    Digital Twin for a Turbocharged 4-Stroke Aero Piston Engine (Rotax 914 class)
    used in Medium Altitude Long Endurance (MALE) UAVs.

    The Digital Twin maintains an analytical nominal model of the engine.
    By comparing live sensor measurements against nominal digital twin predictions,
    it calculates residuals, evaluates subsystem health, and computes mission reliability.
    """

    def __init__(self):
        # Operational Redline Limits for Aero Piston Engines
        self.limits = {
            "rpm_max": 5800.0,
            "rpm_min": 1400.0,
            "cht_max_celsius": 135.0,        # Cylinder Head Temp redline
            "cht_warn_celsius": 125.0,
            "egt_max_celsius": 910.0,        # Exhaust Gas Temp redline
            "egt_warn_celsius": 880.0,
            "oil_press_min_bar": 1.5,        # Critical minimum lubrication pressure
            "oil_press_warn_bar": 2.0,
            "oil_temp_max_celsius": 130.0,    # Max oil temp redline
            "vibration_max_g": 2.0           # Excessive mechanical vibration
        }

    def compute_nominal_twin(self, throttle_pct: float, altitude_ft: float) -> Dict[str, float]:
        """
        Calculates theoretical/expected nominal engine sensor values based on operating point.
        """
        # Nominal RPM based on throttle
        rpm_expected = 2200.0 + (throttle_pct / 100.0) * 3600.0

        # Nominal Turbo Boost MAP (inHg)
        # Drops slightly with extreme altitude as compressor reaches operational limits
        map_expected = 26.0 + (throttle_pct / 100.0) * 13.5 - (altitude_ft / 20000.0) * 1.5

        # Nominal CHT (°C)
        cht_expected = 80.0 + (throttle_pct / 100.0) * 38.0 + (rpm_expected / 5800.0) * 12.0

        # Nominal EGT (°C)
        egt_expected = 730.0 + (throttle_pct / 100.0) * 130.0

        # Nominal Oil Pressure (bar)
        oil_press_expected = 2.5 + (rpm_expected / 5800.0) * 2.2

        # Nominal Oil Temp (°C)
        oil_temp_expected = 75.0 + (rpm_expected / 5800.0) * 28.0

        # Nominal Fuel Flow (L/h)
        fuel_flow_expected = 8.0 + (throttle_pct / 100.0) * 22.0

        # Nominal Vibration (g RMS)
        vibration_expected = 0.4 + (rpm_expected / 5800.0) * 0.6

        return {
            "rpm_expected": float(rpm_expected),
            "map_expected": float(map_expected),
            "cht_expected": float(cht_expected),
            "egt_expected": float(egt_expected),
            "oil_press_expected": float(oil_press_expected),
            "oil_temp_expected": float(oil_temp_expected),
            "fuel_flow_expected": float(fuel_flow_expected),
            "vibration_expected": float(vibration_expected)
        }

    def diagnose_frame(self, actual_sensors: Dict[str, float]) -> Dict[str, Any]:
        """
        Evaluates a single telemetry sample against the Digital Twin.
        Returns subsystem health scores, residuals, diagnosed anomalies, and mission advisory.
        """
        throttle = actual_sensors.get("throttle_pct", 70.0)
        altitude = actual_sensors.get("altitude_ft", 10000.0)
        twin = self.compute_nominal_twin(throttle, altitude)

        actual_rpm = actual_sensors.get("rpm", twin["rpm_expected"])
        actual_map = actual_sensors.get("manifold_pressure_inHg", twin["map_expected"])
        actual_cht = actual_sensors.get("cht_celsius", twin["cht_expected"])
        actual_egt = actual_sensors.get("egt_celsius", twin["egt_expected"])
        actual_oil_p = actual_sensors.get("oil_pressure_bar", twin["oil_press_expected"])
        actual_oil_t = actual_sensors.get("oil_temp_celsius", twin["oil_temp_expected"])
        actual_fuel = actual_sensors.get("fuel_flow_lph", twin["fuel_flow_expected"])
        actual_vib = actual_sensors.get("vibration_g", twin["vibration_expected"])

        # 1. Residuals (Actual - Twin Expected)
        res_map = actual_map - twin["map_expected"]
        res_cht = actual_cht - twin["cht_expected"]
        res_egt = actual_egt - twin["egt_expected"]
        res_oil_p = actual_oil_p - twin["oil_press_expected"]
        res_oil_t = actual_oil_t - twin["oil_temp_expected"]
        res_vib = actual_vib - twin["vibration_expected"]

        # 2. Subsystem Health Calculations (0.0 to 100.0%)
        # Turbo / Induction Health
        # Penalty when MAP is significantly below expected boost
        turbo_penalty = max(0.0, -res_map) * 12.0
        health_turbo = float(np.clip(100.0 - turbo_penalty, 0.0, 100.0))

        # Lubrication System Health
        # Severe penalty if oil pressure drops below nominal or oil temp spikes
        oil_p_penalty = max(0.0, -res_oil_p) * 35.0
        oil_t_penalty = max(0.0, res_oil_t) * 1.5
        health_lubrication = float(np.clip(100.0 - (oil_p_penalty + oil_t_penalty), 0.0, 100.0))

        # Cooling / Thermal Health
        # Sensitive to CHT rise above twin prediction
        cht_penalty = max(0.0, res_cht) * 2.8
        health_cooling = float(np.clip(100.0 - cht_penalty, 0.0, 100.0))

        # Combustion / Fuel System Health
        # Sensitive to abnormal EGT differences
        combustion_penalty = abs(res_egt) * 0.75
        health_combustion = float(np.clip(100.0 - combustion_penalty, 0.0, 100.0))

        # Mechanical Structural Health
        vib_penalty = max(0.0, res_vib) * 55.0
        health_mechanical = float(np.clip(100.0 - vib_penalty, 0.0, 100.0))

        # Overall Engine Health Index (EHI) - Weighted combination
        ehi = float(
            0.25 * health_lubrication +
            0.25 * health_cooling +
            0.20 * health_turbo +
            0.15 * health_combustion +
            0.15 * health_mechanical
        )

        # 3. Anomaly Detection & Diagnostic Root Cause
        anomalies = []
        severity = "NORMAL"

        if actual_oil_p < self.limits["oil_press_min_bar"]:
            anomalies.append(f"CRITICAL: Oil pressure at {actual_oil_p:.2f} bar (Min limit: {self.limits['oil_press_min_bar']} bar). Immediate engine seizure hazard!")
            severity = "CRITICAL"
        elif actual_oil_p < self.limits["oil_press_warn_bar"]:
            anomalies.append(f"CAUTION: Oil pressure degraded to {actual_oil_p:.2f} bar.")
            severity = "WARNING" if severity != "CRITICAL" else severity

        if actual_cht > self.limits["cht_max_celsius"]:
            anomalies.append(f"CRITICAL: CHT reached {actual_cht:.1f}°C (Exceeded redline {self.limits['cht_max_celsius']}°C). Thermal runaway!")
            severity = "CRITICAL"
        elif actual_cht > self.limits["cht_warn_celsius"]:
            anomalies.append(f"CAUTION: High CHT {actual_cht:.1f}°C. Coolant flow or airflow compromised.")
            severity = "WARNING" if severity != "CRITICAL" else severity

        if res_map < -4.0:
            anomalies.append(f"ALERT: Turbocharger Underboost: MAP is {res_map:.1f} inHg below Digital Twin expectations.")
            if severity == "NORMAL":
                severity = "WARNING"

        if actual_vib > self.limits["vibration_max_g"]:
            anomalies.append(f"ALERT: Severe engine vibration detected: {actual_vib:.2f} g.")
            severity = "CRITICAL"

        if not anomalies:
            anomalies.append("All engine subsystems operating within normal digital twin bounds.")

        # 4. Mission Reliability & Decision Advisory (Defence Pilot / Ground Operator Decision)
        if severity == "CRITICAL" or ehi < 55.0:
            mission_advisory = "ABORT MISSION (RTB IMMEDIATELY)"
            advisory_color = "red"
            reliability_score = max(10.0, ehi * 0.6)
            decision_text = "Critical engine health degradation detected. Proceed immediately to nearest recovery runway or emergency glide path."
        elif severity == "WARNING" or ehi < 80.0:
            mission_advisory = "MISSION DEGRADED (MONITOR CLOSELY)"
            advisory_color = "orange"
            reliability_score = ehi * 0.85
            decision_text = "Non-catastrophic anomaly detected. Restrict high-throttle manoeuvres and consider planned Return to Base (RTB)."
        else:
            mission_advisory = "MISSION GO (NOMINAL)"
            advisory_color = "green"
            reliability_score = min(99.0, ehi)
            decision_text = "Piston propulsion system fully nominal. Cleared for high-altitude loiter and operational tasking."

        return {
            "ehi": round(ehi, 1),
            "reliability_score": round(reliability_score, 1),
            "severity": severity,
            "mission_advisory": mission_advisory,
            "advisory_color": advisory_color,
            "decision_text": decision_text,
            "anomalies": anomalies,
            "subsystems": {
                "Lubrication": round(health_lubrication, 1),
                "Cooling": round(health_cooling, 1),
                "Turbo / Induction": round(health_turbo, 1),
                "Combustion": round(health_combustion, 1),
                "Mechanical Integrity": round(health_mechanical, 1)
            },
            "residuals": {
                "map_residual": round(res_map, 2),
                "cht_residual": round(res_cht, 1),
                "egt_residual": round(res_egt, 1),
                "oil_p_residual": round(res_oil_p, 2),
                "oil_t_residual": round(res_oil_t, 1),
                "vib_residual": round(res_vib, 3)
            },
            "twin_expected": twin
        }

    def process_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Runs digital twin diagnostics on an entire flight telemetry dataframe.
        """
        results = []
        for _, row in df.iterrows():
            diag = self.diagnose_frame(row.to_dict())
            results.append({
                "ehi": diag["ehi"],
                "reliability_score": diag["reliability_score"],
                "severity": diag["severity"],
                "mission_advisory": diag["mission_advisory"],
                "health_lubrication": diag["subsystems"]["Lubrication"],
                "health_cooling": diag["subsystems"]["Cooling"],
                "health_turbo": diag["subsystems"]["Turbo / Induction"],
                "health_combustion": diag["subsystems"]["Combustion"],
                "health_mechanical": diag["subsystems"]["Mechanical Integrity"],
                "map_residual": diag["residuals"]["map_residual"],
                "cht_residual": diag["residuals"]["cht_residual"],
                "oil_p_residual": diag["residuals"]["oil_p_residual"]
            })
        diag_df = pd.DataFrame(results)
        return pd.concat([df.reset_index(drop=True), diag_df], axis=1)


if __name__ == "__main__":
    from engine_simulator import generate_engine_telemetry

    twin = AeroPistonDigitalTwin()
    df_sim = generate_engine_telemetry(duration_seconds=200, scenario="oil_leak")
    df_analyzed = twin.process_dataframe(df_sim)

    print("Diagnostic processing complete.")
    print("Columns available:", list(df_analyzed.columns))
    print("\nSample at t = 50s (Normal Climb):")
    sample_50 = df_analyzed.iloc[50]
    print(f"RPM: {sample_50['rpm']}, EHI: {sample_50['ehi']}%, Advisory: {sample_50['mission_advisory']}")

    print("\nSample at t = 180s (Oil Leak Fault):")
    sample_180 = df_analyzed.iloc[180]
    print(f"Oil Press: {sample_180['oil_pressure_bar']} bar, EHI: {sample_180['ehi']}%, Advisory: {sample_180['mission_advisory']}")

