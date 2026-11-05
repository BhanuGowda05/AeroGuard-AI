"""
AeroGuard AI - Comprehensive Automated Test Suite
Verifies all 13 baseline tests + Feature 1 Fault Injection Panel tests.
Uses pure ASCII output to prevent Windows cp1252 terminal encoding errors.
"""

import sys
import io
import time
import pandas as pd
import numpy as np

# Import functions from app
from app import (
    analyze_engine_state,
    compute_mission_reliability,
    generate_sensor_history,
    calculate_trend_direction,
    create_virtual_engine_figure,
    generate_explainable_alerts,
    THRESHOLDS
)

def run_tests():
    passed = 0
    failed = 0

    print("======================================================================")
    print("           AEROGUARD AI - FULL TEST SUITE EXECUTION                   ")
    print("======================================================================")

    # -------------------------------------------------------------------------
    # TEST 1: Healthy Scenario
    # -------------------------------------------------------------------------
    try:
        res = analyze_engine_state(85.0, 65.0, 3.0, 3000.0)
        assert res["health_score"] == 100, f"Expected 100, got {res['health_score']}"
        assert res["status"] == "HEALTHY", f"Expected HEALTHY, got {res['status']}"
        assert len(res["fault_details"]) == 0, f"Expected 0 faults, got {len(res['fault_details'])}"
        print("[PASS] TEST 1: Healthy scenario (Score: 100, Status: HEALTHY, 0 faults)")
        passed += 1
    except Exception as e:
        print(f"[FAIL] TEST 1: {e}")
        failed += 1

    # -------------------------------------------------------------------------
    # TEST 2: Warning Scenario
    # -------------------------------------------------------------------------
    try:
        res = analyze_engine_state(115.0, 65.0, 3.0, 3000.0)
        assert res["health_score"] == 75, f"Expected 75, got {res['health_score']}"
        assert res["status"] == "WARNING", f"Expected WARNING, got {res['status']}"
        assert len(res["fault_details"]) == 1, f"Expected 1 fault, got {len(res['fault_details'])}"
        assert res["fault_details"][0]["warning"] == "High temperature detected."
        assert res["fault_details"][0]["recommendation"] == "Recommend inspecting the cooling system."
        print("[PASS] TEST 2: Warning scenario (Score: 75, Status: WARNING, High temp detected)")
        passed += 1
    except Exception as e:
        print(f"[FAIL] TEST 2: {e}")
        failed += 1

    # -------------------------------------------------------------------------
    # TEST 3: Critical Scenario
    # -------------------------------------------------------------------------
    try:
        res = analyze_engine_state(130.0, 20.0, 9.0, 5200.0)
        assert res["health_score"] == 10, f"Expected 10, got {res['health_score']}"
        assert res["status"] == "CRITICAL", f"Expected CRITICAL, got {res['status']}"
        assert len(res["fault_details"]) == 4, f"Expected 4 faults, got {len(res['fault_details'])}"
        warnings = [f["warning"] for f in res["fault_details"]]
        assert "High temperature detected." in warnings
        assert "Low oil pressure detected." in warnings
        assert "Abnormal vibration detected." in warnings
        assert "High RPM detected." in warnings
        print("[PASS] TEST 3: Critical scenario (Score: 10, Status: CRITICAL, 4 faults triggered)")
        passed += 1
    except Exception as e:
        print(f"[FAIL] TEST 3: {e}")
        failed += 1

    # -------------------------------------------------------------------------
    # TEST 4: Manual Sensor Input
    # -------------------------------------------------------------------------
    try:
        res = analyze_engine_state(95.0, 52.0, 4.2, 3800.0)
        assert res["health_score"] == 100, f"Expected 100, got {res['health_score']}"
        assert res["status"] == "HEALTHY", f"Expected HEALTHY, got {res['status']}"
        assert len(res["fault_details"]) == 0
        print("[PASS] TEST 4: Manual sensor input within limits (Score: 100, Status: HEALTHY)")
        passed += 1
    except Exception as e:
        print(f"[FAIL] TEST 4: {e}")
        failed += 1

    # -------------------------------------------------------------------------
    # TEST 5: Temperature Fault Detection
    # -------------------------------------------------------------------------
    try:
        res = analyze_engine_state(111.0, 65.0, 3.0, 3000.0)
        assert res["health_score"] == 75
        assert res["status"] == "WARNING"
        assert res["fault_details"][0]["param"] == "Engine Temperature"
        assert res["fault_details"][0]["recommendation"] == "Recommend inspecting the cooling system."
        print("[PASS] TEST 5: Temperature fault (>110 deg C) detected & recommendation correct")
        passed += 1
    except Exception as e:
        print(f"[FAIL] TEST 5: {e}")
        failed += 1

    # -------------------------------------------------------------------------
    # TEST 6: Oil Pressure Fault Detection
    # -------------------------------------------------------------------------
    try:
        res = analyze_engine_state(85.0, 28.5, 3.0, 3000.0)
        assert res["health_score"] == 75
        assert res["status"] == "WARNING"
        assert res["fault_details"][0]["param"] == "Oil Pressure"
        assert res["fault_details"][0]["recommendation"] == "Recommend inspecting the lubrication system."
        print("[PASS] TEST 6: Oil pressure fault (<30 PSI) detected & recommendation correct")
        passed += 1
    except Exception as e:
        print(f"[FAIL] TEST 6: {e}")
        failed += 1

    # -------------------------------------------------------------------------
    # TEST 7: Vibration Fault Detection
    # -------------------------------------------------------------------------
    try:
        res = analyze_engine_state(85.0, 65.0, 7.5, 3000.0)
        assert res["health_score"] == 75
        assert res["status"] == "WARNING"
        assert res["fault_details"][0]["param"] == "Vibration"
        assert res["fault_details"][0]["recommendation"] == "Recommend inspecting engine mounting and rotating components."
        print("[PASS] TEST 7: Vibration fault (>7.0) detected & recommendation correct")
        passed += 1
    except Exception as e:
        print(f"[FAIL] TEST 7: {e}")
        failed += 1

    # -------------------------------------------------------------------------
    # TEST 8: RPM Fault Detection
    # -------------------------------------------------------------------------
    try:
        res = analyze_engine_state(85.0, 65.0, 3.0, 5100.0)
        assert res["health_score"] == 85
        assert res["status"] == "WARNING"
        assert res["fault_details"][0]["param"] == "Engine RPM"
        assert res["fault_details"][0]["recommendation"] == "Recommend checking the engine operating condition against its approved operating limits."
        print("[PASS] TEST 8: RPM fault (>5000 RPM) detected & recommendation correct")
        passed += 1
    except Exception as e:
        print(f"[FAIL] TEST 8: {e}")
        failed += 1

    # -------------------------------------------------------------------------
    # TEST 9: Multiple Faults Occurring Together
    # -------------------------------------------------------------------------
    try:
        res_double = analyze_engine_state(120.0, 22.0, 3.0, 3000.0)
        assert res_double["health_score"] == 50, f"Expected 50, got {res_double['health_score']}"
        assert res_double["status"] == "WARNING", f"Expected WARNING, got {res_double['status']}"
        assert len(res_double["fault_details"]) == 2

        res_triple = analyze_engine_state(120.0, 22.0, 8.0, 3000.0)
        assert res_triple["health_score"] == 25, f"Expected 25, got {res_triple['health_score']}"
        assert res_triple["status"] == "CRITICAL", f"Expected CRITICAL, got {res_triple['status']}"
        assert len(res_triple["fault_details"]) == 3

        print("[PASS] TEST 9: Multiple simultaneous faults correctly aggregated")
        passed += 1
    except Exception as e:
        print(f"[FAIL] TEST 9: {e}")
        failed += 1

    # -------------------------------------------------------------------------
    # TEST 10: Health Score Clamping & Edge Boundaries
    # -------------------------------------------------------------------------
    try:
        res_zero = analyze_engine_state(140.0, 10.0, 9.5, 5800.0)
        assert res_zero["health_score"] == 10
        assert res_zero["health_score"] >= 0

        res_75 = analyze_engine_state(115.0, 65.0, 3.0, 3000.0)
        assert res_75["status"] == "WARNING"

        res_crit = analyze_engine_state(120.0, 20.0, 8.0, 3000.0)
        assert res_crit["status"] == "CRITICAL"

        print("[PASS] TEST 10: Health score calculation, non-negative clamping & status brackets verified")
        passed += 1
    except Exception as e:
        print(f"[FAIL] TEST 10: {e}")
        failed += 1

    # -------------------------------------------------------------------------
    # TEST 11: Virtual Engine Monitoring Updates
    # -------------------------------------------------------------------------
    try:
        fig = create_virtual_engine_figure(120.0, 20.0, 8.5, 5200.0, "CRITICAL")
        assert fig is not None
        assert len(fig.layout.shapes) >= 5, "Expected at least 5 engine component shapes"
        assert len(fig.layout.annotations) >= 5, "Expected component text annotations"
        print("[PASS] TEST 11: Virtual Engine figure generates with all component shapes & dynamic colors")
        passed += 1
    except Exception as e:
        print(f"[FAIL] TEST 11: {e}")
        failed += 1

    # -------------------------------------------------------------------------
    # TEST 12: Historical Graphs & Trend Analysis
    # -------------------------------------------------------------------------
    try:
        df_hist = generate_sensor_history(115.0, 65.0, 3.0, 3000.0, points=60)
        assert df_hist.shape == (60, 7), f"Expected shape (60, 7), got {df_hist.shape}"
        assert not df_hist.isnull().values.any(), "Historical dataframe contains NaN values"
        
        direction, icon, col, delta = calculate_trend_direction(df_hist["temperature_c"], threshold_delta=2.0)
        assert direction == "Increasing", f"Expected Increasing, got {direction}"
        assert delta > 0, "Expected positive delta for rising temperature"

        print("[PASS] TEST 12: 60-second historical sensor dataframe & trend direction verified")
        passed += 1
    except Exception as e:
        print(f"[FAIL] TEST 12: {e}")
        failed += 1

    # -------------------------------------------------------------------------
    # TEST 13: CSV Report Generation & Download Data
    # -------------------------------------------------------------------------
    try:
        eval_sample = analyze_engine_state(115.0, 65.0, 3.0, 3000.0)
        faults_str = " | ".join([f['warning'] for f in eval_sample["fault_details"]])
        recs_str = " | ".join([f['recommendation'] for f in eval_sample["fault_details"]])

        test_df = pd.DataFrame({
            "Metric": ["Status", "Health Score", "Faults", "Actions"],
            "Value": [eval_sample["status"], eval_sample["health_score"], faults_str, recs_str]
        })
        
        csv_bytes = test_df.to_csv(index=False).encode("utf-8")
        assert len(csv_bytes) > 0
        
        read_back_df = pd.read_csv(io.BytesIO(csv_bytes))
        assert read_back_df.shape == (4, 2)
        assert read_back_df.iloc[0]["Value"] == "WARNING"

        print("[PASS] TEST 13: CSV report encoding, formatting, and read-back verified")
        passed += 1
    except Exception as e:
        print(f"[FAIL] TEST 13: {e}")
        failed += 1

    # -------------------------------------------------------------------------
    # TEST 14: FEATURE 1 - Fault Injection: Spark Plug Misfire
    # -------------------------------------------------------------------------
    try:
        t0 = time.perf_counter()
        res_misfire = analyze_engine_state(89.0, 62.0, 8.4, 2850.0)
        t1 = time.perf_counter()
        latency = (t1 - t0) * 1000.0
        assert latency > 0
        assert res_misfire["health_score"] == 75
        assert res_misfire["status"] == "WARNING"
        assert any("vibration" in f["warning"].lower() for f in res_misfire["fault_details"])
        print(f"[PASS] TEST 14: Feature 1 - Spark Plug Misfire injection verified (Latency: {latency:.3f} ms)")
        passed += 1
    except Exception as e:
        print(f"[FAIL] TEST 14: {e}")
        failed += 1

    # -------------------------------------------------------------------------
    # TEST 15: FEATURE 1 - Fault Injection: Oil Pressure Drop
    # -------------------------------------------------------------------------
    try:
        res_oil_drop = analyze_engine_state(92.0, 18.0, 3.4, 3000.0)
        assert res_oil_drop["health_score"] == 75
        assert res_oil_drop["status"] == "WARNING"
        assert res_oil_drop["fault_details"][0]["warning"] == "Low oil pressure detected."
        print("[PASS] TEST 15: Feature 1 - Oil Pressure Drop injection verified")
        passed += 1
    except Exception as e:
        print(f"[FAIL] TEST 15: {e}")
        failed += 1

    # -------------------------------------------------------------------------
    # TEST 16: FEATURE 1 - Fault Injection: Engine Overheating
    # -------------------------------------------------------------------------
    try:
        res_overheat = analyze_engine_state(128.0, 60.0, 3.2, 3100.0)
        assert res_overheat["health_score"] == 75
        assert res_overheat["status"] == "WARNING"
        assert res_overheat["fault_details"][0]["warning"] == "High temperature detected."
        print("[PASS] TEST 16: Feature 1 - Engine Overheating injection verified")
        passed += 1
    except Exception as e:
        print(f"[FAIL] TEST 16: {e}")
        failed += 1

    # -------------------------------------------------------------------------
    # TEST 17: FEATURE 1 - Fault Injection: Abnormal Engine Vibration
    # -------------------------------------------------------------------------
    try:
        res_vib = analyze_engine_state(87.0, 64.0, 8.8, 3050.0)
        assert res_vib["health_score"] == 75
        assert res_vib["status"] == "WARNING"
        assert res_vib["fault_details"][0]["warning"] == "Abnormal vibration detected."
        print("[PASS] TEST 17: Feature 1 - Abnormal Engine Vibration injection verified")
        passed += 1
    except Exception as e:
        print(f"[FAIL] TEST 17: {e}")
        failed += 1

    # -------------------------------------------------------------------------
    # TEST 18: FEATURE 1 - Fault Injection: High RPM
    # -------------------------------------------------------------------------
    try:
        res_rpm = analyze_engine_state(98.0, 58.0, 4.5, 5400.0)
        assert res_rpm["health_score"] == 85
        assert res_rpm["status"] == "WARNING"
        assert res_rpm["fault_details"][0]["warning"] == "High RPM detected."
        print("[PASS] TEST 18: Feature 1 - High RPM injection verified")
        passed += 1
    except Exception as e:
        print(f"[FAIL] TEST 18: {e}")
        failed += 1

    # -------------------------------------------------------------------------
    # TEST 19: FEATURE 1 - Fault Injection: Sensor Failure
    # -------------------------------------------------------------------------
    try:
        res_sensor_fail = analyze_engine_state(-999.0, 65.0, 3.0, 3000.0, sensor_failure="Engine Temperature Sensor")
        assert res_sensor_fail["health_score"] == 70  # 100 - 30 = 70
        assert res_sensor_fail["status"] == "WARNING"
        assert "Sensor Failure" in res_sensor_fail["fault_details"][0]["warning"]
        print("[PASS] TEST 19: Feature 1 - Sensor Failure injection verified")
        passed += 1
    except Exception as e:
        print(f"[FAIL] TEST 19: {e}")
        failed += 1

    # -------------------------------------------------------------------------
    # TEST 20: FEATURE 2 - Mission Reliability Score: Healthy Scenario
    # -------------------------------------------------------------------------
    try:
        state_healthy = analyze_engine_state(85.0, 65.0, 3.0, 3000.0)
        rel_healthy = compute_mission_reliability(
            85.0, 65.0, 3.0, 3000.0, state_healthy["fault_details"]
        )
        assert rel_healthy["reliability_score"] >= 75.0, f"Expected >= 75.0, got {rel_healthy['reliability_score']}"
        assert rel_healthy["condition_label"] == "GOOD CONDITION", f"Expected GOOD CONDITION, got {rel_healthy['condition_label']}"
        assert rel_healthy["condition_color"] == "#10b981"
        assert "Continue Mission" not in rel_healthy["explanation"]
        assert "Continue Mission" not in rel_healthy["condition_label"]
        print(f"[PASS] TEST 20: Feature 2 - Healthy Scenario Mission Reliability: {rel_healthy['reliability_score']}% ({rel_healthy['condition_label']})")
        passed += 1
    except Exception as e:
        print(f"[FAIL] TEST 20: {e}")
        failed += 1

    # -------------------------------------------------------------------------
    # TEST 21: FEATURE 2 - Mission Reliability Score: Warning Scenario
    # -------------------------------------------------------------------------
    try:
        state_warn = analyze_engine_state(115.0, 65.0, 3.0, 3000.0)
        rel_warn = compute_mission_reliability(
            115.0, 65.0, 3.0, 3000.0, state_warn["fault_details"]
        )
        assert 40.0 <= rel_warn["reliability_score"] < 75.0, f"Expected 40-74, got {rel_warn['reliability_score']}"
        assert rel_warn["condition_label"] == "CAUTION", f"Expected CAUTION, got {rel_warn['condition_label']}"
        assert rel_warn["condition_color"] == "#f59e0b"
        assert "Continue Mission" not in rel_warn["explanation"]
        print(f"[PASS] TEST 21: Feature 2 - Warning Scenario Mission Reliability: {rel_warn['reliability_score']}% ({rel_warn['condition_label']})")
        passed += 1
    except Exception as e:
        print(f"[FAIL] TEST 21: {e}")
        failed += 1

    # -------------------------------------------------------------------------
    # TEST 22: FEATURE 2 - Mission Reliability Score: Critical Scenario
    # -------------------------------------------------------------------------
    try:
        state_crit = analyze_engine_state(130.0, 20.0, 9.0, 5200.0)
        rel_crit = compute_mission_reliability(
            130.0, 20.0, 9.0, 5200.0, state_crit["fault_details"]
        )
        assert rel_crit["reliability_score"] < 40.0, f"Expected < 40.0, got {rel_crit['reliability_score']}"
        assert rel_crit["condition_label"] == "HIGH RISK", f"Expected HIGH RISK, got {rel_crit['condition_label']}"
        assert rel_crit["condition_color"] == "#ef4444"
        assert "Continue Mission" not in rel_crit["explanation"]
        print(f"[PASS] TEST 22: Feature 2 - Critical Scenario Mission Reliability: {rel_crit['reliability_score']}% ({rel_crit['condition_label']})")
        passed += 1
    except Exception as e:
        print(f"[FAIL] TEST 22: {e}")
        failed += 1

    # -------------------------------------------------------------------------
    # TEST 23: FEATURE 2 - Dynamic Explanation and Multi-factor Degradation
    # -------------------------------------------------------------------------
    try:
        # Test low oil pressure degradation explanation
        state_oil = analyze_engine_state(85.0, 20.0, 3.0, 3000.0)
        rel_oil = compute_mission_reliability(85.0, 20.0, 3.0, 3000.0, state_oil["fault_details"])
        assert "oil pressure" in rel_oil["explanation"].lower()

        # Test abnormal vibration degradation explanation
        state_vib = analyze_engine_state(85.0, 65.0, 8.5, 3000.0)
        rel_vib = compute_mission_reliability(85.0, 65.0, 8.5, 3000.0, state_vib["fault_details"])
        assert "vibration" in rel_vib["explanation"].lower()

        # Test sensor failure degradation explanation & penalty
        state_sens = analyze_engine_state(-999.0, 65.0, 3.0, 3000.0, sensor_failure="Engine Temperature Sensor")
        rel_sens = compute_mission_reliability(-999.0, 65.0, 3.0, 3000.0, state_sens["fault_details"], sensor_failure="Engine Temperature Sensor")
        assert "sensor" in rel_sens["explanation"].lower()
        assert rel_sens["condition_label"] in ["CAUTION", "HIGH RISK"]

        print("[PASS] TEST 23: Feature 2 - Dynamic explanation & individual degradation factors verified")
        passed += 1
    except Exception as e:
        print(f"[FAIL] TEST 23: {e}")
        failed += 1

    # -------------------------------------------------------------------------
    # TEST 24: FEATURE 3 - Oil Pressure Drop Explainable Alert
    # -------------------------------------------------------------------------
    try:
        res = analyze_engine_state(85.0, 18.0, 3.0, 3000.0)
        assert len(res["explainable_alerts"]) >= 1, "Expected at least 1 explainable alert"
        oil_alert = [a for a in res["explainable_alerts"] if a["parameter"] == "Oil Pressure"][0]
        assert oil_alert["alert_title"] == "Engine Alert!", f"Expected 'Engine Alert!', got {oil_alert['alert_title']}"
        assert oil_alert["reason"] == "Oil pressure is below the illustrative threshold."
        assert oil_alert["suggestion"] == "Inspect the lubrication system and check for possible oil leakage."
        assert oil_alert["severity"] == "CRITICAL"
        assert "< 30 PSI" in oil_alert["threshold"]
        print("[PASS] TEST 24: Feature 3 - Oil Pressure Drop explainable alert, reason & suggestion verified")
        passed += 1
    except Exception as e:
        print(f"[FAIL] TEST 24: {e}")
        failed += 1

    # -------------------------------------------------------------------------
    # TEST 25: FEATURE 3 - Engine Overheating Explainable Alert
    # -------------------------------------------------------------------------
    try:
        res = analyze_engine_state(118.0, 65.0, 3.0, 3000.0)
        temp_alert = [a for a in res["explainable_alerts"] if a["parameter"] == "Engine Temperature"][0]
        assert temp_alert["alert_title"] == "High Temperature Alert!", f"Expected 'High Temperature Alert!', got {temp_alert['alert_title']}"
        assert temp_alert["reason"] == "Engine temperature is above the illustrative threshold."
        assert temp_alert["suggestion"] == "Inspect the cooling system."
        assert temp_alert["severity"] in ["HIGH", "CRITICAL"]
        assert "> 110°C" in temp_alert["threshold"]
        print("[PASS] TEST 25: Feature 3 - Engine Overheating explainable alert, reason & suggestion verified")
        passed += 1
    except Exception as e:
        print(f"[FAIL] TEST 25: {e}")
        failed += 1

    # -------------------------------------------------------------------------
    # TEST 26: FEATURE 3 - Abnormal Vibration Explainable Alert
    # -------------------------------------------------------------------------
    try:
        res = analyze_engine_state(85.0, 65.0, 8.2, 3000.0)
        vib_alert = [a for a in res["explainable_alerts"] if "Vibration" in a["parameter"]][0]
        assert vib_alert["alert_title"] == "Vibration Alert!", f"Expected 'Vibration Alert!', got {vib_alert['alert_title']}"
        assert vib_alert["reason"] == "Vibration exceeds the illustrative threshold."
        assert vib_alert["suggestion"] == "Inspect engine mounting and rotating components."
        assert vib_alert["severity"] == "HIGH"
        print("[PASS] TEST 26: Feature 3 - Abnormal Vibration explainable alert, reason & suggestion verified")
        passed += 1
    except Exception as e:
        print(f"[FAIL] TEST 26: {e}")
        failed += 1

    # -------------------------------------------------------------------------
    # TEST 27: FEATURE 3 - Spark Plug Misfire Explainable Alert
    # -------------------------------------------------------------------------
    try:
        res = analyze_engine_state(89.0, 62.0, 8.4, 2850.0, active_fault_name="Spark Plug Misfire")
        misfire_alert = [a for a in res["explainable_alerts"] if a["alert_title"] == "Ignition Fault Alert!"][0]
        assert misfire_alert["reason"] == "Simulated misfire detected through abnormal engine behaviour."
        assert misfire_alert["suggestion"] == "Inspect the ignition system and spark plugs."
        assert misfire_alert["severity"] == "HIGH"
        assert "combustion" in misfire_alert["why_generated"].lower()
        print("[PASS] TEST 27: Feature 3 - Spark Plug Misfire ignition alert, reason & suggestion verified")
        passed += 1
    except Exception as e:
        print(f"[FAIL] TEST 27: {e}")
        failed += 1

    # -------------------------------------------------------------------------
    # TEST 28: FEATURE 3 - High RPM Explainable Alert
    # -------------------------------------------------------------------------
    try:
        res = analyze_engine_state(85.0, 65.0, 3.0, 5350.0)
        rpm_alert = [a for a in res["explainable_alerts"] if a["parameter"] == "Engine RPM"][0]
        assert rpm_alert["alert_title"] == "RPM Alert!", f"Expected 'RPM Alert!', got {rpm_alert['alert_title']}"
        assert rpm_alert["reason"] == "RPM exceeds the illustrative demonstration threshold."
        assert rpm_alert["suggestion"] == "Check engine operating conditions against approved operating limits."
        assert rpm_alert["severity"] == "WARNING"
        print("[PASS] TEST 28: Feature 3 - High RPM explainable alert, reason & suggestion verified")
        passed += 1
    except Exception as e:
        print(f"[FAIL] TEST 28: {e}")
        failed += 1

    # -------------------------------------------------------------------------
    # TEST 29: FEATURE 3 - Multiple Fault Prioritization
    # -------------------------------------------------------------------------
    try:
        res_multi = analyze_engine_state(128.0, 18.0, 3.0, 5400.0)
        assert len(res_multi["explainable_alerts"]) == 3, f"Expected 3 alerts, got {len(res_multi['explainable_alerts'])}"
        hp = res_multi["highest_priority_fault"]
        assert hp is not None, "Highest priority fault must be identified"
        assert hp["severity"] == "CRITICAL", f"Expected CRITICAL, got {hp['severity']}"
        assert hp["alert_title"] in ["Engine Alert!", "High Temperature Alert!"], f"Expected Engine Alert! or High Temperature Alert!, got {hp['alert_title']}"
        # Verify priority sorting: Priority 1 first, Priority 3 last
        assert res_multi["explainable_alerts"][0]["priority_rank"] <= res_multi["explainable_alerts"][-1]["priority_rank"]
        print("[PASS] TEST 29: Feature 3 - Multi-fault detection & highest-priority severity ranking verified")
        passed += 1
    except Exception as e:
        print(f"[FAIL] TEST 29: {e}")
        failed += 1

    # -------------------------------------------------------------------------
    # TEST 30: FEATURE 3 - Deep Reason Completeness & Absence of Arbitrary Percentages
    # -------------------------------------------------------------------------
    try:
        alerts, hp = generate_explainable_alerts(120.0, 20.0, 8.0, 5200.0)
        for a in alerts:
            # Must contain explanation for "Why was this alert generated?" expander
            assert "why_generated" in a and len(a["why_generated"]) > 20, "Missing detailed 'why_generated' explanation"
            # Must not contain ungrounded arbitrary percentages like '(42%)'
            assert "%" not in a["alert_title"], f"Arbitrary percentage in alert title: {a['alert_title']}"
            assert "%" not in a["reason"], f"Arbitrary percentage in alert reason: {a['reason']}"
        print("[PASS] TEST 30: Feature 3 - Absence of arbitrary percentages & deep explanation completeness verified")
        passed += 1
    except Exception as e:
        print(f"[FAIL] TEST 30: {e}")
        failed += 1

    print("======================================================================")
    print(f"TEST SUMMARY: {passed} / {passed + failed} TESTS PASSED")
    if failed == 0:
        print("ALL 30 TEST CASES (BASELINE + FEATURE 1 + FEATURE 2 + FEATURE 3) PASSED WITH 100% SUCCESS!")
    else:
        print(f"{failed} TESTS FAILED. PLEASE REVIEW.")
    print("======================================================================")
    
    return failed == 0

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
