# 🛡️ AeroGuard AI
### AI-Based Digital Twin for Health Monitoring, Fault Detection and Mission Reliability Enhancement of Aero Piston Engines used in MALE UAVs
**Theme:** AI in Defence  
**Target Platform:** Medium Altitude Long Endurance (MALE) UAVs (e.g., MQ-1 Predator, Heron, Rustom-II) powered by Turbocharged Aero Piston Engines.

---

## ⚡ 1. How to Run the Application

In your terminal or PowerShell inside the project directory:

```powershell
streamlit run app.py
```

The application will launch immediately in your browser at:  
👉 **`http://localhost:8501`**

---

## 🏗️ 2. Project Architecture

AeroGuard AI is structured into a clean, 3-tier architecture built with **Python, Streamlit, Pandas, NumPy, and Plotly**:

```text
┌────────────────────────────────────────────────────────────────────────┐
│                   AEROGUARD AI SYSTEM ARCHITECTURE                     │
├────────────────────────────────────────────────────────────────────────┤
│ 1. TELEMETRY & SIMULATION LAYER (NumPy)                                │
│    ├── Predefined Flight Presets (Healthy, Warning, Critical)          │
│    ├── Independent Manual Sliders (Temp, Oil, Vib, RPM)                │
│    └── 60-Second Time-Series Physics Trend Generator                   │
├────────────────────────────────────────────────────────────────────────┤
│ 2. DIGITAL TWIN ANOMALY & HEALTH ENGINE (Python / Logic)               │
│    ├── Physics-Grounded Demonstration Threshold Checker                │
│    ├── 100-Point Deductive Health Score Calculator                     │
│    ├── Status Classifier (HEALTHY / WARNING / CRITICAL)                │
│    └── Condition-to-Inspection Maintenance Engine                      │
├────────────────────────────────────────────────────────────────────────┤
│ 3. AEROSPACE COMMAND DASHBOARD LAYER (Streamlit & Plotly)              │
│    ├── Top Status Banner & 4 Core Metric Cards                         │
│    ├── 2D Virtual Engine Twin Schematic (Plotly Dynamic Coloring)      │
│    ├── Interactive Parameter Trend Graphs (Plotly Lines & Redlines)    │
│    └── Downloadable Ground-Crew Audit Reports (Pandas CSV Export)      │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 🧭 3. How Each Module Works

| Module # | Module Name | Core Functionality |
| :---: | :--- | :--- |
| **1** | **🏠 Home Dashboard** | Comprehensive command center displaying top metric cards, the 2D Virtual Engine schematic, health score gauge, active explainable alerts, and tactical advisory status. |
| **2** | **⚙️ Virtual Engine Monitoring** | Interactive 2D schematic of an opposed 4-cylinder aero piston engine. Cylinders, crankcase, oil gallery, and propeller hub update colors dynamically in real time. |
| **3** | **🎛️ Sensor Monitoring** | Dual-input interface supporting 1-click **Predefined Scenarios** (Healthy, Warning, Critical) and **Manual Input** via independent sliders. |
| **4** | **🔍 Fault Detection** | Transparent, rule-based anomaly detection displaying active warnings, explaining abnormal parameters, and identifying physical causes. |
| **5** | **📊 Engine Health Score** | Visual gauge and progress bar displaying the 100-point composite score with an itemized points-deduction audit log. |
| **6** | **⚡ Fault Injection Panel** | Dedicated testing rig to inject faults (Spark Plug Misfire, Oil Pressure Drop, Overheating, Vibration, High RPM, Sensor Failure) and measure real-time detection latency. |
| **7** | **🛡️ Mission Reliability Score** | Dynamic circular gauge calculating continuous mission endurance reliability (0–100%) with condition labels (GOOD CONDITION, CAUTION, HIGH RISK) and degradation explanations. |
| **8** | **💡 Explainable Alerts with Suggestions** | Plain-language fault diagnosis with alert titles, detected readings vs. demonstration thresholds, root physical reasons, severity levels, multi-fault priority ranking, and actionable maintenance suggestions. |
| **9** | **📈 Historical Sensor Analysis** | 4 Plotly interactive charts with demonstration threshold redlines, trend direction indicators (Increasing/Decreasing/Stable), and a 60-second telemetry table. |
| **10** | **🛠️ Maintenance Recommendations** | Prescriptive ground-crew inspection procedures mapped directly to each detected abnormal condition. |
| **11** | **📄 Reports and CSV Download** | One-click export of an official executive monitoring report and full 60-second time-series telemetry log in CSV format. |
| **12** | **ℹ️ About the Project** | Detailed background on MALE UAV propulsion vulnerability, defence mission criticality, and technical methodology. |

---

## 📡 4. Which Parts Use Simulated Data

To ensure complete transparency during hackathon evaluation:
- **Simulated Component:** All sensor inputs (Temperature, Oil Pressure, Vibration, and RPM) and the 60-second historical time series are simulated in-memory using **NumPy**.
- **Real Component:** The Digital Twin diagnostic evaluation, 100-point health score computation, dynamic 2D schematic rendering, and CSV report generation run in real time on the active data.
- **Explicit Notice:** The application does **not** claim to be connected to physical aircraft hardware or real flight telemetry.

---

## 🔍 5. How Fault Detection Works

AeroGuard AI avoids unexplainable black-box machine learning. It uses a **transparent, physics-informed rule baseline** with four demonstration thresholds:

1. **Engine Temperature $> 110^\circ\text{C}$** $\rightarrow$ Triggers *"High temperature detected"* $\rightarrow$ Recommends inspecting the cooling system.
2. **Oil Pressure $< 30\text{ PSI}$** $\rightarrow$ Triggers *"Low oil pressure detected"* $\rightarrow$ Recommends inspecting the lubrication system.
3. **Engine Vibration $> 7.0$** $\rightarrow$ Triggers *"Abnormal vibration detected"* $\rightarrow$ Recommends inspecting engine mounting and rotating components.
4. **Engine RPM $> 5000\text{ RPM}$** $\rightarrow$ Triggers *"High RPM detected"* $\rightarrow$ Recommends checking operating conditions against approved limits.

---

## 🧮 6. How the Engine Health Score is Calculated

The illustrative health score starts with a baseline of **100 points**:

$$\text{Health Score} = \max\left(0,\; 100 - \sum \text{Deductions}\right)$$

### Point Deduction Rules:
- **$-25$ points** for High Temperature ($> 110^\circ\text{C}$)
- **$-25$ points** for Low Oil Pressure ($< 30\text{ PSI}$)
- **$-25$ points** for Abnormal Vibration ($> 7.0$)
- **$-15$ points** for High RPM ($> 5000\text{ RPM}$)
- The score is clamped so it **never falls below zero**.

### Health Status Brackets:
- **75 – 100 Points:** `HEALTHY` (when zero faults are active)
- **40 – 74 Points:** `WARNING` (or 75 with 1 active fault)
- **Below 40 Points:** `CRITICAL`

---

## 🎯 7. How the Mission Reliability Score is Calculated (Feature 2)

Unlike the discrete rule-based Engine Health Score, the **Mission Reliability Score** is an illustrative continuous index (0–100%) modeling propulsion endurance margin for MALE UAV surveillance sorties:

- **Lubrication Margin (35% weight):** Evaluates distance of oil pressure above the 30 PSI minimum threshold.
- **Thermal Margin (25% weight):** Evaluates distance of cylinder head temperature below the 110°C limit.
- **Vibration Margin (25% weight):** Evaluates stability below the 7.0 IPS abnormal threshold.
- **RPM Reserve (15% weight):** Evaluates operational headroom below 5000 RPM.
- **Active Fault Severity Penalty:** Deducts up to an additional 25 points based on cumulative active physical faults.

### Mission Condition Labels:
- **75 – 100%:** `GOOD CONDITION` (Green) — Nominal operating parameters.
- **40 – 74%:** `CAUTION` (Yellow) — Degradation detected; increased surveillance risk.
- **Below 40%:** `HIGH RISK` (Red) — Critical margin breach; urgent attention required.

> **Safety Notice:** This score is an illustrative demonstration and never authorizes a UAV to continue flight or override approved military aviation technical orders. Real mission decisions require approved procedures and qualified personnel.

---

## 💡 8. Explainable Alerts with Suggestions (Feature 3)

AeroGuard AI provides **plain-language explainability** for every detected anomaly, avoiding opaque black-box machine learning percentages:

### Alert Reference Standards:
| Anomaly Mode | Alert Title | Primary Reason | Prescribed Maintenance Suggestion | Severity |
| :--- | :--- | :--- | :--- | :---: |
| **Oil Pressure Drop** | `Engine Alert!` | Oil pressure is below the illustrative threshold. | Inspect the lubrication system and check for possible oil leakage. | **CRITICAL** |
| **Engine Overheating** | `High Temperature Alert!` | Engine temperature is above the illustrative threshold. | Inspect the cooling system. | **HIGH / CRITICAL** |
| **Abnormal Vibration** | `Vibration Alert!` | Vibration exceeds the illustrative threshold. | Inspect engine mounting and rotating components. | **HIGH** |
| **Spark Plug Misfire** | `Ignition Fault Alert!` | Simulated misfire detected through abnormal engine behaviour. | Inspect the ignition system and spark plugs. | **HIGH** |
| **High RPM** | `RPM Alert!` | RPM exceeds the illustrative demonstration threshold. | Check engine operating conditions against approved operating limits. | **WARNING** |
| **Sensor Disconnect** | `Sensor Fault Alert!` | Sensor signal is out-of-range or invalid (signal lost). | Inspect sensor wiring harness and replace the transducer. | **HIGH** |

### Multi-Fault Severity Prioritization:
When multiple simultaneous anomalies occur, AeroGuard AI evaluates severity ranks and designates the **Highest-Priority Fault** (e.g., Oil Pressure loss takes precedence because hydrodynamic bearing failure risks sudden engine lockup within minutes).

### "Why was this alert generated?" Deep Dives:
Each alert includes an interactive expandable section detailing the thermodynamic and mechanical physics behind the threshold excursion.

---

## ⏱️ 9. Three-Minute Judge Presentation Script

| Time | Action | What to Say / Point Out to Judges |
| :---: | :--- | :--- |
| **0:00 - 0:45** | **Home Dashboard (Healthy Preset)** | *"MALE UAVs conduct 24+ hour long-endurance border surveillance. Engine failures mid-sortie cause the loss of multimillion-dollar defence assets. AeroGuard AI provides a Digital Twin that monitors propulsion health. Currently, in Healthy mode, all 4 sensors are nominal, the Health Score is 100, and Mission Reliability is 100% (GOOD CONDITION)."* |
| **0:45 - 1:30** | **Fault Injection Panel (Feature 1)** | *"Let's test dynamic fault injection in Module 4: Select 'Oil Pressure Drop' and click 'Start Fault Simulation'. In under 0.05 ms, the Digital Twin detects the pressure drop, alerts ground command, drops the Health Score to 75, and updates component colors on the 2D engine schematic."* |
| **1:30 - 2:15** | **Mission Reliability & Explainable Alerts (Features 2 & 3)** | *"In Module 5, the circular gauge models endurance reserve at 70% CAUTION. Now look at Module 6 (Feature 3): Instead of confusing black-box percentages, AeroGuard AI produces an 'Engine Alert!' with the exact reason, threshold, and suggestion ('Inspect lubrication system'). If multiple faults occur, it automatically identifies the highest-priority critical fault."* |
| **2:15 - 3:00** | **Trend Graphs & CSV Export** | *"In Module 9, interactive Plotly charts display 60 seconds of telemetry against threshold redlines. In Module 11, ground crews can export a complete CSV audit report with one click. In summary, AeroGuard AI provides an explainable, lightweight Digital Twin to protect national defence UAVs."* |

---

## 🚀 10. What is Implemented vs. Future Work

### ✅ What is Implemented in this Prototype:
- Full 12-module Streamlit & Plotly aerospace dashboard.
- Dual-mode sensor inputs: 3 Predefined Scenarios (Healthy, Warning, Critical) + 4 Manual Sliders.
- **Feature 1 (Fault Injection Panel):** 6 selectable fault modes with dynamic microsecond latency detection.
- **Feature 2 (Mission Reliability Score):** Interactive circular gauge, 4 weighted degradation factors, condition labels (GOOD CONDITION, CAUTION, HIGH RISK).
- **Feature 3 (Explainable Alert with Suggestion):** Structured plain-language explanations, severity ratings, multi-fault priority ranking, and deep 'Why was this alert generated?' expanders.
- Dynamic 2D Virtual Engine schematic with real-time component color coding.
- Transparent, explainable rule-based anomaly detection engine.
- 100-point deductive health scoring model with status classification.
- 4 interactive historical trend charts with directional arrows (▲/▼/■).
- Prescriptive ground-crew maintenance recommendations.
- Executive monitoring report generation with 1-click CSV download.
- 100% automated test suite (`test_aeroguard.py`) with 30/30 passing tests.

### 🔮 Future Work (Post-Hackathon Roadmap):
- **Hardware Telemetry Integration:** Ingest live MAVLink / ARINC-429 telemetry streams from actual UAV avionics hardware.
- **Thermodynamic Digital Twin Physics:** Integrate full 1D thermodynamic differential equations (calculating volumetric efficiency and indicated mean effective pressure).
- **Remaining Useful Life (RUL) Prognostics:** Train physics-informed neural networks (PINNs) on historical engine teardown data to predict hours until component failure.
- **Edge Deployment:** Package the lightweight Python runtime onto radiation-hardened onboard UAV mission computers (e.g., NVIDIA Jetson Orin Defence).
