"""
AeroGuard AI - AI-Based Digital Twin for Health Monitoring, Fault Detection 
and Mission Reliability Enhancement of Aero Piston Engines used in MALE UAVs.

Theme: AI in Defence
Technology Stack: Python, Streamlit, Pandas, NumPy, Plotly
"""

import os
import io
import time
from datetime import datetime
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st

# ==============================================================================
# 1. PAGE CONFIGURATION & DEFENCE UI THEME
# ==============================================================================
st.set_page_config(
    page_title="AeroGuard AI - Defence Engine Digital Twin",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Deep Space Navy Aerospace & Digital Twin Telemetry Theme (Reference Image Style)
st.markdown("""
<style>
    /* Global Base & Aerospace Theme */
    .stApp {
        background: radial-gradient(ellipse at 50% 15%, #08162e 0%, #040914 65%, #02050b 100%) !important;
        background-attachment: fixed !important;
        color: #f8fafc;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    }

    /* Sidebar Background & Aesthetics */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #050d1a 0%, #03070f 100%) !important;
        border-right: 1px solid rgba(56, 189, 248, 0.15) !important;
    }
    
    /* Top Header Bar */
    .defence-header {
        background: linear-gradient(135deg, rgba(8, 22, 48, 0.9) 0%, rgba(4, 12, 28, 0.95) 100%);
        border: 1px solid rgba(56, 189, 248, 0.35);
        border-radius: 12px;
        padding: 16px 24px;
        margin-bottom: 20px;
        box-shadow: 0 4px 25px rgba(0, 242, 254, 0.1), inset 0 0 15px rgba(56, 189, 248, 0.05);
    }
    .defence-title {
        font-size: 26px;
        font-weight: 800;
        letter-spacing: 1px;
        color: #f8fafc;
        margin: 0;
        text-shadow: 0 0 12px rgba(56, 189, 248, 0.5);
    }
    .defence-subtitle {
        font-size: 13px;
        color: #38bdf8;
        letter-spacing: 0.5px;
        font-weight: 600;
        margin-top: 4px;
    }

    /* Digital Twin Reference Top Header */
    .dt-topbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: rgba(6, 15, 33, 0.85);
        border: 1px solid rgba(56, 189, 248, 0.28);
        border-radius: 12px;
        padding: 18px 24px;
        margin-bottom: 22px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5), inset 0 0 15px rgba(56, 189, 248, 0.04);
    }
    .dt-brand {
        display: flex;
        flex-direction: column;
    }
    .dt-title {
        font-size: 24px;
        font-weight: 900;
        letter-spacing: 2px;
        color: #ffffff;
        text-transform: uppercase;
        margin: 0;
        line-height: 1.1;
    }
    .dt-subtitle {
        font-size: 13px;
        font-weight: 700;
        letter-spacing: 1.5px;
        color: #38bdf8;
        text-transform: uppercase;
        margin-top: 4px;
    }
    .dt-kpi-group {
        display: flex;
        gap: 36px;
        align-items: center;
    }
    .dt-kpi {
        text-align: left;
    }
    .dt-kpi-label {
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 1.2px;
        color: #94a3b8;
        text-transform: uppercase;
    }
    .dt-kpi-val {
        font-size: 22px;
        font-weight: 800;
        color: #ffffff;
        margin-top: 2px;
    }
    .dt-kpi-unit {
        font-size: 13px;
        color: #38bdf8;
        font-weight: 600;
        margin-left: 3px;
    }

    /* Reference Style Top Right Maintenance Badge */
    .dt-alert-box {
        background: rgba(10, 24, 48, 0.7);
        border: 1px solid rgba(56, 189, 248, 0.35);
        border-radius: 10px;
        padding: 10px 18px;
        display: flex;
        align-items: center;
        gap: 14px;
        box-shadow: 0 0 15px rgba(56, 189, 248, 0.1);
    }
    .dt-alert-icon {
        font-size: 28px;
        line-height: 1;
    }
    .dt-alert-texts {
        display: flex;
        flex-direction: column;
    }
    .dt-alert-header {
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 1px;
        color: #cbd5e1;
        text-transform: uppercase;
    }
    .dt-alert-status {
        font-size: 14px;
        font-weight: 700;
    }

    /* Status Banner */
    .status-banner {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: rgba(7, 18, 38, 0.85);
        border: 1px solid rgba(56, 189, 248, 0.25);
        border-radius: 10px;
        padding: 14px 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4);
    }
    .badge-healthy {
        background: linear-gradient(90deg, rgba(6, 78, 59, 0.8) 0%, rgba(2, 44, 34, 0.8) 100%);
        border: 1px solid #10b981;
        color: #6ee7b7;
        padding: 8px 16px;
        border-radius: 8px;
        font-size: 16px;
        font-weight: 700;
        display: inline-block;
        box-shadow: 0 0 12px rgba(16, 185, 129, 0.2);
    }
    .badge-warning {
        background: linear-gradient(90deg, rgba(120, 53, 15, 0.8) 0%, rgba(69, 26, 3, 0.8) 100%);
        border: 1px solid #f59e0b;
        color: #fde68a;
        padding: 8px 16px;
        border-radius: 8px;
        font-size: 16px;
        font-weight: 700;
        display: inline-block;
        box-shadow: 0 0 12px rgba(245, 158, 11, 0.2);
    }
    .badge-critical {
        background: linear-gradient(90deg, rgba(127, 29, 29, 0.8) 0%, rgba(69, 10, 10, 0.8) 100%);
        border: 1px solid #ef4444;
        color: #fca5a5;
        padding: 8px 16px;
        border-radius: 8px;
        font-size: 16px;
        font-weight: 700;
        display: inline-block;
        box-shadow: 0 0 12px rgba(239, 68, 68, 0.25);
    }

    /* Sensor Metric Cards */
    .sensor-card {
        background: rgba(7, 18, 38, 0.8);
        border: 1px solid rgba(56, 189, 248, 0.2);
        border-radius: 10px;
        padding: 16px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4), inset 0 0 10px rgba(56, 189, 248, 0.03);
    }
    .sensor-label {
        font-size: 11px;
        color: #94a3b8;
        text-transform: uppercase;
        font-weight: 700;
        letter-spacing: 0.8px;
    }
    .sensor-val {
        font-size: 24px;
        font-weight: 800;
        color: #ffffff;
        margin: 6px 0;
    }
    .tag-healthy {
        background-color: rgba(16, 185, 129, 0.15);
        color: #34d399;
        border: 1px solid #10b981;
        padding: 3px 8px;
        border-radius: 4px;
        font-size: 11px;
        font-weight: 700;
    }
    .tag-warning {
        background-color: rgba(245, 158, 11, 0.15);
        color: #fbbf24;
        border: 1px solid #f59e0b;
        padding: 3px 8px;
        border-radius: 4px;
        font-size: 11px;
        font-weight: 700;
    }
    .tag-critical {
        background-color: rgba(239, 68, 68, 0.15);
        color: #f87171;
        border: 1px solid #ef4444;
        padding: 3px 8px;
        border-radius: 4px;
        font-size: 11px;
        font-weight: 700;
    }

    /* Left Column Sensor Gauge Cards (Reference Image Style) */
    .gauge-widget {
        background: rgba(6, 16, 36, 0.75);
        border: 1px solid rgba(56, 189, 248, 0.25);
        border-radius: 12px;
        padding: 14px 18px;
        margin-bottom: 14px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4);
    }
    .gauge-header-row {
        display: flex;
        justify-content: space-between;
        align-items: baseline;
        margin-bottom: 10px;
    }
    .gauge-code {
        font-size: 14px;
        font-weight: 800;
        color: #94a3b8;
        letter-spacing: 1px;
    }
    .gauge-val {
        font-size: 26px;
        font-weight: 900;
        color: #ffffff;
        letter-spacing: 0.5px;
    }
    .gauge-body-row {
        display: flex;
        align-items: center;
        gap: 16px;
    }
    .capsule-track {
        width: 14px;
        height: 64px;
        background: rgba(15, 23, 42, 0.9);
        border: 1px solid rgba(56, 189, 248, 0.3);
        border-radius: 8px;
        overflow: hidden;
        display: flex;
        flex-direction: column;
        justify-content: flex-end;
        box-shadow: inset 0 2px 5px rgba(0,0,0,0.6);
    }
    .capsule-fill {
        width: 100%;
        border-radius: 0 0 6px 6px;
        transition: height 0.4s ease;
    }
    .dial-container {
        flex: 1;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    /* Right Column: Parameters Panel (Reference Image Style) */
    .parameters-box {
        background: rgba(6, 16, 36, 0.85);
        border: 1px solid rgba(56, 189, 248, 0.28);
        border-radius: 12px;
        padding: 18px 20px;
        margin-bottom: 16px;
        box-shadow: 0 4px 18px rgba(0, 0, 0, 0.45);
    }
    .param-title {
        font-size: 13px;
        font-weight: 900;
        letter-spacing: 2px;
        color: #ffffff;
        text-transform: uppercase;
        margin-bottom: 14px;
        border-bottom: 1px solid rgba(56, 189, 248, 0.18);
        padding-bottom: 6px;
    }
    .param-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 8px 0;
        border-bottom: 1px solid rgba(255, 255, 255, 0.04);
    }
    .param-label {
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 1.2px;
        color: #94a3b8;
        text-transform: uppercase;
    }
    .param-number {
        font-size: 18px;
        font-weight: 800;
        color: #ffffff;
    }
    .param-unit-tag {
        font-size: 11px;
        color: #38bdf8;
        font-weight: 600;
        margin-left: 4px;
    }

    /* Content Cards */
    .card-box {
        background: rgba(7, 18, 38, 0.8);
        border: 1px solid rgba(56, 189, 248, 0.22);
        border-radius: 10px;
        padding: 18px;
        margin-bottom: 16px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.35);
    }

    .injection-box {
        background: linear-gradient(135deg, rgba(8, 22, 48, 0.95) 0%, rgba(20, 16, 55, 0.95) 60%, rgba(7, 18, 38, 0.95) 100%);
        border: 1px solid rgba(99, 102, 241, 0.45);
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 20px rgba(99, 102, 241, 0.2);
    }

    /* Clean Aerospace Alert & Disclaimer */
    .disclaimer-box {
        background: rgba(7, 18, 38, 0.85);
        border-left: 4px solid #38bdf8;
        padding: 10px 14px;
        border-radius: 0 8px 8px 0;
        font-size: 13px;
        color: #94a3b8;
        margin-bottom: 20px;
        border-top: 1px solid rgba(56, 189, 248, 0.15);
        border-right: 1px solid rgba(56, 189, 248, 0.15);
        border-bottom: 1px solid rgba(56, 189, 248, 0.15);
    }
</style>
""", unsafe_allow_html=True)


# ==============================================================================
# 2. SESSION STATE MANAGEMENT FOR FAULT INJECTION & SCENARIOS
# ==============================================================================
if "active_fault" not in st.session_state:
    st.session_state["active_fault"] = None
if "injected_params" not in st.session_state:
    st.session_state["injected_params"] = {
        "temp": 85.0,
        "oil": 65.0,
        "vib": 3.0,
        "rpm": 3000.0,
        "sensor_failure": None
    }
if "detection_time_ms" not in st.session_state:
    st.session_state["detection_time_ms"] = None
if "affected_param" not in st.session_state:
    st.session_state["affected_param"] = None
if "fault_timestamp" not in st.session_state:
    st.session_state["fault_timestamp"] = None


# ==============================================================================
# 3. DIGITAL TWIN RULE-BASED ANOMALY & HEALTH ENGINE
# ==============================================================================
THRESHOLDS = {
    "temp_max": 110.0,       # Temperature > 110°C = High temperature
    "oil_press_min": 30.0,   # Oil pressure < 30 PSI = Low oil pressure
    "vib_max": 7.0,          # Vibration > 7.0 = Abnormal vibration
    "rpm_max": 5000.0        # RPM > 5000 = High RPM
}

def generate_explainable_alerts(temp: float, oil_press: float, vib: float, rpm: float, sensor_failure: str = None, active_fault_name: str = None):
    """
    FEATURE 3: EXPLAINABLE ALERTS WITH ACTIONABLE SUGGESTIONS
    
    Provides simple, understandable explanations whenever an abnormal engine condition is detected.
    Identifies the highest-priority fault based on severity.
    """
    alerts = []

    # 1. Oil Pressure Drop (Engine Alert!)
    if not (sensor_failure and "Oil" in sensor_failure):
        if oil_press < THRESHOLDS["oil_press_min"]:
            alerts.append({
                "alert_title": "Engine Alert!",
                "parameter": "Oil Pressure",
                "reading": f"{oil_press:.1f} PSI",
                "threshold": "< 30 PSI",
                "reason": "Oil pressure is below the illustrative threshold.",
                "suggestion": "Inspect the lubrication system and check for possible oil leakage.",
                "severity": "CRITICAL",
                "priority_rank": 1,
                "priority_reason": "Oil pressure loss directly compromises hydrodynamic bearing lubrication, posing an immediate risk of catastrophic engine seizure within minutes.",
                "why_generated": (
                    f"Oil pressure ({oil_press:.1f} PSI) has fallen below the 30.0 PSI illustrative safety threshold. "
                    f"Aero piston engines rely on pressurized oil to cushion crankshaft journals and dissipate friction heat. "
                    f"Operating below 30 PSI leads to accelerated bearing wipe and rapid mechanical lockup."
                )
            })

    # 2. Engine Overheating (High Temperature Alert!)
    if not (sensor_failure and "Temperature" in sensor_failure):
        if temp > THRESHOLDS["temp_max"]:
            is_extreme = temp >= 125.0
            alerts.append({
                "alert_title": "High Temperature Alert!",
                "parameter": "Engine Temperature",
                "reading": f"{temp:.1f}°C",
                "threshold": "> 110°C",
                "reason": "Engine temperature is above the illustrative threshold.",
                "suggestion": "Inspect the cooling system.",
                "severity": "CRITICAL" if is_extreme else "HIGH",
                "priority_rank": 1 if is_extreme else 2,
                "priority_reason": "Excessive cylinder head temperature induces severe thermal fatigue, risks cylinder distortion, and accelerates lubricant breakdown.",
                "why_generated": (
                    f"Engine Temperature ({temp:.1f}°C) is above the 110.0°C demonstration limit. "
                    f"In air-cooled or liquid-cooled aero piston engines, prolonged elevated temperature causes cylinder head distortion, "
                    f"micro-welding of piston rings to cylinder walls, and vapor lock."
                )
            })

    # 3. Abnormal Vibration OR Spark Plug Misfire (Vibration Alert! or Ignition Fault Alert!)
    if vib > THRESHOLDS["vib_max"]:
        if active_fault_name and "Spark Plug Misfire" in active_fault_name:
            alerts.append({
                "alert_title": "Ignition Fault Alert!",
                "parameter": "Ignition System / Spark Plugs",
                "reading": f"{vib:.1f} (Combustion Shudder)",
                "threshold": "Combustion Stability (Max 7.0)",
                "reason": "Simulated misfire detected through abnormal engine behaviour.",
                "suggestion": "Inspect the ignition system and spark plugs.",
                "severity": "HIGH",
                "priority_rank": 2,
                "priority_reason": "Combustion misfire causes cyclic torque spikes and harmonic oscillations that fatigue engine mounts and reduction gearboxes.",
                "why_generated": (
                    f"Simulated spark plug misfire created uneven combustion strokes across opposed cylinders, "
                    f"manifesting as cyclic torque shudder and elevated vibration ({vib:.1f} > 7.0). "
                    f"Unaddressed misfire leads to unburnt fuel cylinder wash and spark plug fouling."
                )
            })
        else:
            alerts.append({
                "alert_title": "Vibration Alert!",
                "parameter": "Engine Vibration",
                "reading": f"{vib:.1f} / 10",
                "threshold": "> 7.0",
                "reason": "Vibration exceeds the illustrative threshold.",
                "suggestion": "Inspect engine mounting and rotating components.",
                "severity": "HIGH",
                "priority_rank": 2,
                "priority_reason": "Excessive vibration causes structural fatigue in airframe mounts, electrical harnesses, and fuel lines.",
                "why_generated": (
                    f"Vibration level ({vib:.1f}) exceeds the 7.0 illustrative threshold. "
                    f"High-frequency vibration indicates rotating component unbalance, propeller track discrepancy, or deteriorated rubber shock mounts."
                )
            })

    # 4. High RPM (RPM Alert!)
    if rpm > THRESHOLDS["rpm_max"]:
        alerts.append({
            "alert_title": "RPM Alert!",
            "parameter": "Engine RPM",
            "reading": f"{rpm:.0f} RPM",
            "threshold": "> 5000 RPM",
            "reason": "RPM exceeds the illustrative demonstration threshold.",
            "suggestion": "Check engine operating conditions against approved operating limits.",
            "severity": "WARNING",
            "priority_rank": 3,
            "priority_reason": "Engine speed exceeds rated cruise envelope, increasing centrifugal stresses and accelerated ring wear.",
            "why_generated": (
                f"Engine RPM ({rpm:.0f} RPM) exceeds the 5000 RPM demonstration limit. "
                f"Operating at elevated engine speed increases valvetrain floating risk and friction wear."
            )
        })

    # 5. Sensor Hardware / Signal Failure (Sensor Fault Alert!)
    if sensor_failure:
        alerts.append({
            "alert_title": "Sensor Fault Alert!",
            "parameter": f"Sensor Signal ({sensor_failure})",
            "reading": "INVALID (Signal Lost)",
            "threshold": "Continuous Signal Required",
            "reason": "Sensor signal is out-of-range or invalid (signal lost).",
            "suggestion": "Inspect sensor wiring harness and replace the transducer.",
            "severity": "HIGH",
            "priority_rank": 2,
            "priority_reason": "Loss of sensor data compromises telemetry integrity, preventing flight operators from monitoring engine health.",
            "why_generated": (
                f"Telemetry channel reports open circuit or invalid reading for {sensor_failure}. "
                f"Without verified sensor data, the Digital Twin cannot evaluate operating margins for this subsystem."
            )
        })

    # Sort alerts by priority_rank (1=CRITICAL first, 2=HIGH, 3=WARNING)
    alerts.sort(key=lambda x: x["priority_rank"])

    highest_priority = alerts[0] if len(alerts) > 0 else None

    return alerts, highest_priority

def analyze_engine_state(temp: float, oil_press: float, vib: float, rpm: float, sensor_failure: str = None, active_fault_name: str = None):
    """
    Transparent, explainable rule-based anomaly detection engine.
    
    100-Point Scoring Model:
    - Base: 100 points
    - Deduct 25 for temp > 110°C
    - Deduct 25 for oil < 30 PSI
    - Deduct 25 for vib > 7.0
    - Deduct 15 for rpm > 5000
    - Deduct 30 for sensor failure / signal disconnection
    - Clamped: min = 0
    
    Classification:
    - 75–100: HEALTHY (no active faults)
    - 40–74: WARNING
    - < 40: CRITICAL
    """
    score = 100
    fault_details = []
    deductions = []

    # 0. Check for Simulated Sensor Hardware / Signal Failure
    if sensor_failure:
        score -= 30
        deductions.append({
            "param": f"Sensor Signal ({sensor_failure})",
            "condition": "Signal Open-Circuit / Invalid Data",
            "pts": -30
        })
        fault_details.append({
            "param": f"Sensor Signal ({sensor_failure})",
            "val": "INVALID (ERR_OOR / DISCONNECTED)",
            "thresh": "Signal Continuity Required",
            "warning": f"Sensor Failure: {sensor_failure} data stream invalid.",
            "explanation": f"The telemetry bus reports an open-circuit or invalid data stream for {sensor_failure}. Real-time monitoring of this channel is compromised.",
            "recommendation": f"Recommend inspecting wiring harness, 5V reference line, and replacing {sensor_failure} transducer."
        })

    # 1. Temperature Check (only if sensor is not failed/disconnected)
    if not (sensor_failure and "Temperature" in sensor_failure):
        if temp > THRESHOLDS["temp_max"]:
            score -= 25
            deductions.append({"param": "Engine Temperature", "condition": f"{temp:.1f}°C > 110°C", "pts": -25})
            fault_details.append({
                "param": "Engine Temperature",
                "val": f"{temp:.1f}°C",
                "thresh": "> 110°C",
                "warning": "High temperature detected.",
                "explanation": f"Engine Temperature ({temp:.1f}°C) is above the 110°C threshold, indicating insufficient cooling airflow or high combustion heat.",
                "recommendation": "Recommend inspecting the cooling system."
            })

    # 2. Oil Pressure Check
    if not (sensor_failure and "Oil" in sensor_failure):
        if oil_press < THRESHOLDS["oil_press_min"]:
            score -= 25
            deductions.append({"param": "Oil Pressure", "condition": f"{oil_press:.1f} PSI < 30 PSI", "pts": -25})
            fault_details.append({
                "param": "Oil Pressure",
                "val": f"{oil_press:.1f} PSI",
                "thresh": "< 30 PSI",
                "warning": "Low oil pressure detected.",
                "explanation": f"Oil Pressure ({oil_press:.1f} PSI) has fallen below the 30 PSI safety threshold, compromising hydrodynamic lubrication.",
                "recommendation": "Recommend inspecting the lubrication system."
            })

    # 3. Vibration Check
    if vib > THRESHOLDS["vib_max"]:
        score -= 25
        deductions.append({"param": "Vibration", "condition": f"{vib:.1f} > 7.0", "pts": -25})
        fault_details.append({
            "param": "Vibration",
            "val": f"{vib:.1f}",
            "thresh": "> 7.0",
            "warning": "Abnormal vibration detected.",
            "explanation": f"Vibration level ({vib:.1f}) exceeds the 7.0 threshold, indicating dynamic imbalance, cylinder misfire, or mount degradation.",
            "recommendation": "Recommend inspecting engine mounting and rotating components."
        })

    # 4. Engine RPM Check
    if rpm > THRESHOLDS["rpm_max"]:
        score -= 15
        deductions.append({"param": "Engine RPM", "condition": f"{rpm:.0f} RPM > 5000 RPM", "pts": -15})
        fault_details.append({
            "param": "Engine RPM",
            "val": f"{rpm:.0f} RPM",
            "thresh": "> 5000 RPM",
            "warning": "High RPM detected.",
            "explanation": f"Engine RPM ({rpm:.0f} RPM) is exceeding the 5000 RPM threshold, placing continuous stress on the powertrain.",
            "recommendation": "Recommend checking the engine operating condition against its approved operating limits."
        })

    health_score = max(0, score)

    # Feature 3: Generate structured explainable alerts & highest-priority identification
    explainable_alerts, highest_priority_fault = generate_explainable_alerts(
        temp, oil_press, vib, rpm, sensor_failure=sensor_failure, active_fault_name=active_fault_name
    )

    # Status determination (No "Continue Mission" claims)
    if len(fault_details) == 0 and health_score >= 75:
        status = "HEALTHY"
        condition_guidance = "GOOD CONDITION (All simulated parameters nominal)"
        maint_priority = "ROUTINE PRE-FLIGHT / POST-FLIGHT INSPECTION"
    elif health_score >= 40:
        status = "WARNING"
        condition_guidance = "CAUTION (Subsystem degradation detected; refer to maintenance manual)"
        maint_priority = "SCHEDULED FLIGHT-LINE INTERVENTION REQUIRED"
    else:
        status = "CRITICAL"
        condition_guidance = "HIGH RISK (Critical threshold breach; authorized abort evaluation required)"
        maint_priority = "AIRCRAFT GROUNDED: IMMEDIATE FULL ENGINE TEARDOWN & OVERHAUL"

    return {
        "health_score": health_score,
        "status": status,
        "fault_details": fault_details,
        "explainable_alerts": explainable_alerts,
        "highest_priority_fault": highest_priority_fault,
        "deductions": deductions,
        "condition_guidance": condition_guidance,
        "maint_priority": maint_priority
    }


# ==============================================================================
# 4. FEATURE 2 — DYNAMIC MISSION RELIABILITY SCORE ENGINE
# ==============================================================================
def compute_mission_reliability(temp: float, oil_press: float, vib: float, rpm: float, fault_details: list, sensor_failure: str = None):
    """
    Calculates an illustrative Mission Reliability Score (0 to 100%) based on weighted 
    endurance risk factors. Distinct from discrete health point deductions.
    
    Formula:
    - Lubrication factor (35% weight)
    - Thermal endurance factor (25% weight)
    - Vibration structural factor (25% weight)
    - RPM powertrain wear factor (15% weight)
    - Additional penalty for active fault count or sensor failure
    
    Condition Brackets:
    - 75–100%: GOOD CONDITION
    - 40–74%: CAUTION
    - Below 40%: HIGH RISK
    """
    # 1. Lubrication factor (35% weight)
    effective_oil = oil_press
    if effective_oil >= 55.0:
        r_oil = 100.0
    elif effective_oil >= 30.0:
        r_oil = 70.0 + ((effective_oil - 30.0) / 25.0) * 30.0
    elif effective_oil >= 15.0:
        r_oil = 30.0 + ((effective_oil - 15.0) / 15.0) * 40.0
    else:
        r_oil = max(5.0, (effective_oil / 15.0) * 30.0)

    # 2. Thermal endurance factor (25% weight)
    if sensor_failure and "Temperature" in sensor_failure:
        r_temp = 40.0
    else:
        if temp <= 95.0:
            r_temp = 100.0
        elif temp <= 110.0:
            r_temp = 75.0 + ((110.0 - temp) / 15.0) * 25.0
        elif temp <= 125.0:
            r_temp = 35.0 + ((125.0 - temp) / 15.0) * 40.0
        else:
            r_temp = max(5.0, 35.0 - (temp - 125.0) * 2.0)

    # 3. Vibration structural factor (25% weight)
    if vib <= 4.0:
        r_vib = 100.0
    elif vib <= 7.0:
        r_vib = 65.0 + ((7.0 - vib) / 3.0) * 35.0
    elif vib <= 8.5:
        r_vib = 25.0 + ((8.5 - vib) / 1.5) * 40.0
    else:
        r_vib = max(5.0, 25.0 - (vib - 8.5) * 10.0)

    # 4. RPM powertrain wear factor (15% weight)
    if 2400 <= rpm <= 4500:
        r_rpm = 100.0
    elif rpm < 2400:
        r_rpm = max(40.0, 70.0 + (rpm / 2400.0) * 30.0)
    elif rpm <= 5000:
        r_rpm = 70.0 + ((5000.0 - rpm) / 500.0) * 30.0
    else:
        r_rpm = max(10.0, 70.0 - ((rpm - 5000.0) / 1000.0) * 50.0)

    # Base weighted sum
    weighted_score = (0.35 * r_oil) + (0.25 * r_temp) + (0.25 * r_vib) + (0.15 * r_rpm)

    # Fault severity adjustment
    fault_count = len(fault_details)
    penalty = 0.0
    if sensor_failure:
        penalty += 25.0
    if fault_count >= 3:
        penalty += 35.0
    elif fault_count == 2:
        penalty += 28.0
    elif fault_count == 1:
        penalty += 20.0

    reliability = round(max(0.0, min(100.0, weighted_score - penalty)), 1)

    # Condition label & color strictly matching requirements:
    # 75–100: GOOD CONDITION
    # 40–74: CAUTION
    # Below 40: HIGH RISK
    if reliability >= 75.0:
        condition_label = "GOOD CONDITION"
        condition_color = "#10b981"
        badge_class = "badge-healthy"
    elif reliability >= 40.0:
        condition_label = "CAUTION"
        condition_color = "#f59e0b"
        badge_class = "badge-warning"
    else:
        condition_label = "HIGH RISK"
        condition_color = "#ef4444"
        badge_class = "badge-critical"

    # Dynamic explanation of why score changed
    reasons = []
    if r_oil < 70.0:
        reasons.append(f"sub-optimal oil pressure ({oil_press:.1f} PSI), increasing lubrication breakdown risk")
    if r_temp < 75.0:
        reasons.append(f"elevated engine temperature ({temp:.1f}°C), causing accelerated thermal stress")
    if r_vib < 65.0:
        reasons.append(f"abnormal vibration level ({vib:.1f}/10), accelerating airframe dynamic fatigue")
    if r_rpm < 70.0:
        reasons.append(f"sustained high RPM ({rpm:.0f} RPM), creating continuous cycle fatigue")
    if sensor_failure:
        reasons.append(f"telemetry signal loss on {sensor_failure}")

    if not reasons:
        explanation = (
            "Engine is operating in optimal thermodynamic and mechanical balance. All propulsion subsystems "
            "indicate high simulated mission endurance reliability."
        )
    else:
        explanation = (
            f"Reliability is at {reliability:.1f}% ({condition_label}) driven primarily by "
            f"{', and '.join(reasons)}."
        )

    sub_factors = {
        "Lubrication Reliability (35% wt)": round(r_oil, 1),
        "Thermal Endurance (25% wt)": round(r_temp, 1),
        "Structural / Vibration (25% wt)": round(r_vib, 1),
        "Powertrain Speed (15% wt)": round(r_rpm, 1)
    }

    return {
        "reliability_score": reliability,
        "condition_label": condition_label,
        "condition_color": condition_color,
        "badge_class": badge_class,
        "explanation": explanation,
        "sub_factors": sub_factors
    }


# ==============================================================================
# 5. NUMPY HISTORICAL TELEMETRY GENERATOR
# ==============================================================================
def generate_sensor_history(curr_temp, curr_oil, curr_vib, curr_rpm, points=60, seed=42):
    """Generates simulated time-series history leading up to the current state."""
    np.random.seed(seed)
    time_series = np.arange(-points + 1, 1)  # -59s to 0s
    n = len(time_series)
    
    progress = np.linspace(0.15, 1.0, n)
    
    effective_temp = 85.0 if curr_temp < 0 else curr_temp
    effective_oil = curr_oil
    effective_vib = curr_vib
    effective_rpm = curr_rpm

    temp_hist = (1 - progress) * 85.0 + progress * effective_temp + np.random.normal(0, 0.4, n)
    oil_hist = (1 - progress) * 65.0 + progress * effective_oil + np.random.normal(0, 0.5, n)
    vib_hist = (1 - progress) * 3.0 + progress * effective_vib + np.random.normal(0, 0.1, n)
    rpm_hist = (1 - progress) * 3000.0 + progress * effective_rpm + np.random.normal(0, 15.0, n)

    oil_hist = np.clip(oil_hist, 0.0, 100.0)
    vib_hist = np.clip(vib_hist, 0.0, 10.0)
    rpm_hist = np.clip(rpm_hist, 0.0, 6000.0)

    health_hist = []
    reliability_hist = []
    for i in range(n):
        res = analyze_engine_state(temp_hist[i], oil_hist[i], vib_hist[i], rpm_hist[i])
        rel = compute_mission_reliability(temp_hist[i], oil_hist[i], vib_hist[i], rpm_hist[i], res["fault_details"])
        health_hist.append(res["health_score"])
        reliability_hist.append(rel["reliability_score"])

    return pd.DataFrame({
        "time_seconds": time_series,
        "temperature_c": np.round(temp_hist, 1),
        "oil_pressure_psi": np.round(oil_hist, 1),
        "vibration_level": np.round(vib_hist, 2),
        "rpm": np.round(rpm_hist, 0),
        "health_score": np.round(health_hist, 1),
        "reliability_score": np.round(reliability_hist, 1)
    })

def calculate_trend_direction(series: pd.Series, threshold_delta: float):
    """Calculates trend direction between first 10s and last 10s."""
    initial_mean = series.head(10).mean()
    recent_mean = series.tail(10).mean()
    delta = recent_mean - initial_mean

    if delta > threshold_delta:
        return "Increasing", "▲", "#ef4444" if threshold_delta > 0 else "#38bdf8", delta
    elif delta < -threshold_delta:
        return "Decreasing", "▼", "#38bdf8" if threshold_delta > 0 else "#ef4444", delta
    else:
        return "Stable", "■", "#10b981", delta


# ==============================================================================
# 6. ENHANCED VIRTUAL ENGINE MONITORING SCHEMATIC (PLOTLY)
# ==============================================================================
def create_virtual_engine_figure(temp, oil_press, vib, rpm, status, sensor_failure=None):
    """
    Creates an interactive 2D engineering schematic of a 4-cylinder aero piston engine.
    Styled as a CAD Digital Twin with glowing cyan outlines, callout pins, and component nodes.
    """
    if sensor_failure and "Temperature" in sensor_failure:
        temp_color = "#f59e0b"
        temp_label = "SENSOR FAIL"
    else:
        temp_color = "#00f2fe" if temp <= 110 else "#ef4444"
        temp_label = f"{temp:.0f}°C"

    oil_color = "#00f2fe" if oil_press >= 30 else "#ef4444"
    vib_color = "#00f2fe" if vib <= 7.0 else "#ef4444"
    rpm_color = "#38bdf8" if rpm <= 5000 else "#ef4444"

    fig = go.Figure()

    # Outer CAD Casing / Nacelle Envelope (Digital Twin Aerospace Boundary)
    fig.add_shape(
        type="rect", x0=-6.2, y0=-3.0, x1=6.2, y1=3.2,
        fillcolor="rgba(8, 20, 44, 0.45)",
        line=dict(color="rgba(0, 242, 254, 0.25)", width=1.5, dash="dot"),
        layer="below"
    )

    # 1. Crankcase / Engine Core (Center)
    fig.add_shape(
        type="rect", x0=-2.2, y0=-1.6, x1=2.2, y1=1.6,
        fillcolor="rgba(10, 24, 48, 0.9)", line=dict(color=vib_color, width=3.5),
        layer="below"
    )
    fig.add_annotation(
        x=0, y=0,
        text=f"<b>ENGINE CRANKCASE</b><br>Vibration: {vib:.1f} / 10<br><span style='font-size:10px; color:{vib_color};'>[{'STABLE' if vib<=7.0 else 'ANOMALY'}]</span>",
        showarrow=False, font=dict(color="#f8fafc", size=12)
    )

    # 2. Four Cylinders (Opposed Layout: Cyl 1 & 3 Left, Cyl 2 & 4 Right)
    cylinders = [
        {"name": "CYLINDER 1", "x0": -5.4, "y0": 0.4, "x1": -2.2, "y1": 1.6, "cx": -3.8, "cy": 1.0},
        {"name": "CYLINDER 3", "x0": -5.4, "y0": -1.6, "x1": -2.2, "y1": -0.4, "cx": -3.8, "cy": -1.0},
        {"name": "CYLINDER 2", "x0": 2.2, "y0": 0.4, "x1": 5.4, "y1": 1.6, "cx": 3.8, "cy": 1.0},
        {"name": "CYLINDER 4", "x0": 2.2, "y0": -1.6, "x1": 5.4, "y1": -0.4, "cx": 3.8, "cy": -1.0},
    ]

    for cyl in cylinders:
        fig.add_shape(
            type="rect", x0=cyl["x0"], y0=cyl["y0"], x1=cyl["x1"], y1=cyl["y1"],
            fillcolor="rgba(7, 18, 38, 0.95)", line=dict(color=temp_color, width=2.5)
        )
        fig.add_annotation(
            x=cyl["cx"], y=cyl["cy"],
            text=f"<b>{cyl['name']}</b><br>{temp_label}<br><span style='font-size:10px; color:{temp_color};'>[{'NOMINAL' if temp<=110 else 'OVERHEAT'}]</span>",
            showarrow=False, font=dict(color=temp_color, size=11)
        )

    # 3. Propeller Hub / Reduction Gearbox (Top)
    fig.add_shape(
        type="rect", x0=-1.4, y0=1.6, x1=1.4, y1=2.9,
        fillcolor="rgba(12, 74, 110, 0.8)", line=dict(color=rpm_color, width=2.5)
    )
    fig.add_annotation(
        x=0, y=2.25,
        text=f"<b>PROPELLER / GEARBOX</b><br>{rpm:.0f} RPM<br><span style='font-size:10px; color:{rpm_color};'>[{'SAFE' if rpm<=5000 else 'HIGH RPM'}]</span>",
        showarrow=False, font=dict(color="#e0f2fe", size=11)
    )

    # 4. Oil Sump & Lubrication Gallery (Bottom)
    fig.add_shape(
        type="rect", x0=-2.0, y0=-2.8, x1=2.0, y1=-1.6,
        fillcolor="rgba(2, 44, 34, 0.85)" if oil_press >= 30 else "rgba(69, 10, 10, 0.85)",
        line=dict(color=oil_color, width=2.5)
    )
    fig.add_annotation(
        x=0, y=-2.2,
        text=f"<b>OIL SUMP & GALLERY</b><br>{oil_press:.1f} PSI<br><span style='font-size:10px; color:{oil_color};'>[{'SUFFICIENT' if oil_press>=30 else 'LOW PRESSURE'}]</span>",
        showarrow=False, font=dict(color=oil_color, size=11)
    )

    # 5. Reference-Style CAD Callout Pins & Leader Nodes (Circular Pins)
    callout_pins = [
        {"cx": -3.8, "cy": 1.6, "tx": -3.8, "ty": 2.3},  # Cyl 1 node
        {"cx": 3.8, "cy": 1.6, "tx": 3.8, "ty": 2.3},    # Cyl 2 node
        {"cx": -1.8, "cy": 0.0, "tx": -2.7, "ty": 0.0},  # Crankcase node
        {"cx": 0.0, "cy": -1.6, "tx": 0.0, "ty": -1.2},  # Sump node
    ]
    for pin in callout_pins:
        # Leader line
        fig.add_shape(
            type="line", x0=pin["cx"], y0=pin["cy"], x1=pin["tx"], y1=pin["ty"],
            line=dict(color="rgba(56, 189, 248, 0.6)", width=1.5)
        )
        # Circular Node Ring
        fig.add_shape(
            type="circle", x0=pin["tx"]-0.14, y0=pin["ty"]-0.14, x1=pin["tx"]+0.14, y1=pin["ty"]+0.14,
            fillcolor="#ffffff", line=dict(color="#00f2fe", width=2)
        )

    fig.update_xaxes(showgrid=False, zeroline=False, showticklabels=False, range=[-6.5, 6.5])
    fig.update_yaxes(showgrid=False, zeroline=False, showticklabels=False, range=[-3.2, 3.4])
    fig.update_layout(
        height=390,
        margin=dict(l=10, r=10, t=15, b=10),
        plot_bgcolor="#040914",
        paper_bgcolor="#040914"
    )
    return fig


def create_aerospace_waveform_figure(history_df, vib, rpm):
    """
    Creates the dual oscillating waveform line graph matching the reference image bottom section.
    Electric cyan and ice blue traces over time on deep space dark navy background.
    """
    fig = go.Figure()
    
    # Trace 1: Primary Vibration Telemetry Signal (Cyan glow with soft area fill)
    fig.add_trace(go.Scatter(
        x=history_df["time_seconds"],
        y=history_df["vibration_level"],
        mode="lines",
        name="Vibration Waveform",
        line=dict(color="#00f2fe", width=2.8, shape="spline"),
        fill="tozeroy",
        fillcolor="rgba(0, 242, 254, 0.07)"
    ))

    # Trace 2: Secondary Dynamic Waveform / Normalized Harmonic (Ice blue)
    # Synthesized from engine RPM dynamics for realistic dual-curve telemetry
    n_pts = len(history_df)
    harmonic = (history_df["rpm"] / 5000.0) * 3.2 + np.sin(np.linspace(0, 4 * np.pi, n_pts)) * 0.75
    fig.add_trace(go.Scatter(
        x=history_df["time_seconds"],
        y=np.round(np.clip(harmonic, 0.5, 9.5), 2),
        mode="lines",
        name="Dynamic Harmonic",
        line=dict(color="#38bdf8", width=1.8, dash="dot", shape="spline")
    ))

    # Critical Vibration Threshold (7.0 limit)
    fig.add_shape(
        type="line",
        x0=float(history_df["time_seconds"].min()),
        y0=7.0,
        x1=float(history_df["time_seconds"].max()),
        y1=7.0,
        line=dict(color="rgba(239, 68, 68, 0.65)", width=1.5, dash="dash")
    )
    fig.add_annotation(
        x=float(history_df["time_seconds"].max()) - 3,
        y=7.4,
        text="VIB LIMIT (7.0)",
        showarrow=False,
        font=dict(color="#f87171", size=10, family="monospace")
    )

    fig.update_xaxes(
        title=dict(text="<b>TIME (s)</b>", font=dict(color="#94a3b8", size=11)),
        showgrid=True,
        gridcolor="rgba(56, 189, 248, 0.12)",
        zeroline=False,
        tickfont=dict(color="#cbd5e1", size=10)
    )
    fig.update_yaxes(
        title=dict(text="<b>AMPLITUDE</b>", font=dict(color="#94a3b8", size=11)),
        showgrid=True,
        gridcolor="rgba(56, 189, 248, 0.12)",
        zeroline=False,
        tickfont=dict(color="#cbd5e1", size=10),
        range=[0, 10.5]
    )
    fig.update_layout(
        height=220,
        margin=dict(l=40, r=20, t=25, b=25),
        plot_bgcolor="#040914",
        paper_bgcolor="#040914",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(color="#94a3b8", size=10)
        )
    )
    return fig


