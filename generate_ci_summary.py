#!/usr/bin/env python3
"""
GitHub Actions Step Summary Generator for Possaku Maestro Automation.
Parses the generated Playwright-style HTML report and appends a structured markdown
summary to $GITHUB_STEP_SUMMARY.
"""

import os
import sys
import glob
import re

def parse_html_report(report_path):
    if not os.path.exists(report_path):
        return None

    with open(report_path, "r", encoding="utf-8") as f:
        html = f.read()

    # Extract metrics from pw-stat-card
    total_m = re.search(r'Total Test Cases</div>\s*<div class="pw-stat-val">(\d+)</div>', html)
    passed_m = re.search(r'Passed TCs</div>\s*<div class="pw-stat-val pass">(\d+)</div>', html)
    failed_m = re.search(r'Failed TCs</div>\s*<div class="pw-stat-val[^"]*">(\d+)</div>', html)
    pass_rate_m = re.search(r'TC Pass Rate</div>\s*<div class="pw-stat-val[^"]*">([^<]+)</div>', html)

    # Extract flow name and duration from metadata table if present
    duration_m = re.search(r'<td class="pw-meta-key">Duration</td><td class="pw-meta-val">([^<]+)</td>', html)
    flow_m = re.search(r'<td class="pw-meta-key">Flow Name</td><td class="pw-meta-val">([^<]+)</td>', html)

    total = int(total_m.group(1)) if total_m else 0
    passed = int(passed_m.group(1)) if passed_m else 0
    failed = int(failed_m.group(1)) if failed_m else 0
    pass_rate = pass_rate_m.group(1) if pass_rate_m else ("100%" if failed == 0 and total > 0 else "0%")
    duration = duration_m.group(1) if duration_m else "N/A"
    flow_name = flow_m.group(1) if flow_m else os.path.basename(report_path)

    return {
        "report_file": os.path.basename(report_path),
        "flow_name": flow_name,
        "total": total,
        "passed": passed,
        "failed": failed,
        "pass_rate": pass_rate,
        "duration": duration,
        "success": failed == 0 and total > 0
    }

def main():
    summary_file = os.environ.get("GITHUB_STEP_SUMMARY")
    report_target = sys.argv[1] if len(sys.argv) > 1 else None

    # Locate report
    if report_target and os.path.exists(report_target):
        report_path = report_target
    else:
        reports = glob.glob("reports/*.html")
        if not reports:
            print("No HTML reports found in reports/ directory.")
            return
        report_path = max(reports, key=os.path.getmtime)

    metrics = parse_html_report(report_path)
    if not metrics:
        print(f"Could not parse metrics from {report_path}")
        return

    status_icon = "🟢 **PASSED**" if metrics["success"] else "🔴 **FAILED**"
    badge_color = "success" if metrics["success"] else "critical"

    summary_md = f"""## 🎭 Maestro Test Execution Summary

| Metric | Result |
| :--- | :--- |
| **Status** | {status_icon} |
| **Target Flow** | `{metrics['flow_name']}` |
| **Report File** | `{metrics['report_file']}` |
| **Total Test Cases** | **{metrics['total']}** |
| **Passed** | **{metrics['passed']}** ✅ |
| **Failed** | **{metrics['failed']}** ❌ |
| **Pass Rate** | **{metrics['pass_rate']}** |
| **Execution Duration** | **{metrics['duration']}** ⏱️ |

---

### 📦 Playwright HTML Report & Artifacts
The full interactive Playwright-style HTML report has been uploaded to the **Workflow Artifacts** of this run:
- **Artifact Name:** `maestro-playwright-report`
- **Features Included:**
  - 🔍 Live interactive search and filter (`/`)
  - 📋 Step-by-step UI actions with masked passwords/PINs
  - 📸 Embedded Base64 screenshots with lightbox preview
  - ℹ️ Device metadata (Android 11, API 30, Package: `com.cloudiex.possaku`)

> *Download and open `{metrics['report_file']}` in any browser to inspect detailed flow execution.*
"""

    if summary_file:
        with open(summary_file, "a", encoding="utf-8") as f:
            f.write(summary_md + "\n")
        print(f"Appended CI summary to {summary_file}")
    else:
        print(summary_md)

if __name__ == "__main__":
    main()
