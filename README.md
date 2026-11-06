# 🚀 AeroGuard AI – AI-Powered Digital Twin for Aero Engine Health Monitoring

An intelligent, software-based digital twin prototype designed for health monitoring, fault detection and mission reliability analysis of aero piston engines used in MALE (Medium Altitude Long Endurance) UAVs.

AeroGuard AI demonstrates how engine sensor data can be monitored and analysed in real time to identify abnormal conditions, simulate engine faults, calculate engine health scores and provide explainable maintenance recommendations through an interactive dashboard.

---

## 📌 Overview

**AeroGuard AI** is designed to simplify aero piston engine health monitoring through a virtual engine representation and an interactive monitoring dashboard.

The system demonstrates how crucial engine parameters can be continuously analysed to identify potential operating abnormalities before in-flight failure occurs.

### Users can:
* **Monitor** engine temperature, oil pressure, vibration and RPM in real time.
* **View** a virtual CAD schematic matrix representation of an aero piston engine.
* **Simulate** 6 different engine fault conditions using the onboard Fault Injection Panel.
* **Detect** abnormal sensor readings using physical demonstration limits.
* **Calculate** an illustrative engine health score (0–100 pts).
* **Analyse** an illustrative mission reliability score (0–100%).
* **Receive** explainable fault alerts and prescriptive maintenance suggestions.
* **Visualize** historical sensor trends and live dual-harmonic vibration waveforms.
* **Download** generated monitoring reports as a CSV file.

> **Note:** The current prototype uses simulated sensor readings and explainable rule-based fault detection. Real engine sensor hardware integration and validated predictive analytics are future engineering enhancements.

---

## ✨ Key Features

| Feature | Description |
| :--- | :--- |
| ✈️ **Virtual Engine Monitoring** | Displays an interactive CAD schematic of an aero piston engine updating component status dynamically. |
| 🌡️ **Sensor Monitoring** | Monitors temperature, oil pressure, vibration and RPM with predefined scenarios and manual slider controls. |
| 🧪 **Fault Injection Panel** | Simulates 6 different engine faults to evaluate the monitoring system's real-time detection response. |
| 🔍 **Fault Detection** | Identifies abnormal sensor readings instantaneously using predefined demonstration thresholds. |
| ❤️ **Engine Health Score** | Calculates an illustrative composite health score (0–100 pts) based on detected abnormalities. |
| 🎯 **Mission Reliability Score** | Displays an illustrative reliability indicator (0–100%) using weighted engine condition factors. |
| 🚨 **Explainable Alerts** | Explains detected faults, affected parameters, actual readings, thresholds and root causes. |
| 🔧 **Maintenance Suggestions** | Provides possible inspection recommendations mapped directly to detected abnormalities. |
| 📈 **Historical Sensor Analysis** | Displays simulated sensor trends and directional indicators using interactive Plotly graphs. |
| 📊 **Command Dashboard** | Presents engine monitoring information through an aerospace dark-navy command dashboard with live vibration waveforms. |
| 📄 **Reports & CSV Download** | Allows users to generate and download comprehensive engine monitoring reports as CSV files. |

---

## 🛠️ Technology Stack

| Layer | Technology | Description |
| :--- | :--- | :--- |
| **Programming Language** | Python 3.10+ | Core analytical models, telemetry simulation and logic |
| **Frontend / UI** | Streamlit | High-frequency reactive dashboard and telemetry controls |
| **Numerical Computation** | NumPy | Vectorized math, historical telemetry generation and noise modeling |
| **Data Processing** | Pandas | Time-series data management, tabular metrics and CSV reporting |
| **Visualization** | Plotly | Interactive CAD engine schematics and dual-harmonic vibration waveforms |
| **Styling** | Custom CSS | Deep space navy aerospace theme with glassmorphic monitoring cards |
| **Testing** | Automated Test Suite | Comprehensive 30-test automated verification script (`test_aeroguard.py`) |

> ⚠️ **Important:** The current prototype uses rule-based anomaly detection and an analytical digital twin. It does not use a black-box machine learning model or connect to physical aircraft engine hardware.

---

## 🗂️ Project Structure

```text
AeroGuard-AI/
│
├── app.py                  # Main Streamlit application with interactive command dashboard & all 12 modules
├── digital_twin.py         # Analytical Digital Twin models & component health matrix
├── engine_simulator.py     # Aero engine telemetry simulation engine
├── test_aeroguard.py       # Comprehensive 30-test automated verification suite
├── requirements.txt        # Project Python dependencies
├── README.md               # Complete project documentation & guide
└── .gitignore              # Git ignore rules for clean repository state
```

---

## ⚙️ How It Works

```text
    Simulated Engine Sensor Data (NumPy)
                   ↓
            Data Collection
                   ↓
            Data Processing
                   ↓
       Virtual CAD Engine Model
                   ↓
         Fault Detection System
                   ↓
        ┌──────────┴──────────┐
        ↓                     ↓
Engine Health Analysis   Mission Reliability Analysis
 (Current Condition)        (Endurance Forecast)
        └──────────┬──────────┘
                   ↓
          Explainable Alerts
                   ↓
     Maintenance Recommendations
                   ↓
   Interactive Dashboard & CSV Export
```

### Sensor Parameters

The system monitors four core engine parameters:

| Parameter | Nominal Range | Warning Limit | Purpose |
| :--- | :---: | :---: | :--- |
| **Engine Temperature** | 70°C – 105°C | > 110°C | Monitors engine operating temperature & cooling efficiency |
| **Oil Pressure** | 45 – 75 PSI | < 30 PSI | Monitors engine lubrication system pressure |
| **Vibration** | 1.0 – 5.0 / 10 | > 7.0 / 10 | Identifies abnormal engine & airframe vibration |
| **RPM** | 2200 – 4800 RPM | > 5000 RPM | Monitors engine rotational speed against approved envelope |

