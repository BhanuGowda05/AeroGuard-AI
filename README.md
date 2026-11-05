# 🚀 AeroGuard AI – AI-Powered Digital Twin for Aero Engine Health Monitoring

An intelligent, software-based digital twin prototype designed for health monitoring, fault detection, and mission reliability analysis of aero piston engines used in MALE (Medium Altitude Long Endurance) UAVs.

AeroGuard AI demonstrates how engine sensor data can be monitored and analysed in real time to identify abnormal operating conditions, simulate critical engine faults, calculate comprehensive engine health scores, and provide explainable maintenance recommendations through an interactive aerospace dashboard.

---

## 📌 Overview

**AeroGuard AI** is designed to simplify aero piston engine health monitoring through a virtual digital twin engine representation and an interactive command dashboard.

The system demonstrates how crucial engine parameters can be continuously evaluated to identify potential operating abnormalities before catastrophic in-flight mechanical failure occurs.

### Users can:
* **Monitor** core engine parameters: Temperature, Oil Pressure, Dynamic Vibration, and RPM.
* **View** an interactive CAD schematic matrix digital twin of an opposed 4-cylinder aero piston engine.
* **Simulate** 6 real-world engine fault conditions via a dedicated Fault Injection Panel.
* **Detect** abnormal sensor readings with zero-latency rule-based logic.
* **Calculate** an illustrative Engine Health Score (0–100 pts) with transparent penalty breakdowns.
* **Analyze** an illustrative Mission Reliability Score (0–100%) weighted by critical thermodynamic and lubrication factors.
* **Receive** plain-language, explainable fault alerts paired with prescriptive maintenance suggestions.
* **Visualize** historical sensor trends and real-time dual-harmonic vibration waveforms.
* **Export** official maintenance inspection reports and 60-second time-series logs as CSV files.

> **Note:** The current prototype uses simulated telemetry readings and explainable rule-based fault detection. Real engine sensor hardware integration and validated predictive analytics represent future engineering phases.

---

## ✨ Key Features

| Feature | Description |
| :--- | :--- |
| ✈️ **Virtual Engine Monitoring** | Interactive CAD schematic of an opposed 4-cylinder aero piston engine updating component status dynamically. |
| 🌡️ **Sensor Monitoring** | Real-time monitoring of Engine Temperature, Oil Pressure, Dynamic Vibration, and RPM with dual input modes (Presets & Manual Sliders). |
| 🧪 **Fault Injection Panel** | Real-time simulation of 6 engine failure modes to rigorously evaluate system detection response and latency. |
| 🔍 **Fault Detection** | Instantaneous identification of abnormal conditions based on physical aerospace operating limits. |
| ❤️ **Engine Health Score** | Dynamic composite score (0–100 pts) reflecting instantaneous mechanical state (HEALTHY / WARNING / CRITICAL). |
| 🎯 **Mission Reliability Score** | Forward-looking endurance index (0–100%) based on weighted thermodynamic, structural, and lubrication factors. |
| 🚨 **Explainable Alerts** | Detailed fault diagnosis highlighting abnormal parameters, actual readings, thresholds, root physical causes, and severity. |
| 🔧 **Maintenance Suggestions** | Prescriptive ground-crew inspection actions mapped directly to detected abnormalities. |
| 📈 **Historical Sensor Analysis** | Interactive 60-second trend charts with threshold redlines and directional indicators (Increasing, Decreasing, Stable). |
| 📊 **Command Dashboard** | Military/aerospace command UI featuring capsule gauges, circular dials, and live vibration waveforms. |
| 📄 **Reports & CSV Export** | One-click generation and download of complete diagnostic reports and raw telemetry data. |

---

## 🛠️ Technology Stack

| Layer | Technology | Purpose |
| :--- | :--- | :--- |
| **Programming Language** | Python 3.10+ | Core analytical models, telemetry simulation, and application logic |
| **Frontend / UI** | Streamlit | High-frequency reactive dashboard and telemetry controls |
| **Numerical Computation** | NumPy | Vectorized math, historical sensor generation, and trend calculation |
| **Data Processing** | Pandas | Time-series data management, tabular telemetry, and CSV report export |
| **Visualization** | Plotly | Interactive CAD engine schematics and dual-harmonic vibration waveforms |
| **Styling** | Custom CSS | Deep space navy aerospace theme with glassmorphic monitoring cards |

