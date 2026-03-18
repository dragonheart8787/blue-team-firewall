#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Release 治理 - 將冗餘/迭代檔案移至 archive，根目錄只保留 release 必要檔案
執行後 archive/ 加入 .gitignore，不納入版本控制
"""

import shutil
from pathlib import Path

ROOT = Path(__file__).parent.parent
ARCHIVE = ROOT / "archive"

# 移至 archive：冗餘變體（保留一個 canonical）
ARCHIVE_PATTERNS = {
    "waf_proxy": ["waf_proxy_fixed.py", "waf_proxy_minimal.py", "waf_proxy_stable.py",
                  "waf_proxy_debug.py", "waf_proxy_final_fixed.py", "waf_proxy_simple_stable.py",
                  "waf_proxy_ultimate.py", "waf_proxy_enterprise_fixed.py", "waf_proxy_ultra_performance.py",
                  "waf_proxy_rock_solid.py", "waf_proxy_final_solution.py"],
    "test_variants": ["test_minimal.py", "test_rock_solid.py", "test_simple_stable.py", "test_stable_system.py",
                      "test_final_fixed.py", "test_final_solution.py", "test_fixed_system.py",
                      "test_ultimate_system.py", "test_waf_direct.py", "test_waf_debug.py", "test_quick.py"],
    "demo": ["demo_enterprise_features.py", "demo_military_firewall.py", "demo_protection.py",
             "demo_real_capabilities.py", "demo_ultimate_firewall.py"],
    "legacy": ["final_improved_test.py", "final_ultra_test.py", "ultra_enhanced_test.py",
               "final_improvement_summary.py", "diagnose_issues.py", "debug_waf.py",
               "debug_waf_detailed.py", "debug_waf_rules.py"],
}

# 模組變體：以 prefix 批量移至 archive
ARCHIVE_PREFIXES = ["military_", "real_"]

# 移至 tests/
TEST_FILES = [
    "test_nosql_injection.py", "test_sql_injection.py", "test_user_login.py",
    "test_regex.py", "test_admin_pattern.py", "test_waf_rules.py", "test_waf_stress.py",
    "test_enterprise_features.py", "test_edr_mimikatz.py", "test_crto2_c2_beaconing.py",
    "test_crto2_pass_the_hash.py", "test_crto2_golden_ticket.py", "test_atomic_t1078_cloud_logon.py",
    "test_atomic_t1610_container_escape.py", "test_attack_chain.py", "test_atomic_t1021_002.py",
    "test_atomic_t1053_005.py", "test_atomic_t1486.py", "test_atomic_t1566_001.py",
    "test_atomic_t1003_001.py", "test_atomic_t1071_001.py", "test_atomic_t1059_003.py",
    "test_complete_system.py", "test_ctf_system.py", "test_waf.py", "test_system_quick.py",
    "test_compliance_frameworks.py", "test_medium_priority_modules.py", "test_high_priority_modules.py",
    "test_basic_functions.py", "test_all_functions.py", "test_military_system.py", "test_system.py",
]

# 根目錄保留的核心（不移動）
KEEP_IN_ROOT = {
    "national_defense_firewall.py", "kill_chain_detector.py", "mitre_attack_mapper.py",
    "memory_forensics_module.py", "pcap_analysis_module.py", "evidence_chain_system.py",
    "soar_playbooks.py", "cti_integration_engine.py", "ml_anomaly_detector.py",
    "national_defense_grade_test.py", "test_all_firewall_capabilities.py",
    "run_benchmarks.py", "main.py", "central_server.py", "secure_web_system.py",
    "waf_proxy.py", "target_app.py",
    "windows_event_parser.py", "ad_attack_path_detector.py", "kerberos_anomaly_detector.py",
    "privileged_group_monitor.py",
    "standalone_certification_tests.py", "evidence_verification_system.py",
}


def main():
    ARCHIVE.mkdir(exist_ok=True)
    for sub in ["waf_variants", "test_variants", "demo", "legacy"]:
        (ARCHIVE / sub).mkdir(exist_ok=True)

    moved_archive = 0
    moved_tests = 0

    # 1. 移至 archive
    subdirs = {"waf_proxy": "waf_variants", "test_variants": "test_variants", "demo": "demo", "legacy": "legacy"}
    (ARCHIVE / "modules").mkdir(exist_ok=True)
    for category, files in ARCHIVE_PATTERNS.items():
        subdir = ARCHIVE / subdirs.get(category, "legacy")
        subdir.mkdir(exist_ok=True)
        for f in files:
            src = ROOT / f
            if src.exists():
                shutil.move(str(src), str(subdir / f))
                moved_archive += 1
                print(f"  archive/ {f}")

    # 2. 批量移至 archive (military_*, real_*)
    for prefix in ARCHIVE_PREFIXES:
        subdir = ARCHIVE / "modules"
        subdir.mkdir(exist_ok=True)
        for f in ROOT.glob(f"{prefix}*.py"):
            if f.is_file():
                shutil.move(str(f), str(subdir / f.name))
                moved_archive += 1
                print(f"  archive/modules/ {f.name}")

    # 3. 移至 tests/
    for f in TEST_FILES:
        src = ROOT / f
        if src.exists():
            dest = ROOT / "tests" / f
            if not dest.exists():
                shutil.move(str(src), str(dest))
                moved_tests += 1
                print(f"  tests/ {f}")

    print(f"\nMoved: archive={moved_archive}, tests={moved_tests}")


if __name__ == "__main__":
    main()