---

## 🧪 Fault Injection Scenarios

The Fault Injection Panel allows users to test how the application responds to different simulated abnormalities:

| Fault Type | Simulated Condition | Detection Logic | Description |
| :--- | :--- | :--- | :--- |
| **Spark Plug Misfire** | Vibration spikes to 8.2/10, RPM drops to 2600 | Vibration > 7.0 | Simulates improper ignition of the fuel-air mixture. |
| **Oil Pressure Drop** | Oil pressure drops to 18.0 PSI | Oil Pressure < 30 PSI | Simulates a decrease in engine oil lubrication pressure. |
| **Engine Overheating** | Temperature rises to 128.0°C | Temperature > 110°C | Simulates an abnormal increase in engine temperature. |
| **Abnormal Engine Vibration** | Vibration elevates to 9.1/10 | Vibration > 7.0 | Simulates unusual engine structural vibration. |
| **High RPM** | Engine speed reaches 5450 RPM | RPM > 5000 | Simulates engine speed exceeding approved limits. |
| **Sensor Failure** | Out-of-range reading (`ERR_OOR`) | Validity Range Check | Simulates missing, invalid or disconnected sensor telemetry. |

---

## 🧠 Engine Health & Reliability Analysis

### 1. Engine Health Score (0–100 pts)
The demonstration scoring system starts with 100 points and deducts penalties for abnormal readings:
* **75–100 pts:** `HEALTHY` (All parameters within safe envelope)
* **50–74 pts:** `WARNING` (One or more parameter threshold breaches)
* **Below 50 pts:** `CRITICAL` (Severe or multiple concurrent abnormalities)

### 2. Mission Reliability Score (0–100%)
The mission reliability module separately evaluates four weighted factors:
1. **Lubrication Reliability (35% weight)**
2. **Thermal Endurance (25% weight)**
3. **Structural / Vibration (25% weight)**
4. **Powertrain Speed (15% weight)**

Condition brackets:
* **75–100%:** `GOOD CONDITION`
* **40–74%:** `CAUTION`
* **Below 40%:** `HIGH RISK`

*These scores are illustrative indicators and are not validated predictions of actual aircraft engine reliability or mission success.*

---

## 🚀 Installation & Running

### Prerequisites
* Python 3.10 or above
* pip
* Git

### Step-by-Step Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/BhanuGowda05/AeroGuard-AI.git
   cd AeroGuard-AI
   ```

2. **Create a virtual environment**
   * Windows:
     ```bash
     python -m venv venv
     venv\Scripts\activate
     ```
   * macOS / Linux:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Install dependencies**
   ```bash
   python -m pip install -r requirements.txt
   ```

4. **Run the automated test suite (optional but recommended)**
   ```bash
   python test_aeroguard.py
   ```

5. **Run the application**
   ```bash
   streamlit run app.py
   ```

The application will open automatically at:  
👉 **`http://localhost:8501`**

---

## 💻 How to Use

* **Step 1 – Open the Dashboard:** Launch AeroGuard AI and explore the command center on `1. Home Dashboard`.
* **Step 2 – Monitor Engine Parameters:** View temperature, oil pressure, vibration and RPM via capsule gauges and circular dials.
* **Step 3 – Select Sensor Readings:** Choose predefined `Healthy`, `Warning` or `Critical` presets, or adjust sliders in `Manual Input` mode.
* **Step 4 – Simulate Engine Faults:** Navigate to `6. Fault Injection Panel`, select a fault from the dropdown, and click **Start Fault Simulation**.
* **Step 5 – Analyse Engine Health:** Observe the instantaneous Engine Health Score and forward-looking Mission Reliability indicator.
* **Step 6 – View Explainable Alerts:** Check `8. Explainable Alerts with Suggestions` for plain-language root causes and maintenance inspection actions.
* **Step 7 – Analyse Historical Trends:** Explore `9. Historical Sensor Analysis` to inspect parameter trend lines and directional indicators.
* **Step 8 – Export CSV Reports:** Go to `11. Reports and CSV Download` to download a complete monitoring report.

---

## 🔮 Future Enhancements

* Real-time integration with physical engine sensors.
* Integration with UAV engine monitoring systems and telemetry (ARINC 429 / CAN / MAVLink).
* Machine learning-based fault prediction.
* Historical engine degradation analysis.
* Remaining Useful Life (RUL) estimation using Weibull models.
* Advanced physics-based digital twin modelling.
* Multi-engine monitoring for twin-propeller UAVs.
* Mission-condition-based engine performance analysis.
* Validated predictive maintenance models.

---

## 📚 Project Information

* **Project Name:** AeroGuard AI
* **Domain:** Artificial Intelligence / Aerospace / Digital Twin Technology
* **Application Area:** Aero Piston Engine Monitoring for MALE UAVs
* **Project Type:** AI in Defence Hackathon Prototype
* **Development Approach:** Software-Based Digital Twin Demonstrator

---

## 👩‍💻 Developed By

 **Bhanushree G**

 **Department:** Computer Science and Engineering – Data Science  
 **Institution:** Nagarjuna College of Engineering and Technology (NCET)

---

### 📄 Disclaimer
*AeroGuard AI is an educational and hackathon prototype using simulated engine data. Its scores, thresholds, fault simulations and maintenance suggestions are illustrative only. It is not an aviation-certified monitoring system and must not be used for real aircraft operational or maintenance decisions.*