---

## 🗂️ Project Structure

```text
AeroGuard-AI/
│
├── app.py                  # Main Streamlit application with interactive command dashboard & modules
├── digital_twin.py         # Digital Twin state representation & analytical models
├── engine_simulator.py     # Aero engine telemetry simulation engine
├── test_aeroguard.py       # Comprehensive 30-test automated verification suite
├── requirements.txt        # Project Python dependencies
├── README.md               # Complete project documentation & presentation guide
└── .gitignore              # Git ignore rules for clean repository state
```

---

## ⚙️ How It Works

```text
       Simulated Engine Telemetry (NumPy)
                       ↓
       Data Acquisition & Ingestion (app.py)
                       ↓
   Virtual Digital Twin Model (CAD Schematic)
                       ↓
          Rule-Based Fault Detection System
                       ↓
           ┌───────────┴───────────┐
           ↓                       ↓
  Engine Health Score     Mission Reliability Score
   (Current Condition)       (Endurance Forecast)
           └───────────┬───────────┘
                       ↓
          Explainable Alerts (XAI)
                       ↓
      Prescriptive Maintenance Actions
                       ↓
   Interactive Command Dashboard (Plotly & CSV)
```

---

## 🎛️ Sensor Operating Envelopes

The system monitors four core engine parameters based on standard aero piston engine operating limits:

| Parameter | Nominal Range | Warning Limit | Critical Threshold | Purpose |
| :--- | :---: | :---: | :---: | :--- |
| **Engine Temperature** | 70°C – 105°C | > 110°C | > 125°C | Monitors cylinder head & coolant thermal stress |
| **Oil Pressure** | 45 – 75 PSI | < 30 PSI | < 25 PSI | Monitors lubrication health and oil line integrity |
| **Dynamic Vibration** | 1.0 – 5.0 / 10 | > 7.0 / 10 | > 8.5 / 10 | Detects airframe structural and mounting fatigue |
| **Engine Speed (RPM)**| 2200 – 4800 RPM | > 5000 RPM | > 5400 RPM | Monitors powertrain rotational envelope |

---

## 🧪 Fault Injection Scenarios

The onboard Fault Injection Panel allows operators to simulate 6 realistic in-flight failure modes:

| Fault Type | Simulated Condition | Detection Logic | Primary Affected Subsystem |
| :--- | :--- | :--- | :--- |
| **Spark Plug Misfire** | Vibration spikes to 8.2/10, RPM drops to 2600 | Vibration > 7.0 limit | Ignition System & Spark Plugs |
| **Oil Pressure Drop** | Oil pressure drops to 18.0 PSI | Oil Pressure < 30 PSI | Lubrication System & Oil Lines |
| **Engine Overheating** | Temperature rises to 128.0°C | Temperature > 110°C | Cooling Radiator & Cylinder Heads |
| **Abnormal Vibration** | Vibration elevates to 9.1/10 | Vibration > 7.0 limit | Engine Mounts & Rotating Assembly |
| **High RPM** | Engine speed reaches 5450 RPM | RPM > 5000 limit | Propeller Governor & Throttle Linkage |
| **Sensor Failure** | Out-of-range / open-circuit telemetry (`ERR_OOR`) | Validity Range Check | Avionics Sensor Wiring & Transducers |

---

## 🧠 Health & Reliability Scoring Methodology

### 1. Engine Health Score (0–100 pts)
Evaluates current mechanical status through deduction penalties:
* **100 pts:** Optimal operating condition (`HEALTHY`).
* **75–99 pts:** Minor threshold violation (`WARNING`).
* **< 50 pts:** Multiple or severe threshold violations (`CRITICAL`).