# ==============================================================================
# 7. HEADER & SIDEBAR NAVIGATION
# ==============================================================================
st.markdown("""
<div class="defence-header">
    <div style="display:flex; justify-content:space-between; align-items:center;">
        <div>
            <div class="defence-title">🛡️ AeroGuard AI</div>
            <div class="defence-subtitle">AI-Based Aero Engine Digital Twin</div>
        </div>
        <div style="text-align:right;">
            <span style="background-color:#0284c7; color:#f0f9ff; padding:6px 14px; border-radius:20px; font-size:12px; font-weight:700;">
                MALE UAV DEFENCE PROTOTYPE
            </span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Sidebar Navigation (Integrated Complete 11-Module Dashboard + About)
st.sidebar.markdown("## 🧭 Navigation")
nav_module = st.sidebar.radio(
    "Select Module:",
    [
        "1. Home Dashboard",
        "2. Virtual Engine Monitoring",
        "3. Sensor Monitoring",
        "4. Fault Detection",
        "5. Engine Health Score",
        "6. Fault Injection Panel",
        "7. Mission Reliability Score",
        "8. Explainable Alerts with Suggestions",
        "9. Historical Sensor Analysis",
        "10. Maintenance Recommendations",
        "11. Reports and CSV Download",
        "12. About the Project"
    ]
)

st.sidebar.markdown("---")
st.sidebar.markdown("## 🎛️ Sensor Input Controls")

input_mode = st.sidebar.radio(
    "Choose Input Method:",
    ["Predefined Scenarios", "Manual Input"]
)

if input_mode == "Predefined Scenarios":
    scenario_choice = st.sidebar.selectbox(
        "Select Scenario Preset:",
        ["Healthy", "Warning", "Critical"]
    )
    if st.session_state["active_fault"] is not None:
        st.sidebar.warning(f"⚠️ Fault Injection Active: **{st.session_state['active_fault']}**\n(Switching presets or resetting in Module 6 overrides this)")
        sensor_temp = st.session_state["injected_params"]["temp"]
        sensor_oil = st.session_state["injected_params"]["oil"]
        sensor_vib = st.session_state["injected_params"]["vib"]
        sensor_rpm = st.session_state["injected_params"]["rpm"]
        active_sensor_failure = st.session_state["injected_params"]["sensor_failure"]
    else:
        if scenario_choice == "Healthy":
            sensor_temp, sensor_oil, sensor_vib, sensor_rpm = 85.0, 65.0, 3.0, 3000.0
        elif scenario_choice == "Warning":
            sensor_temp, sensor_oil, sensor_vib, sensor_rpm = 115.0, 65.0, 3.0, 3000.0
        else:  # Critical
            sensor_temp, sensor_oil, sensor_vib, sensor_rpm = 130.0, 20.0, 9.0, 5200.0
        active_sensor_failure = None
        st.sidebar.success(f"Loaded **{scenario_choice}** Scenario:\n- Temp: {sensor_temp}°C\n- Oil: {sensor_oil} PSI\n- Vib: {sensor_vib}\n- RPM: {sensor_rpm:.0f}")

else:  # Manual Input
    st.sidebar.caption("Adjust sliders independently:")
    default_t = 85.0 if st.session_state["injected_params"]["temp"] < 0 else st.session_state["injected_params"]["temp"]
    default_o = st.session_state["injected_params"]["oil"]
    default_v = st.session_state["injected_params"]["vib"]
    default_r = st.session_state["injected_params"]["rpm"]

    sensor_temp = st.sidebar.slider("Engine Temperature (°C):", 40.0, 150.0, float(default_t), 1.0)
    sensor_oil = st.sidebar.slider("Oil Pressure (PSI):", 0.0, 100.0, float(default_o), 1.0)
    sensor_vib = st.sidebar.slider("Engine Vibration (0-10):", 0.0, 10.0, float(default_v), 0.1)
    sensor_rpm = st.sidebar.slider("Engine RPM:", 0.0, 6000.0, float(default_r), 50.0)
    active_sensor_failure = st.session_state["injected_params"].get("sensor_failure", None)

# Run Rule-Based Evaluation on Current Readings (Integrated with Feature 3: Explainable Alerts)
evaluation = analyze_engine_state(
    sensor_temp, sensor_oil, sensor_vib, sensor_rpm,
    sensor_failure=active_sensor_failure,
    active_fault_name=st.session_state.get("active_fault", None)
)

# Run Feature 2: Mission Reliability Calculation
mission_rel = compute_mission_reliability(sensor_temp, sensor_oil, sensor_vib, sensor_rpm, evaluation["fault_details"], sensor_failure=active_sensor_failure)

history_df = generate_sensor_history(sensor_temp, sensor_oil, sensor_vib, sensor_rpm)


# ==============================================================================
# TOP STATUS & SENSOR METRIC CARDS (PERSISTENT ACROSS MODULES 2-12)
# ==============================================================================
if nav_module != "1. Home Dashboard":
    st.markdown(f"""
    <div class="status-banner">
        <div>
            <span style="color:#94a3b8; font-size:12px; text-transform:uppercase; font-weight:700;">Simulated Mission Reliability:</span><br>
            <div class="{mission_rel['badge_class']}" style="margin-top:6px;">
                {mission_rel['condition_label']} &nbsp;•&nbsp; RELIABILITY: {mission_rel['reliability_score']}%
            </div>
        </div>
        <div style="text-align:right;">
            <span style="color:#94a3b8; font-size:12px; text-transform:uppercase; font-weight:700;">Engine Health Score:</span><br>
            <span style="color:#38bdf8; font-size:18px; font-weight:700;">{evaluation['health_score']} / 100 pts ({evaluation['status']})</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 4 Main Sensor Metric Cards
    mc1, mc2, mc3, mc4 = st.columns(4)

    with mc1:
        if active_sensor_failure and "Temperature" in active_sensor_failure:
            st.markdown("""
            <div class="sensor-card">
                <div class="sensor-label">🔥 Engine Temperature</div>
                <div class="sensor-val" style="color:#fbbf24; font-size:20px;">ERR_OOR</div>
                <span class="tag-critical">SENSOR FAILURE</span>
            </div>
            """, unsafe_allow_html=True)
        else:
            t_tag = "tag-warning" if sensor_temp > 110 else "tag-healthy"
            t_status = "WARNING" if sensor_temp > 110 else "HEALTHY"
            st.markdown(f"""
            <div class="sensor-card">
                <div class="sensor-label">🔥 Engine Temperature</div>
                <div class="sensor-val">{sensor_temp:.1f} <span style="font-size:16px; color:#94a3b8;">°C</span></div>
                <span class="{t_tag}">{t_status} (Limit: 110°C)</span>
            </div>
            """, unsafe_allow_html=True)

    with mc2:
        o_tag = "tag-warning" if sensor_oil < 30 else "tag-healthy"
        o_status = "WARNING" if sensor_oil < 30 else "HEALTHY"
        st.markdown(f"""
        <div class="sensor-card">
            <div class="sensor-label">🛢️ Oil Pressure</div>
            <div class="sensor-val">{sensor_oil:.1f} <span style="font-size:16px; color:#94a3b8;">PSI</span></div>
            <span class="{o_tag}">{o_status} (Limit: 30 PSI)</span>
        </div>
        """, unsafe_allow_html=True)

    with mc3:
        v_tag = "tag-warning" if sensor_vib > 7.0 else "tag-healthy"
        v_status = "WARNING" if sensor_vib > 7.0 else "HEALTHY"
        st.markdown(f"""
        <div class="sensor-card">
            <div class="sensor-label">📳 Engine Vibration</div>
            <div class="sensor-val">{sensor_vib:.1f} <span style="font-size:16px; color:#94a3b8;">/ 10</span></div>
            <span class="{v_tag}">{v_status} (Limit: 7.0)</span>
        </div>
        """, unsafe_allow_html=True)

    with mc4:
        r_tag = "tag-warning" if sensor_rpm > 5000 else "tag-healthy"
        r_status = "WARNING" if sensor_rpm > 5000 else "HEALTHY"
        st.markdown(f"""
        <div class="sensor-card">
            <div class="sensor-label">⚡ Engine RPM</div>
            <div class="sensor-val">{sensor_rpm:.0f} <span style="font-size:16px; color:#94a3b8;">RPM</span></div>
            <span class="{r_tag}">{r_status} (Limit: 5000 RPM)</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:16px;'></div>", unsafe_allow_html=True)


# ==============================================================================
# MODULE 1: HOME DASHBOARD (REFERENCE IMAGE AEROSPACE LAYOUT)
# ==============================================================================
if nav_module == "1. Home Dashboard":
    # 1. Top Aerospace Digital Twin Header Bar (Matching Reference Image)
    has_anomaly = len(evaluation["explainable_alerts"]) > 0 or (active_sensor_failure is not None)
    alert_box_border = "rgba(239, 68, 68, 0.6)" if has_anomaly else "rgba(56, 189, 248, 0.4)"
    alert_box_glow = "0 0 16px rgba(239, 68, 68, 0.3)" if has_anomaly else "0 0 16px rgba(56, 189, 248, 0.15)"
    alert_icon = "⚠️" if has_anomaly else "▲"
    alert_icon_color = "#f87171" if has_anomaly else "#38bdf8"
    alert_status_text = "Anomaly detected" if has_anomaly else "All Systems Nominal"
    alert_status_color = "#fca5a5" if has_anomaly else "#6ee7b7"

    st.markdown(f"""
    <div class="dt-topbar">
        <div class="dt-brand">
            <span class="dt-title">DIGITAL TWIN</span>
            <span class="dt-subtitle">AERO PISTON ENGINE</span>
        </div>
        <div class="dt-kpi-group">
            <div class="dt-kpi">
                <div class="dt-kpi-label">HEALTH SCORE</div>
                <div class="dt-kpi-val">{evaluation['health_score']}<span class="dt-kpi-unit">PTS</span></div>
            </div>
            <div class="dt-kpi">
                <div class="dt-kpi-label">RELIABILITY</div>
                <div class="dt-kpi-val">{mission_rel['reliability_score']}<span class="dt-kpi-unit">%</span></div>
            </div>
            <div class="dt-kpi">
                <div class="dt-kpi-label">ENGINE SPEED</div>
                <div class="dt-kpi-val">{sensor_rpm:,.0f}<span class="dt-kpi-unit">RPM</span></div>
            </div>
        </div>
        <div class="dt-alert-box" style="border-color:{alert_box_border}; box-shadow:{alert_box_glow};">
            <span class="dt-alert-icon" style="color:{alert_icon_color};">{alert_icon}</span>
            <div class="dt-alert-texts">
                <span class="dt-alert-header">PREDICTIVE MAINTENANCE</span>
                <span class="dt-alert-status" style="color:{alert_status_color};">{alert_status_text}</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 2. Main Middle Section: 3-Column Layout (Left Gauges, Center Engine, Right Alerts & Parameters)
    col_left, col_center, col_right = st.columns([1.1, 2.3, 1.4])

    # LEFT COLUMN: Attractive Sensor Gauges (T1 Temp, P1 Oil, V1 Vibration)
    with col_left:
        # Gauge 1: T1 Temperature
        if active_sensor_failure and "Temperature" in active_sensor_failure:
            t1_val_str = "ERR_OOR"
            t1_pct = 95
            t1_grad = "linear-gradient(180deg, #f59e0b 0%, #b45309 100%)"
            t1_stroke = "#f59e0b"
            t1_offset = 15
        else:
            t1_val_str = f"{sensor_temp:.0f} °C"
            t1_pct = int(max(10, min(100, ((sensor_temp - 40.0) / 110.0) * 100)))
            if sensor_temp > 110:
                t1_grad = "linear-gradient(180deg, #ef4444 0%, #b91c1c 100%)"
                t1_stroke = "#ef4444"
            else:
                t1_grad = "linear-gradient(180deg, #00f2fe 0%, #0284c7 100%)"
                t1_stroke = "#00f2fe"
            t1_offset = int(134 * (1 - min(1.0, sensor_temp / 150.0)))

        st.markdown(f"""
        <div class="gauge-widget">
            <div class="gauge-header-row">
                <span class="gauge-code">T1</span>
                <span class="gauge-val">{t1_val_str}</span>
            </div>
            <div class="gauge-body-row">
                <div class="capsule-track">
                    <div class="capsule-fill" style="height:{t1_pct}%; background:{t1_grad};"></div>
                </div>
                <div class="dial-container">
                    <svg width="72" height="72" viewBox="0 0 100 100">
                        <circle cx="50" cy="50" r="34" fill="none" stroke="#0a1932" stroke-width="7" stroke-dasharray="160" stroke-dashoffset="-20" stroke-linecap="round"/>
                        <circle cx="50" cy="50" r="34" fill="none" stroke="{t1_stroke}" stroke-width="7" stroke-dasharray="160" stroke-dashoffset="{t1_offset}" stroke-linecap="round"/>
                        <text x="50" y="55" text-anchor="middle" fill="#94a3b8" font-size="11" font-family="-apple-system, sans-serif" font-weight="700">110°C</text>
                    </svg>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Gauge 2: P1 Oil Pressure
        p1_val_str = f"{sensor_oil:.1f} PSI"
        p1_pct = int(max(10, min(100, (sensor_oil / 100.0) * 100)))
        if sensor_oil < 30:
            p1_grad = "linear-gradient(180deg, #ef4444 0%, #b91c1c 100%)"
            p1_stroke = "#ef4444"
        else:
            p1_grad = "linear-gradient(180deg, #38bdf8 0%, #0369a1 100%)"
            p1_stroke = "#38bdf8"
        p1_offset = int(134 * (1 - min(1.0, sensor_oil / 100.0)))

        st.markdown(f"""
        <div class="gauge-widget">
            <div class="gauge-header-row">
                <span class="gauge-code">P1</span>
                <span class="gauge-val">{p1_val_str}</span>
            </div>
            <div class="gauge-body-row">
                <div class="capsule-track">
                    <div class="capsule-fill" style="height:{p1_pct}%; background:{p1_grad};"></div>
                </div>
                <div class="dial-container">
                    <svg width="72" height="72" viewBox="0 0 100 100">
                        <circle cx="50" cy="50" r="34" fill="none" stroke="#0a1932" stroke-width="7" stroke-dasharray="160" stroke-dashoffset="-20" stroke-linecap="round"/>
                        <circle cx="50" cy="50" r="34" fill="none" stroke="{p1_stroke}" stroke-width="7" stroke-dasharray="160" stroke-dashoffset="{p1_offset}" stroke-linecap="round"/>
                        <text x="50" y="55" text-anchor="middle" fill="#94a3b8" font-size="11" font-family="-apple-system, sans-serif" font-weight="700">30 PSI</text>
                    </svg>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Gauge 3: V1 Engine Vibration
        v1_val_str = f"{sensor_vib:.1f} / 10"
        v1_pct = int(max(10, min(100, (sensor_vib / 10.0) * 100)))
        if sensor_vib > 7.0:
            v1_grad = "linear-gradient(180deg, #ef4444 0%, #b91c1c 100%)"
            v1_stroke = "#ef4444"
        else:
            v1_grad = "linear-gradient(180deg, #00f2fe 0%, #0891b2 100%)"
            v1_stroke = "#00f2fe"
        v1_offset = int(134 * (1 - min(1.0, sensor_vib / 10.0)))

        st.markdown(f"""
        <div class="gauge-widget">
            <div class="gauge-header-row">
                <span class="gauge-code">V1</span>
                <span class="gauge-val">{v1_val_str}</span>
            </div>
            <div class="gauge-body-row">
                <div class="capsule-track">
                    <div class="capsule-fill" style="height:{v1_pct}%; background:{v1_grad};"></div>
                </div>
                <div class="dial-container">
                    <svg width="72" height="72" viewBox="0 0 100 100">
                        <circle cx="50" cy="50" r="34" fill="none" stroke="#0a1932" stroke-width="7" stroke-dasharray="160" stroke-dashoffset="-20" stroke-linecap="round"/>
                        <circle cx="50" cy="50" r="34" fill="none" stroke="{v1_stroke}" stroke-width="7" stroke-dasharray="160" stroke-dashoffset="{v1_offset}" stroke-linecap="round"/>
                        <text x="50" y="55" text-anchor="middle" fill="#94a3b8" font-size="11" font-family="-apple-system, sans-serif" font-weight="700">7.0 VIB</text>
                    </svg>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # CENTER COLUMN: Prominent Virtual Engine Twin CAD Schematic Matrix
    with col_center:
        fig_engine = create_virtual_engine_figure(sensor_temp, sensor_oil, sensor_vib, sensor_rpm, evaluation['status'], active_sensor_failure)
        st.plotly_chart(fig_engine, use_container_width=True)

    # RIGHT COLUMN: Predictive Maintenance Alerts & Parameters
    with col_right:
        # 1. PARAMETERS Panel (Matching Reference Image)
        temp_param_disp = "ERR_OOR" if (active_sensor_failure and "Temperature" in active_sensor_failure) else f"{sensor_temp:.1f} °C"
        st.markdown(f"""
        <div class="parameters-box">
            <div class="param-title">PARAMETERS</div>
            <div class="param-item">
                <span class="param-label">SPEED</span>
                <span class="param-number">{sensor_rpm:,.0f} <span class="param-unit-tag">RPM</span></span>
            </div>
            <div class="param-item">
                <span class="param-label">PRESSURE</span>
                <span class="param-number">{sensor_oil:.1f} <span class="param-unit-tag">PSI</span></span>
            </div>
            <div class="param-item">
                <span class="param-label">TEMPERATURE</span>
                <span class="param-number">{temp_param_disp}</span>
            </div>
            <div class="param-item">
                <span class="param-label">VIBRATION</span>
                <span class="param-number">{sensor_vib:.1f} <span class="param-unit-tag">/ 10</span></span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # 2. Predictive Maintenance Alerts / Suggestions
        if len(evaluation["explainable_alerts"]) == 0:
            st.markdown("""
            <div class="card-box" style="border-left: 4px solid #10b981;">
                <div style="font-size:12px; font-weight:800; color:#34d399; letter-spacing:1px; margin-bottom:4px;">STATUS: OPTIMAL</div>
                <div style="font-size:13px; color:#cbd5e1;">All propulsion telemetry operating within nominal design limits. Routine pre-flight status confirmed.</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            if evaluation["highest_priority_fault"]:
                hp = evaluation["highest_priority_fault"]
                st.markdown(f"""
                <div class="card-box" style="border-left: 4px solid #ef4444; background:rgba(30, 10, 15, 0.85);">
                    <div style="font-size:11px; font-weight:800; color:#f87171; letter-spacing:1px; text-transform:uppercase;">{hp['severity']}: {hp['alert_title']}</div>
                    <div style="font-size:13px; font-weight:700; color:#ffffff; margin:4px 0;">{hp['parameter']}: {hp['reading']} <span style="font-size:11px; color:#94a3b8;">(Limit: {hp['threshold']})</span></div>
                    <div style="font-size:12px; color:#cbd5e1; margin-bottom:6px;"><b>Reason:</b> {hp['reason']}</div>
                    <div style="font-size:12px; color:#38bdf8;"><b>Action:</b> {hp['suggestion']}</div>
                </div>
                """, unsafe_allow_html=True)

        # 3. Mission Reliability Insight
        st.markdown(f"""
        <div class="card-box" style="padding:12px 16px; margin-bottom:0;">
            <div style="font-size:11px; font-weight:700; letter-spacing:1px; color:#94a3b8; text-transform:uppercase; margin-bottom:4px;">RELIABILITY INSIGHT</div>
            <div style="font-size:12px; color:#cbd5e1; line-height:1.4;">{mission_rel['explanation']}</div>
        </div>
        """, unsafe_allow_html=True)

    # 3. Bottom Full-Width Section: Historical Vibration & Telemetry Waveforms (Matching Reference Image)
    st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px; padding:0 4px;">
        <span style="font-size:13px; font-weight:800; letter-spacing:2px; color:#ffffff; text-transform:uppercase;">VIBRATION & TELEMETRY WAVEFORMS</span>
        <span style="font-size:11px; font-weight:600; color:#38bdf8;">REAL-TIME DUAL-HARMONIC TELEMETRY</span>
    </div>
    """, unsafe_allow_html=True)

    fig_waveform = create_aerospace_waveform_figure(history_df, sensor_vib, sensor_rpm)
    st.plotly_chart(fig_waveform, use_container_width=True)


# ==============================================================================
# MODULE 2: VIRTUAL ENGINE MONITORING
# ==============================================================================
elif nav_module == "2. Virtual Engine Monitoring":
    st.subheader("⚙️ Virtual Engine Monitoring: Digital Twin Schematic")
    st.write(
        "A virtual visual representation of the 4-cylinder aero piston propulsion system. "
        "Component blocks update dynamically in real time based on sensor readings."
    )

    col_diag, col_specs = st.columns([1.5, 1])

    with col_diag:
        fig_engine = create_virtual_engine_figure(sensor_temp, sensor_oil, sensor_vib, sensor_rpm, evaluation['status'], active_sensor_failure)
        st.plotly_chart(fig_engine, use_container_width=True)

    with col_specs:
        st.markdown("#### 📐 Component Status Matrix")
        temp_disp_status = '🔴 SENSOR FAILURE' if (active_sensor_failure and 'Temperature' in active_sensor_failure) else ('🟢 Normal' if sensor_temp <= 110 else '🔴 High Temp (>110°C)')
        temp_val_str = 'INVALID' if (active_sensor_failure and 'Temperature' in active_sensor_failure) else f'{sensor_temp:.1f}°C'
        st.markdown(f"""
        - **Cylinders (1, 2, 3, 4):** `{temp_val_str}` &nbsp;→&nbsp; **{temp_disp_status}**
        - **Oil Sump & Gallery:** `{sensor_oil:.1f} PSI` &nbsp;→&nbsp; **{'🟢 Sufficient' if sensor_oil >= 30 else '🔴 Low Pressure (<30 PSI)'}**
        - **Engine Crankcase Mounts:** `{sensor_vib:.1f} / 10` &nbsp;→&nbsp; **{'🟢 Stable' if sensor_vib <= 7.0 else '🔴 High Vibration (>7.0)'}**
        - **Propeller Hub / Gearbox:** `{sensor_rpm:.0f} RPM` &nbsp;→&nbsp; **{'🟢 Safe Envelope' if sensor_rpm <= 5000 else '🔴 High RPM (>5000 RPM)'}**
        """)


# ==============================================================================
# MODULE 3: SENSOR MONITORING
# ==============================================================================
elif nav_module == "3. Sensor Monitoring":
    st.subheader("🎛️ Sensor Monitoring: Dual Input Interface")
    st.write(
        "Monitor live readings through **Predefined Scenarios** or **Manual Input** "
        "to test any operational condition."
    )

    col_mode_info, col_gauges = st.columns([1, 1.2])

    with col_mode_info:
        st.markdown(f"### Active Mode: **{input_mode}**")
        st.markdown("""
        **Predefined Scenario Presets:**
        - **🟢 Healthy:** Temp = 85°C, Oil Pressure = 65 PSI, Vibration = 3.0, RPM = 3000
        - **🟡 Warning:** Temp = 115°C, Oil Pressure = 65 PSI, Vibration = 3.0, RPM = 3000
        - **🔴 Critical:** Temp = 130°C, Oil Pressure = 20 PSI, Vibration = 9.0, RPM = 5200
        
        **Manual Input:**
        - Adjust all four sliders independently in the sidebar to simulate custom edge cases.
        """)
        st.info("👉 Use the **Sidebar** to switch presets or adjust sliders at any time.")

    with col_gauges:
        st.markdown("### 🎯 Live Sensor Gauge Level")
        effective_gauge_t = 0 if sensor_temp < 0 else sensor_temp
        fig_g1 = go.Figure(go.Indicator(
            mode="gauge+number",
            value=effective_gauge_t,
            title={'text': "Temperature (°C) [Threshold: 110°C]"},
            gauge={
                'axis': {'range': [40, 150]},
                'bar': {'color': "#38bdf8"},
                'steps': [
                    {'range': [40, 110], 'color': "rgba(16, 185, 129, 0.3)"},
                    {'range': [110, 150], 'color': "rgba(239, 68, 68, 0.4)"}
                ],
                'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 110}
            }
        ))
        fig_g1.update_layout(height=220, margin=dict(l=20, r=20, t=30, b=10), paper_bgcolor="#0b1120", font=dict(color="#f8fafc"))
        st.plotly_chart(fig_g1, use_container_width=True)


# ==============================================================================
# MODULE 4: FAULT DETECTION
# ==============================================================================
elif nav_module == "4. Fault Detection":
    st.subheader("🔍 Fault Detection and Engine Health Analysis")
    st.write(
        "AeroGuard AI uses a transparent, rule-based anomaly detection engine. "
        "Whenever a sensor crosses an established demonstration threshold, a clear warning is triggered, "
        "the abnormal parameter is highlighted, and a possible maintenance recommendation is provided."
    )

    st.markdown("### 🚨 Detected Conditions & Parameter Explanations")
    
    if len(evaluation["fault_details"]) == 0:
        st.success("✅ **ALL PARAMETERS NORMAL:** No abnormal operating conditions detected. Telemetry is within safe demonstration bounds.")
    else:
        for idx, item in enumerate(evaluation["fault_details"], 1):
            with st.container():
                st.markdown(f"""
                <div class="card-box" style="border-left: 4px solid #f59e0b;">
                    <h4 style="margin:0; color:#fbbf24;">Condition {idx}: {item['warning']}</h4>
                    <p style="margin:6px 0 0 0; color:#e2e8f0;"><b>Abnormal Parameter:</b> <code>{item['param']}</code> = <b>{item['val']}</b> (Threshold: {item['thresh']})</p>
                    <p style="margin:4px 0 0 0; color:#94a3b8;"><b>Physical Explanation:</b> {item['explanation']}</p>
                    <p style="margin:6px 0 0 0; color:#38bdf8;">🔧 <b>Possible Inspection Action:</b> {item['recommendation']}</p>
                </div>
                """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 📋 Rule-Based Threshold Reference")
    st.markdown("""
    | # | Monitored Parameter | Demonstration Threshold | Triggered Condition | Point Deduction |
    | :---: | :--- | :--- | :--- | :---: |
    | 1 | **Engine Temperature** | `> 110 °C` | High temperature detected | **-25 pts** |
    | 2 | **Oil Pressure** | `< 30 PSI` | Low oil pressure detected | **-25 pts** |
    | 3 | **Engine Vibration** | `> 7.0` | Abnormal vibration detected | **-25 pts** |
    | 4 | **Engine RPM** | `> 5000 RPM` | High RPM detected | **-15 pts** |
    """)


# ==============================================================================
# MODULE 5: ENGINE HEALTH SCORE
# ==============================================================================
elif nav_module == "5. Engine Health Score":
    st.subheader("📊 Engine Health Score Analysis")
    st.write(
        "The illustrative engine health score starts at **100 points**. Specific points are deducted for each "
        "abnormal operating condition. The score is not allowed to drop below zero."
    )

    col_score_viz, col_score_math = st.columns([1, 1.2])

    with col_score_viz:
        st.markdown("#### Health Score Progress & Gauge")
        
        fig_score = go.Figure(go.Indicator(
            mode="gauge+number",
            value=evaluation["health_score"],
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "#10b981" if evaluation["health_score"] >= 75 else ("#f59e0b" if evaluation["health_score"] >= 40 else "#ef4444")},
                'steps': [
                    {'range': [0, 40], 'color': "rgba(239, 68, 68, 0.3)"},
                    {'range': [40, 75], 'color': "rgba(245, 158, 11, 0.3)"},
                    {'range': [75, 100], 'color': "rgba(16, 185, 129, 0.3)"}
                ]
            }
        ))
        fig_score.update_layout(height=260, margin=dict(l=20, r=20, t=20, b=10), paper_bgcolor="#0b1120", font=dict(color="#f8fafc"))
        st.plotly_chart(fig_score, use_container_width=True)

        st.write(f"**Health Index: {evaluation['health_score']} / 100 points**")
        st.progress(evaluation["health_score"] / 100.0)

    with col_score_math:
        st.markdown("#### 🧮 Points Deduction Breakdown")
        st.write("Base Score: **100 Points**")
        
        if len(evaluation["deductions"]) == 0:
            st.success("✅ No deductions! All parameters operating within normal ranges. (Total Score = 100)")
        else:
            for item in evaluation["deductions"]:
                st.error(f"❌ **{item['param']}** ({item['condition']}): **{item['pts']} points**")
            
            total_deductions = sum(abs(item['pts']) for item in evaluation["deductions"])
            st.markdown(f"**Total Deductions:** `-{total_deductions} points`")
            st.markdown(f"**Final Score:** `max(0, 100 - {total_deductions})` = **`{evaluation['health_score']}`**")

        st.markdown("---")
        st.markdown("#### 🏷️ Health Status Brackets:")
        st.markdown(f"""
        - **75 – 100 Points:** `HEALTHY` {'👈 **(CURRENT)**' if evaluation['status'] == 'HEALTHY' else ''}
        - **40 – 74 Points:** `WARNING` {'👈 **(CURRENT)**' if evaluation['status'] == 'WARNING' else ''}
        - **Below 40 Points:** `CRITICAL` {'👈 **(CURRENT)**' if evaluation['status'] == 'CRITICAL' else ''}
        """)


# ==============================================================================
# MODULE 6: FAULT INJECTION PANEL
# ==============================================================================
elif nav_module == "6. Fault Injection Panel":
    st.subheader("⚡ Fault Injection Panel (Simulation & Stress Testing)")
    
    st.markdown("""
    <div class="injection-box">
        <h3 style="margin:0 0 8px 0; color:#38bdf8;">🎯 Aero Engine Fault Injection Rig</h3>
        <p style="margin:0; color:#cbd5e1; font-size:14px;">
            Simulate specific aero piston engine mechanical, thermal, and sensor failure modes to evaluate real-time Digital Twin detection latency,
            subsystem alerts, and health degradation. <i>(All telemetry is generated via in-memory simulation).</i>
        </p>
    </div>
    """, unsafe_allow_html=True)

    col_inj_ctrl, col_inj_stat = st.columns([1, 1.2])

    with col_inj_ctrl:
        st.markdown("### 🎛️ Fault Injection Controls")
        
        selected_fault = st.selectbox(
            "Inject Fault:",
            [
                "1. Spark Plug Misfire",
                "2. Oil Pressure Drop",
                "3. Engine Overheating",
                "4. Abnormal Engine Vibration",
                "5. High RPM",
                "6. Sensor Failure"
            ]
        )

        fault_descriptions = {
            "1. Spark Plug Misfire": "Simulates unbalanced combustion stroke induced by ignition failure, creating high vibration (8.4/10) and engine RPM shudder.",
            "2. Oil Pressure Drop": "Simulates a cracked oil scavenge line or oil pump relief valve failure, dropping pressure to 18.0 PSI (below 30 PSI threshold).",
            "3. Engine Overheating": "Simulates radiator airflow duct obstruction or coolant loss, pushing Cylinder Head Temperature to 128.0°C (above 110°C threshold).",
            "4. Abnormal Engine Vibration": "Simulates severe mechanical propeller unbalance or loose engine shock mounts, spiking vibration to 8.8 / 10.",
            "5. High RPM": "Simulates propeller governor failure or throttle linkage disconnect, pushing engine speed to 5400 RPM (above 5000 RPM threshold).",
            "6. Sensor Failure": "Simulates telemetry transducer disconnect / open circuit on the CHT sensor, outputting an invalid data stream."
        }

        st.caption(f"ℹ️ **Mechanism:** {fault_descriptions[selected_fault]}")

        col_b1, col_b2 = st.columns(2)
        with col_b1:
            start_btn = st.button("⚡ Start Fault Simulation", use_container_width=True, type="primary")
        with col_b2:
            reset_btn = st.button("🔄 Reset Fault", use_container_width=True)

        if start_btn:
            t0 = time.perf_counter()

            if "Spark Plug Misfire" in selected_fault:
                st.session_state["injected_params"] = {
                    "temp": 89.0, "oil": 62.0, "vib": 8.4, "rpm": 2850.0, "sensor_failure": None
                }
                affected = "Engine Vibration & RPM (Combustion Misfire)"
                fault_key = "Spark Plug Misfire"
            elif "Oil Pressure Drop" in selected_fault:
                st.session_state["injected_params"] = {
                    "temp": 92.0, "oil": 18.0, "vib": 3.4, "rpm": 3000.0, "sensor_failure": None
                }
                affected = "Oil Pressure (PSI)"
                fault_key = "Oil Pressure Drop"
            elif "Engine Overheating" in selected_fault:
                st.session_state["injected_params"] = {
                    "temp": 128.0, "oil": 60.0, "vib": 3.2, "rpm": 3100.0, "sensor_failure": None
                }
                affected = "Engine Temperature (°C)"
                fault_key = "Engine Overheating"
            elif "Abnormal Engine Vibration" in selected_fault:
                st.session_state["injected_params"] = {
                    "temp": 87.0, "oil": 64.0, "vib": 8.8, "rpm": 3050.0, "sensor_failure": None
                }
                affected = "Engine Vibration (0-10 Scale)"
                fault_key = "Abnormal Engine Vibration"
            elif "High RPM" in selected_fault:
                st.session_state["injected_params"] = {
                    "temp": 98.0, "oil": 58.0, "vib": 4.5, "rpm": 5400.0, "sensor_failure": None
                }
                affected = "Engine RPM (Powertrain Speed)"
                fault_key = "High RPM"
            else:  # Sensor Failure
                st.session_state["injected_params"] = {
                    "temp": -999.0, "oil": 65.0, "vib": 3.0, "rpm": 3000.0,
                    "sensor_failure": "Engine Temperature Sensor (CHT Probe)"
                }
                affected = "Engine Temperature Sensor (Signal Loss / Disconnect)"
                fault_key = "Sensor Failure"

            diag_run = analyze_engine_state(
                st.session_state["injected_params"]["temp"],
                st.session_state["injected_params"]["oil"],
                st.session_state["injected_params"]["vib"],
                st.session_state["injected_params"]["rpm"],
                sensor_failure=st.session_state["injected_params"]["sensor_failure"]
            )
            t1 = time.perf_counter()
            actual_latency_ms = (t1 - t0) * 1000.0

            st.session_state["active_fault"] = fault_key
            st.session_state["affected_param"] = affected
            st.session_state["detection_time_ms"] = round(actual_latency_ms, 3)
            st.session_state["fault_timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            st.rerun()

        if reset_btn:
            st.session_state["active_fault"] = None
            st.session_state["injected_params"] = {
                "temp": 85.0, "oil": 65.0, "vib": 3.0, "rpm": 3000.0, "sensor_failure": None
            }
            st.session_state["detection_time_ms"] = None
            st.session_state["affected_param"] = None
            st.session_state["fault_timestamp"] = None
            st.success("✅ Fault simulation reset to nominal engine state.")
            st.rerun()

    with col_inj_stat:
        st.markdown("### 📊 Fault Detection & Diagnosis Results")
        
        if st.session_state["active_fault"] is not None:
            st.markdown(f"""
            <div class="card-box" style="border-left: 4px solid #ef4444;">
                <h4 style="margin:0; color:#f87171;">🚨 FAULT INJECTION ACTIVE: {st.session_state['active_fault']}</h4>
                <p style="margin:6px 0 0 0;"><b>Affected Engine Parameter:</b> <code>{st.session_state['affected_param']}</code></p>
                <p style="margin:4px 0 0 0;"><b>Actual Measured Detection Latency:</b> <span style="color:#38bdf8; font-weight:700;">{st.session_state['detection_time_ms']} ms</span></p>
                <p style="margin:4px 0 0 0;"><b>Injection Timestamp:</b> <code>{st.session_state['fault_timestamp']}</code></p>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("##### 🔍 Detected Condition & Explainable Alerts (Feature 3):")
            for alert in evaluation["explainable_alerts"]:
                st.error(f"**{alert['alert_title']}** (Severity: {alert['severity']}) | Parameter: `{alert['parameter']}` ({alert['reading']})")
                st.write(f"• **Reason:** {alert['reason']}")
                st.info(f"🔧 **Maintenance Action:** {alert['suggestion']}")
                with st.expander(f"Why was this {alert['alert_title']} generated?"):
                    st.caption(f"{alert['why_generated']}")

            st.metric(
                label="Updated Engine Health Score",
                value=f"{evaluation['health_score']} / 100",
                delta=f"-{100 - evaluation['health_score']} pts ({evaluation['status']})",
                delta_color="inverse"
            )
        else:
            st.info("💡 No fault currently injected. Select an engine fault from the dropdown on the left and click **'Start Fault Simulation'**.")


# ==============================================================================
# MODULE 7: MISSION RELIABILITY SCORE
# ==============================================================================
elif nav_module == "7. Mission Reliability Score":
    st.subheader("🎯 Mission Reliability Score Engine")

    col_g_view, col_f_view = st.columns([1, 1.2])

    with col_g_view:
        st.markdown("### 🧭 Mission Reliability Index")
        
        # Required Circular Gauge (0 to 100%)
        fig_rel_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=mission_rel["reliability_score"],
            number={'suffix': "%"},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': mission_rel["condition_color"]},
                'steps': [
                    {'range': [0, 40], 'color': "rgba(239, 68, 68, 0.25)"},
                    {'range': [40, 75], 'color': "rgba(245, 158, 11, 0.25)"},
                    {'range': [75, 100], 'color': "rgba(16, 185, 129, 0.25)"}
                ],
                'threshold': {
                    'line': {'color': mission_rel["condition_color"], 'width': 4},
                    'thickness': 0.8,
                    'value': mission_rel["reliability_score"]
                }
            }
        ))
        fig_rel_gauge.update_layout(
            height=280,
            margin=dict(l=20, r=20, t=30, b=20),
            paper_bgcolor="#0b1120",
            font=dict(color="#f8fafc")
        )
        st.plotly_chart(fig_rel_gauge, use_container_width=True)

        # Condition Badge Display
        st.markdown(f"""
        <div style="text-align:center; margin-top:-10px;">
            <div class="{mission_rel['badge_class']}">
                CONDITION: {mission_rel['condition_label']}
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_f_view:
        st.markdown("### 📊 Dynamic Reliability Factor Breakdown")
        st.write(
            "Unlike discrete step deductions, the Mission Reliability Score dynamically evaluates continuous "
            "endurance risk across 4 key engine parameters and active fault severity:"
        )

        for factor, score_val in mission_rel["sub_factors"].items():
            st.markdown(f"**{factor}:** `{score_val}%`")
            st.progress(score_val / 100.0)

        st.markdown("---")
        st.markdown("#### 🧠 Explanation of Current Score:")
        st.info(mission_rel["explanation"])

    st.markdown("---")
    st.markdown("### 📋 Mission Reliability Condition Thresholds")
    st.markdown("""
    | Condition Label | Score Range | Visual Status | Operational Context |
    | :--- | :---: | :---: | :--- |
    | **GOOD CONDITION** | `75% – 100%` | 🟢 Green | Engine operating in optimal thermodynamic and mechanical balance. |
    | **CAUTION** | `40% – 74%` | 🟡 Yellow | Subsystem degradation or abnormal telemetry active. Ground crew inspection scheduled. |
    | **HIGH RISK** | `< 40%` | 🔴 Red | Severe operating limit breach or multiple simultaneous faults. High probability of in-flight failure. |
    """)


# ==============================================================================
# MODULE 8: EXPLAINABLE ALERTS WITH SUGGESTIONS
# ==============================================================================
elif nav_module == "8. Explainable Alerts with Suggestions":
    st.subheader("💡 Explainable Alerts with Suggestions")
    st.write(
        "AeroGuard AI provides transparent, understandable explanations for every detected abnormal condition. "
        "Each alert displays the exact parameter, live simulated reading, demonstration threshold, primary physical reason, "
        "severity level, and actionable ground-crew maintenance suggestion."
    )

    alerts = evaluation["explainable_alerts"]
    highest_priority = evaluation["highest_priority_fault"]

    if len(alerts) == 0:
        st.success(
            "✅ **NOMINAL ENGINE OPERATING ENVELOPE:** All simulated sensor channels (Temperature, Oil Pressure, "
            "Vibration, and RPM) are operating within established demonstration bounds. No explainable alerts active."
        )
        st.markdown("""
        <div class="card-box" style="border-left: 4px solid #10b981;">
            <h4 style="margin:0; color:#34d399;">System Status: All Systems Go</h4>
            <p style="margin:6px 0 0 0; color:#cbd5e1;">Current engine telemetry shows no thermal excursions, sufficient hydrodynamic lubrication, minimal vibration shudder, and nominal engine speed.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Requirement: "If multiple faults are detected, display all of them and identify the highest-priority fault based on severity."
        if highest_priority:
            hp_border = "#ef4444" if highest_priority['severity'] == 'CRITICAL' else ('#f59e0b' if highest_priority['severity'] == 'HIGH' else '#38bdf8')
            hp_bg = "rgba(239, 68, 68, 0.1)" if highest_priority['severity'] == 'CRITICAL' else "rgba(245, 158, 11, 0.1)"
            st.markdown(f"""
            <div class="card-box" style="border: 2px solid {hp_border}; background: {hp_bg};">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <span style="font-size:17px; font-weight:800; color:{'#f87171' if highest_priority['severity'] == 'CRITICAL' else '#fbbf24'};">
                        ⭐ HIGHEST-PRIORITY FAULT IDENTIFIED: {highest_priority['alert_title']}
                    </span>
                    <span class="tag-{'critical' if highest_priority['severity'] == 'CRITICAL' else 'warning'}" style="font-size:12px;">
                        SEVERITY: {highest_priority['severity']} (PRIORITY 1)
                    </span>
                </div>
                <p style="margin:8px 0 4px 0; color:#e2e8f0; font-size:14px;">
                    <b>Abnormal Parameter:</b> <code>{highest_priority['parameter']}</code> &nbsp;|&nbsp; 
                    <b>Simulated Reading:</b> <code>{highest_priority['reading']}</code> &nbsp;|&nbsp; 
                    <b>Threshold:</b> <code>{highest_priority['threshold']}</code>
                </p>
                <p style="margin:4px 0 4px 0; color:#cbd5e1; font-size:13px;">
                    <b>Primary Reason:</b> {highest_priority['reason']}
                </p>
                <p style="margin:4px 0 4px 0; color:#38bdf8; font-size:13px;">
                    <b>Priority Justification:</b> {highest_priority['priority_reason']}
                </p>
                <p style="margin:6px 0 0 0; color:#34d399; font-size:14px; font-weight:700;">
                    🔧 <b>Immediate Suggestion:</b> {highest_priority['suggestion']}
                </p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown(f"### 🚨 All Active Alerts ({len(alerts)} Detected — Ordered by Severity Priority):")

        for idx, alert in enumerate(alerts, 1):
            sev_class = "tag-critical" if alert['severity'] == 'CRITICAL' else ("tag-warning" if alert['severity'] == 'HIGH' else "tag-warning")
            card_border = "#ef4444" if alert['severity'] == 'CRITICAL' else ("#f59e0b" if alert['severity'] == 'HIGH' else "#38bdf8")

            st.markdown(f"""
            <div class="card-box" style="border-left: 4px solid {card_border};">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <h4 style="margin:0; color:#f8fafc;">Alert #{idx}: {alert['alert_title']}</h4>
                    <span class="{sev_class}">SEVERITY: {alert['severity']}</span>
                </div>
                <div style="margin-top:10px; line-height:1.7; font-size:14px;">
                    <span style="color:#94a3b8;">• <b>Detected Abnormal Parameter:</b></span> <code style="color:#f8fafc;">{alert['parameter']}</code><br>
                    <span style="color:#94a3b8;">• <b>Actual Simulated Sensor Reading:</b></span> <span style="color:#38bdf8; font-weight:700;">{alert['reading']}</span><br>
                    <span style="color:#94a3b8;">• <b>Demonstration Threshold:</b></span> <span style="color:#cbd5e1;">{alert['threshold']}</span><br>
                    <span style="color:#94a3b8;">• <b>Main Reason for Alert:</b></span> <span style="color:#fcd34d;">{alert['reason']}</span><br>
                    <span style="color:#94a3b8;">• <b>Possible Maintenance Suggestion:</b></span> <span style="color:#34d399; font-weight:700;">{alert['suggestion']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Requirement: "Add a 'Why was this alert generated?' expandable section."
            with st.expander(f"🔍 Why was this {alert['alert_title']} generated? (Click to view detailed explanation)"):
                st.markdown(f"**Root Mechanism & Physics:** {alert['why_generated']}")
                st.markdown(f"**Operating Boundary:** Simulated Reading `{alert['reading']}` crossed threshold `{alert['threshold']}`.")
                st.markdown(f"**Safety Impact:** {alert['priority_reason']}")
                st.markdown(f"**Prescribed Action:** {alert['suggestion']}")

    st.markdown("---")
    st.markdown("### 📋 Explainable Alerts Diagnostic Reference Matrix")
    st.markdown("""
    | Condition | Alert Title | Monitored Parameter | Illustrative Threshold | Severity Level | Prescribed Maintenance Suggestion |
    | :--- | :--- | :--- | :---: | :---: | :--- |
    | **Oil Pressure Drop** | `Engine Alert!` | Oil Pressure | `< 30 PSI` | **CRITICAL** | Inspect the lubrication system and check for possible oil leakage. |
    | **Engine Overheating** | `High Temperature Alert!` | Engine Temperature | `> 110 °C` | **HIGH / CRITICAL** | Inspect the cooling system. |
    | **Abnormal Vibration** | `Vibration Alert!` | Engine Vibration | `> 7.0 / 10` | **HIGH** | Inspect engine mounting and rotating components. |
    | **Spark Plug Misfire** | `Ignition Fault Alert!` | Ignition / Vibration | Combustion Limit | **HIGH** | Inspect the ignition system and spark plugs. |
    | **High RPM** | `RPM Alert!` | Engine RPM | `> 5000 RPM` | **WARNING** | Check engine operating conditions against approved operating limits. |
    | **Sensor Disconnect** | `Sensor Fault Alert!` | Telemetry Signal | Signal Continuity | **HIGH** | Inspect sensor wiring harness and replace the transducer. |
    """)


# ==============================================================================
# MODULE 9: HISTORICAL SENSOR ANALYSIS
# ==============================================================================
elif nav_module == "9. Historical Sensor Analysis":
    st.subheader("📈 Historical Sensor Analysis & Trends")

    temp_dir, temp_icon, temp_col, temp_delta = calculate_trend_direction(history_df["temperature_c"], threshold_delta=2.0)
    oil_dir, oil_icon, oil_col, oil_delta = calculate_trend_direction(history_df["oil_pressure_psi"], threshold_delta=2.0)
    vib_dir, vib_icon, vib_col, vib_delta = calculate_trend_direction(history_df["vibration_level"], threshold_delta=0.5)
    rpm_dir, rpm_icon, rpm_col, rpm_delta = calculate_trend_direction(history_df["rpm"], threshold_delta=100.0)

    st.markdown("#### 🧭 Sensor Trend Directions (Last 60 Seconds)")
    tc1, tc2, tc3, tc4 = st.columns(4)

    with tc1:
        st.markdown(f"""
        <div class="sensor-card">
            <span class="sensor-label">Temperature Trend</span><br>
            <span style="font-size:20px; font-weight:700; color:{temp_col};">{temp_icon} {temp_dir}</span><br>
            <span style="font-size:12px; color:#cbd5e1;">Δ {temp_delta:+.1f} °C over 60s</span>
        </div>
        """, unsafe_allow_html=True)

    with tc2:
        st.markdown(f"""
        <div class="sensor-card">
            <span class="sensor-label">Oil Pressure Trend</span><br>
            <span style="font-size:20px; font-weight:700; color:{oil_col};">{oil_icon} {oil_dir}</span><br>
            <span style="font-size:12px; color:#cbd5e1;">Δ {oil_delta:+.1f} PSI over 60s</span>
        </div>
        """, unsafe_allow_html=True)

    with tc3:
        st.markdown(f"""
        <div class="sensor-card">
            <span class="sensor-label">Vibration Trend</span><br>
            <span style="font-size:20px; font-weight:700; color:{vib_col};">{vib_icon} {vib_dir}</span><br>
            <span style="font-size:12px; color:#cbd5e1;">Δ {vib_delta:+.2f} /10 over 60s</span>
        </div>
        """, unsafe_allow_html=True)

    with tc4:
        st.markdown(f"""
        <div class="sensor-card">
            <span class="sensor-label">Engine RPM Trend</span><br>
            <span style="font-size:20px; font-weight:700; color:{rpm_col};">{rpm_icon} {rpm_dir}</span><br>
            <span style="font-size:12px; color:#cbd5e1;">Δ {rpm_delta:+.0f} RPM over 60s</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:16px;'></div>", unsafe_allow_html=True)

    st.markdown("#### 📊 Interactive Parameter Trend Charts")
    col_chart_a, col_chart_b = st.columns(2)

    with col_chart_a:
        fig_temp = go.Figure()
        fig_temp.add_trace(go.Scatter(
            x=history_df["time_seconds"], y=history_df["temperature_c"],
            mode="lines", name="Temperature (°C)", line=dict(color="#f97316", width=2.5)
        ))
        fig_temp.add_hline(y=110, line_dash="dash", line_color="#ef4444", annotation_text="Threshold (110°C)")
        fig_temp.update_layout(
            title="Engine Temperature over Time (°C)",
            xaxis_title="Time to Present (s)", yaxis_title="Temperature (°C)",
            height=280, margin=dict(l=20, r=20, t=35, b=20),
            paper_bgcolor="#0b1120", plot_bgcolor="#0f172a", font=dict(color="#94a3b8")
        )
        st.plotly_chart(fig_temp, use_container_width=True)

        fig_vib = go.Figure()
        fig_vib.add_trace(go.Scatter(
            x=history_df["time_seconds"], y=history_df["vibration_level"],
            mode="lines", name="Vibration (/10)", line=dict(color="#eab308", width=2.5)
        ))
        fig_vib.add_hline(y=7.0, line_dash="dash", line_color="#ef4444", annotation_text="Threshold (7.0)")
        fig_vib.update_layout(
            title="Engine Vibration over Time (0-10)",
            xaxis_title="Time to Present (s)", yaxis_title="Vibration Level",
            height=280, margin=dict(l=20, r=20, t=35, b=20),
            paper_bgcolor="#0b1120", plot_bgcolor="#0f172a", font=dict(color="#94a3b8")
        )
        st.plotly_chart(fig_vib, use_container_width=True)

    with col_chart_b:
        fig_oil = go.Figure()
        fig_oil.add_trace(go.Scatter(
            x=history_df["time_seconds"], y=history_df["oil_pressure_psi"],
            mode="lines", name="Oil Pressure (PSI)", line=dict(color="#38bdf8", width=2.5)
        ))
        fig_oil.add_hline(y=30, line_dash="dash", line_color="#ef4444", annotation_text="Threshold (30 PSI)")
        fig_oil.update_layout(
            title="Oil Pressure over Time (PSI)",
            xaxis_title="Time to Present (s)", yaxis_title="Oil Pressure (PSI)",
            height=280, margin=dict(l=20, r=20, t=35, b=20),
            paper_bgcolor="#0b1120", plot_bgcolor="#0f172a", font=dict(color="#94a3b8")
        )
        st.plotly_chart(fig_oil, use_container_width=True)

        fig_rpm = go.Figure()
        fig_rpm.add_trace(go.Scatter(
            x=history_df["time_seconds"], y=history_df["rpm"],
            mode="lines", name="Engine RPM", line=dict(color="#a855f7", width=2.5)
        ))
        fig_rpm.add_hline(y=5000, line_dash="dash", line_color="#ef4444", annotation_text="Threshold (5000 RPM)")
        fig_rpm.update_layout(
            title="Engine RPM over Time (Speed)",
            xaxis_title="Time to Present (s)", yaxis_title="Engine RPM",
            height=280, margin=dict(l=20, r=20, t=35, b=20),
            paper_bgcolor="#0b1120", plot_bgcolor="#0f172a", font=dict(color="#94a3b8")
        )
        st.plotly_chart(fig_rpm, use_container_width=True)

    # Optional Telemetry Export
    st.markdown("---")
    csv_history = history_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Download Historical Telemetry Data (CSV)",
        data=csv_history,
        file_name=f"AeroGuardAI_Simulated_History_{evaluation['status']}.csv",
        mime="text/csv",
        use_container_width=True
    )


# ==============================================================================
# MODULE 10: MAINTENANCE RECOMMENDATIONS
# ==============================================================================
elif nav_module == "10. Maintenance Recommendations":
    st.subheader("🛠️ Prescriptive Maintenance Recommendations")

    st.markdown("### 🔍 Detected Abnormal Conditions & Inspection Recommendations")
    if len(evaluation["fault_details"]) == 0:
        st.success("✅ **All Parameters Within Limits:** No abnormal conditions detected. Perform standard pre-flight/post-flight routine servicing.")
    else:
        for idx, item in enumerate(evaluation["fault_details"], 1):
            with st.container():
                st.markdown(f"""
                <div class="card-box" style="border-left: 4px solid #38bdf8;">
                    <h4 style="margin:0; color:#38bdf8;">Abnormal Condition #{idx}: {item['warning']}</h4>
                    <p style="margin:6px 0 0 0; color:#e2e8f0;"><b>Parameter:</b> <code>{item['param']}</code> = <b>{item['val']}</b> (Threshold: {item['thresh']})</p>
                    <p style="margin:6px 0 0 0; font-size:16px; color:#34d399;">
                        🔧 <b>Inspection Recommendation:</b> {item['recommendation']}
                    </p>
                </div>
                """, unsafe_allow_html=True)

    st.markdown("---")

    # Maintenance Summary Card
    st.markdown("### 📋 Flight-Line Maintenance Summary")
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    col_s1, col_s2 = st.columns([1, 1.2])

    with col_s1:
        st.markdown(f"""
        <div class="card-box">
            <h4 style="margin:0 0 10px 0; color:#38bdf8;">Operational Status Overview</h4>
            <p><b>Current Engine Status:</b> <span class="tag-{evaluation['status'].lower()}">{evaluation['status']}</span></p>
            <p><b>Engine Health Score:</b> <code>{evaluation['health_score']} / 100 Points</code></p>
            <p><b>Mission Reliability:</b> <code>{mission_rel['reliability_score']}% ({mission_rel['condition_label']})</code></p>
            <p><b>Priority Level:</b> {evaluation['maint_priority']}</p>
            <p><b>Report Generation Timestamp:</b> <code>{now_str}</code></p>
        </div>
        """, unsafe_allow_html=True)

    with col_s2:
        temp_rep_str = "INVALID (ERR_OOR)" if (active_sensor_failure and "Temperature" in active_sensor_failure) else f"{sensor_temp:.1f} °C"
        st.markdown(f"""
        <div class="card-box">
            <h4 style="margin:0 0 10px 0; color:#38bdf8;">Current Sensor Readings</h4>
            <ul style="margin:0; padding-left:20px; line-height:1.8;">
                <li><b>Engine Temperature:</b> <code>{temp_rep_str}</code> (Threshold: 110°C)</li>
                <li><b>Oil Pressure:</b> <code>{sensor_oil:.1f} PSI</code> (Threshold: 30 PSI)</li>
                <li><b>Engine Vibration:</b> <code>{sensor_vib:.1f} / 10</code> (Threshold: 7.0)</li>
                <li><b>Engine RPM:</b> <code>{sensor_rpm:.0f} RPM</code> (Threshold: 5000 RPM)</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("#### 🛠️ Summary of Suggested Actions:")
    if len(evaluation["fault_details"]) == 0:
        st.info("✔️ Routine pre-flight visual walkaround and fluid level verification. Cleared for flight.")
    else:
        for idx, item in enumerate(evaluation["fault_details"], 1):
            st.markdown(f"- **{item['param']}:** {item['recommendation']}")


# ==============================================================================
# MODULE 11: REPORTS AND CSV DOWNLOAD
# ==============================================================================
elif nav_module == "11. Reports and CSV Download":
    st.subheader("📄 Engine Health Monitoring Reports & CSV Export")

    now_dt = datetime.now()
    now_str = now_dt.strftime("%Y-%m-%d %H:%M:%S")
    file_timestamp = now_dt.strftime("%Y%m%d_%H%M%S")

    faults_text = " | ".join([f['warning'] for f in evaluation["fault_details"]]) if evaluation["fault_details"] else "None (All parameters normal)"
    actions_text = " | ".join([f['recommendation'] for f in evaluation["fault_details"]]) if evaluation["fault_details"] else "Routine pre-flight inspection"
    alerts_text = " | ".join([f"{a['alert_title']} [{a['severity']}]: {a['reason']}" for a in evaluation["explainable_alerts"]]) if evaluation["explainable_alerts"] else "None (Nominal Telemetry)"

    temp_export_val = "INVALID (ERR_OOR)" if (active_sensor_failure and "Temperature" in active_sensor_failure) else f"{sensor_temp:.1f} °C"

    summary_report_data = {
        "Metric / Item": [
            "Report Generation Date & Time",
            "Current Engine Status",
            "Engine Health Score (Points)",
            "Mission Reliability Score (%)",
            "Mission Condition Assessment",
            "Engine Temperature",
            "Oil Pressure",
            "Engine Vibration Level",
            "Engine RPM (Speed)",
            "Active Fault Injection",
            "Detected Faults",
            "Explainable Alerts (Feature 3)",
            "Suggested Maintenance Actions",
            "Operational Guidance",
            "Demonstration Disclaimer"
        ],
        "Value / Details": [
            now_str,
            evaluation["status"],
            f"{evaluation['health_score']} / 100",
            f"{mission_rel['reliability_score']}%",
            mission_rel["condition_label"],
            temp_export_val,
            f"{sensor_oil:.1f} PSI",
            f"{sensor_vib:.1f} / 10",
            f"{sensor_rpm:.0f} RPM",
            st.session_state["active_fault"] if st.session_state["active_fault"] else "None (Nominal Telemetry)",
            faults_text,
            alerts_text,
            actions_text,
            evaluation["condition_guidance"],
            "Illustrative demonstration report. Must not replace approved aircraft maintenance procedures."
        ]
    }
    summary_df = pd.DataFrame(summary_report_data)

    st.markdown("### 📋 Executive Maintenance Summary Report")
    st.dataframe(summary_df, use_container_width=True, hide_index=True)

    csv_summary_bytes = summary_df.to_csv(index=False).encode("utf-8")
    
    col_dl1, col_dl2 = st.columns([1, 1.5])
    with col_dl1:
        st.download_button(
            label="📥 Download Monitoring Report (CSV)",
            data=csv_summary_bytes,
            file_name=f"AeroGuardAI_Maintenance_Report_{evaluation['status']}_{file_timestamp}.csv",
            mime="text/csv",
            use_container_width=True
        )
    with col_dl2:
        st.caption("Click above to download this formatted monitoring report as an official CSV record.")

    st.markdown("---")

    with st.expander("📊 View & Download Full 60-Second Historical Telemetry Log"):
        export_history_df = history_df.copy()
        export_history_df["Status_At_T0"] = evaluation["status"]
        export_history_df["Health_Score_At_T0"] = evaluation["health_score"]
        export_history_df["Reliability_Score_At_T0"] = mission_rel["reliability_score"]
        export_history_df["Mission_Condition_At_T0"] = mission_rel["condition_label"]
        export_history_df["Detected_Faults"] = faults_text
        export_history_df["Explainable_Alerts"] = alerts_text
        export_history_df["Recommended_Action"] = actions_text
        
        csv_history_bytes = export_history_df.to_csv(index=False).encode("utf-8")
        st.dataframe(export_history_df.tail(15), use_container_width=True)
        st.download_button(
            label="📥 Download Complete 60-Second Telemetry Log (CSV)",
            data=csv_history_bytes,
            file_name=f"AeroGuardAI_60s_Telemetry_{evaluation['status']}_{file_timestamp}.csv",
            mime="text/csv"
        )


# ==============================================================================
# MODULE 12: ABOUT THE PROJECT
# ==============================================================================
elif nav_module == "12. About the Project":
    st.subheader("ℹ️ About AeroGuard AI: Architecture & Defence Impact")
    
    st.markdown("""
    ### 🎯 Hackathon Theme: AI in Defence
    **Full Title:** *AI-Based Digital Twin for Health Monitoring, Fault Detection and Mission Reliability Enhancement of Aero Piston Engines used in MALE UAVs.*

    ---

    ### 🛡️ Why This Project Matters
    - **MALE UAVs (Medium Altitude Long Endurance Unmanned Aerial Vehicles)** conduct long-endurance reconnaissance and surveillance missions (24+ continuous hours).
    - They rely on **turbocharged aero piston engines**.
    - If engine oil pressure drops or cylinder heads overheat over remote terrain, the UAV suffers in-flight engine seizure, leading to the **catastrophic loss of a multimillion-dollar defence asset**.
    - **AeroGuard AI** provides a real-time **Digital Twin** that continuously benchmarks live sensor telemetry against nominal physical behavior, alerting operators before critical damage occurs.

    ---

    ### 💻 Technology Stack & Principles
    - **100% Lightweight & Explainable:** Built purely with Python, Streamlit, Pandas, NumPy, and Plotly.
    - **Zero Black-Box Guesswork:** Transparent, rule-based Digital Twin anomaly detection with clear physical reasoning.
    - **Dual Input Modes:** 3 Predefined benchmark flight scenarios (Healthy, Warning, Critical) + full Manual Slider Control.
    - **Feature 1 — Fault Injection Panel:** Dedicated testing rig simulating Spark Plug Misfire, Oil Pressure Drop, Overheating, Abnormal Vibration, High RPM, and Sensor Disconnection with real-time measured latency.
    - **Feature 2 — Mission Reliability Score:** Weighted endurance model computing circular gauge reliability ratings (0–100%) and condition labels (`GOOD CONDITION`, `CAUTION`, `HIGH RISK`).
    - **Feature 3 — Explainable Alerts with Suggestions:** Clear alert titles, physical root reasons, demonstration threshold comparisons, multi-fault severity prioritization, and actionable ground-crew maintenance suggestions.
    - **Actionable Output:** 100-point Health Score, clear warnings, parameter explanations, and prescriptive maintenance recommendations.
    """)