### 2. Mission Reliability Score (0–100%)
Evaluates remaining flight endurance using physics-grounded sub-factor weights:
$$\text{Reliability} = (0.35 \times R_{\text{oil}}) + (0.25 \times R_{\text{temp}}) + (0.25 \times R_{\text{vib}}) + (0.15 \times R_{\text{rpm}}) - \text{Penalty}_{\text{faults}}$$

* **75% – 100%:** `GOOD CONDITION` (Nominal mission endurance).
* **40% – 74%:** `CAUTION` (Elevated thermal or mechanical stress; monitor closely).
* **Below 40%:** `HIGH RISK` (Immediate mission abort or emergency divert recommended).

---

## 🚀 Installation & Running

### Prerequisites
* Python 3.10, 3.11, 3.12, or 3.13
* Git

### Step-by-Step Setup

```bash
# 1. Clone the repository
git clone https://github.com/BhanuGowda05/AeroGuard-AI.git
cd AeroGuard-AI

# 2. Create and activate a virtual environment
# Windows:
python -m venv venv
venv\Scripts\activate

# macOS / Linux:
python3 -m venv venv
source venv/bin/activate

# 3. Install required dependencies
pip install -r requirements.txt

# 4. Run automated test suite (verifies all 30 tests)
python test_aeroguard.py

# 5. Launch the AeroGuard AI application
streamlit run app.py
```

The application will launch immediately in your default browser at:  
👉 **`http://localhost:8501`**

---

## 💻 How to Use

1. **Explore the Command Center:** Navigate to `1. Home Dashboard` to see real-time capsule dials, the prominent CAD Digital Twin, parameters, active alerts, and live vibration waveforms.
2. **Switch Predefined Scenarios:** Use the sidebar to switch between `Healthy`, `Warning`, and `Critical` flight presets.
3. **Test Manual Slider Inputs:** Switch to `Manual Input` and adjust temperature, oil pressure, vibration, and RPM sliders to simulate custom operating conditions.
4. **Inject Live Faults:** Open `6. Fault Injection Panel`, select an in-flight fault (e.g., *Oil Pressure Drop* or *Spark Plug Misfire*), and click **Start Fault Simulation**.
5. **Inspect Explainable Alerts:** Review plain-language root causes and suggested maintenance actions in `8. Explainable Alerts with Suggestions`.
6. **Analyze Historical Trends:** Open `9. Historical Sensor Analysis` to examine 60-second parameter trends and redlines.
7. **Export Maintenance Reports:** Navigate to `11. Reports and CSV Download` to download full executive monitoring reports and telemetry logs.

---

## 🔮 Future Enhancements

* Real-time integration with physical engine sensors via standard aerospace protocols (**ARINC 429, CAN aerospace, MAVLink**).
* Edge AI deployment on SWaP-constrained UAV mission computers (NVIDIA Jetson, ARM Cortex).
* Remaining Useful Life (**RUL**) prediction using Weibull survival degradation models.
* High-frequency acoustic FFT spectral analysis to detect cylinder micro-cracking prior to vibration threshold breaches.
* Multi-engine synchronization for twin-engine tactical UAV architectures.

---

## 📚 Project Information

* **Project Name:** AeroGuard AI
* **Domain:** Artificial Intelligence / Aerospace / Digital Twin Technology
* **Application Area:** Aero Piston Engine Health Monitoring for MALE UAVs
* **Project Type:** AI in Defence Hackathon Prototype
* **Development Approach:** Software-Based Analytical Digital Twin Demonstrator

---

## 👩‍💻 Developed By

**Team AeroGuard AI**
* **Bhanushree G**
* **Pallabi Mandal**
* **Shaik Hazibee**
* **Pavani**

* **Department:** Computer Science and Engineering – Data Science  
* **Institution:** Nagarjuna College of Engineering and Technology (NCET)

---

## 📄 Disclaimer

*AeroGuard AI is an educational and hackathon demonstration prototype utilizing simulated engine telemetry. Its scores, thresholds, fault simulations, and maintenance recommendations are illustrative only. It is not an aviation-certified monitoring system and must not replace approved aircraft maintenance manuals or operational flight procedures.*
