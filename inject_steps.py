import re
import sys
import os
import glob
import json
import html as html_lib
import argparse
import base64


def esc(val):
    return html_lib.escape(str(val or ""))


def extract_selector_target(sel):
    if not isinstance(sel, dict):
        return "element"
    return (
        sel.get("textRegex")
        or sel.get("text")
        or sel.get("idRegex")
        or sel.get("id")
        or sel.get("below", {}).get("textRegex")
        or sel.get("below", {}).get("text")
        or "element"
    )


def format_command(cmd, eval_cmd=None):
    if not cmd:
        return "Unknown action", ""

    cmd_type = list(cmd.keys())[0]
    details = cmd[cmd_type] or {}
    eval_details = eval_cmd.get(cmd_type, {}) if eval_cmd and cmd_type in eval_cmd else details

    if cmd_type == "launchAppCommand":
        app_id = eval_details.get("appId") or details.get("appId", "app")
        clear = " (clearState=true)" if eval_details.get("clearState", False) else ""
        return "launchApp", f"<code>{esc(app_id)}</code>{clear}"

    elif cmd_type == "tapOnElement":
        selector = eval_details.get("selector", {}) or details.get("selector", {})
        target = extract_selector_target(selector)
        opt = " <span class='pw-tag' style='color:#64748b;'>optional</span>" if details.get("optional") or selector.get("optional") else ""
        return "tap", f"Target: <b>{esc(target)}</b>{opt}"

    elif cmd_type == "tapOnPointV2Command":
        point = eval_details.get("point") or details.get("point")
        return "tapPoint", f"Coordinates: <code>{esc(point)}</code>"

    elif cmd_type == "inputTextCommand":
        text = str(eval_details.get("text", ""))
        masked = "******" if (text.isdigit() and len(text) in (6, 4)) else text
        return "fill", f"Value: <code>{esc(masked)}</code>"

    elif cmd_type == "runScriptCommand":
        source = details.get("sourceDescription") or "inline script"
        return "runScript", f"<code>{esc(source)}</code>"

    elif cmd_type == "evalScriptCommand":
        script = eval_details.get("scriptString") or details.get("scriptString", "")
        return "evalScript", f"<code>{esc(script)}</code>"

    elif cmd_type == "copyTextFromCommand":
        selector = eval_details.get("selector", {}) or details.get("selector", {})
        target = extract_selector_target(selector)
        return "copyText", f"From: <b>{esc(target)}</b>"

    elif cmd_type == "assertConditionCommand":
        cond = eval_details.get("condition", {}) or details.get("condition", {})
        if "visible" in cond:
            target = extract_selector_target(cond["visible"])
            return "expectVisible", f"Element: <b>{esc(target)}</b>"
        elif "notVisible" in cond:
            target = extract_selector_target(cond["notVisible"])
            return "expectNotVisible", f"Element: <b>{esc(target)}</b>"
        elif "evaluate" in cond or "scriptCondition" in cond:
            expr = cond.get("evaluate") or cond.get("scriptCondition")
            return "expectTrue", f"<code>{esc(expr)}</code>"
        return "expectCondition", "Custom condition"

    elif cmd_type == "scrollUntilVisibleCommand":
        selector = eval_details.get("selector", {}) or details.get("selector", {})
        target = extract_selector_target(selector)
        direction = details.get("direction", "DOWN")
        return "scrollUntilVisible", f"Element: <b>{esc(target)}</b> ({esc(direction)})"

    elif cmd_type == "waitUntilCommand":
        cond = eval_details.get("condition", {}) or details.get("condition", {})
        target = extract_selector_target(cond.get("visible") or cond.get("notVisible") or {})
        return "waitFor", f"Element: <b>{esc(target)}</b>"

    elif cmd_type == "pressKeyCommand":
        code = eval_details.get("code") or details.get("code")
        return "pressKey", f"Key: <code>{esc(code)}</code>"

    elif cmd_type == "hideKeyboardCommand":
        return "hideKeyboard", "Dismiss Soft IME"

    elif cmd_type == "toggleAirplaneModeCommand":
        return "toggleAirplaneMode", "Network connectivity toggled"

    elif cmd_type == "runFlowCommand":
        flow_file = details.get("sourceDescription") or details.get("file") or "sub-flow"
        label = details.get("label", "")
        label_html = f" - <b>{esc(label)}</b>" if label else ""
        return "runFlow", f"File: <code>{esc(flow_file)}</code>{label_html}"

    elif cmd_type == "backCommand":
        return "goBack", "Android Back Navigation"

    elif cmd_type == "scrollCommand":
        return "scroll", "Vertical Scroll"

    elif cmd_type == "swipeCommand":
        start = details.get("start", "")
        end = details.get("end", "")
        return "swipe", f"From <code>{esc(start)}</code> to <code>{esc(end)}</code>"

    elif cmd_type in ("defineVariablesCommand", "applyConfigurationCommand"):
        return cmd_type.replace("Command", ""), ""

    return cmd_type.replace("Command", ""), f"<small class='text-muted'>{esc(details)}</small>"


def format_duration(ms):
    if isinstance(ms, (int, float)):
        if ms < 1000:
            return f"{int(ms)}ms"
        sec = ms / 1000.0
        if sec >= 60:
            mins = int(sec // 60)
            rem = sec % 60
            return f"{mins}m {rem:.1f}s"
        return f"{sec:.2f}s"
    return str(ms or "0ms")


def find_commands_json(debug_dir, clean_flow_name):
    clean_target = clean_flow_name.lower().replace("-", "_")
    for root, dirs, files in os.walk(debug_dir):
        if "commands.json" in files:
            parent_dir = os.path.basename(root).lower().replace("-", "_")
            if clean_target in parent_dir or parent_dir in clean_target:
                return os.path.join(root, "commands.json")
        for f in files:
            if f.startswith("commands-") and f.endswith(".json"):
                f_clean = f.lower().replace("-", "_")
                if clean_target in f_clean:
                    return os.path.join(root, f)
    return None


def find_source_yaml(clean_flow_name):
    target = f"{clean_flow_name}.yaml"
    for root, dirs, files in os.walk("flows"):
        if target in files:
            return os.path.join(root, target)
        for f in files:
            if f.endswith(".yaml") and clean_flow_name in f:
                return os.path.join(root, f)
    return None


def parse_yaml_sections(yaml_path):
    if not yaml_path or not os.path.exists(yaml_path):
        return {}
    with open(yaml_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    past_header = not any(line.strip() == "---" for line in lines)
    cmd_index = 0
    cmd_to_comment = {}
    current_comment = None

    for line in lines:
        stripped = line.strip()
        if not past_header:
            if stripped == "---":
                past_header = True
            continue

        if not stripped:
            continue

        if stripped.startswith("#"):
            comment_text = stripped.lstrip("#").strip()
            if (
                re.match(r"^\[?[A-Z]+-\d+\]?", comment_text)
                or any(char.isdigit() for char in comment_text)
                or comment_text.lower().startswith(
                    ("setup", "[setup]", "step", "teardown", "[teardown]", "navigate", "add item", "open cart", "proceed")
                )
            ):
                current_comment = comment_text
        elif line.startswith("- "):
            if current_comment:
                cmd_to_comment[cmd_index] = current_comment
                current_comment = None
            cmd_index += 1

    return cmd_to_comment


def find_screenshots(commands_json_path):
    flow_dir = os.path.dirname(commands_json_path)
    screenshots_dir = os.path.join(flow_dir, "screenshots")
    if os.path.isdir(screenshots_dir):
        return sorted(glob.glob(os.path.join(screenshots_dir, "*.png")))
    return []


PLAYWRIGHT_HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Possaku Maestro • Playwright Test Report</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
  <style>
    :root {
      --pw-bg: #f8fafc;
      --pw-surface: #ffffff;
      --pw-header: #18181b;
      --pw-header-border: #27272a;
      --pw-border: #e2e8f0;
      --pw-border-subtle: #f1f5f9;
      --pw-text: #0f172a;
      --pw-text-muted: #64748b;
      --pw-text-subtle: #94a3b8;
      --pw-green: #10b981;
      --pw-green-bg: #ecfdf5;
      --pw-green-border: #a7f3d0;
      --pw-green-text: #065f46;
      --pw-red: #ef4444;
      --pw-red-bg: #fef2f2;
      --pw-red-border: #fecaca;
      --pw-red-text: #991b1b;
      --pw-blue: #3b82f6;
      --pw-blue-bg: #eff6ff;
      --pw-font-sans: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      --pw-font-mono: 'JetBrains Mono', ui-monospace, SFMono-Regular, Menlo, monospace;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: var(--pw-font-sans);
      background: var(--pw-bg);
      color: var(--pw-text);
      line-height: 1.5;
      -webkit-font-smoothing: antialiased;
    }
    
    .pw-navbar {
      background: var(--pw-header);
      color: #fff;
      border-bottom: 1px solid var(--pw-header-border);
      padding: 0.75rem 1.5rem;
      position: sticky;
      top: 0;
      z-index: 100;
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 1rem;
    }
    .pw-brand {
      display: flex;
      align-items: center;
      gap: 0.75rem;
    }
    .pw-logo-icon {
      width: 28px;
      height: 28px;
      background: linear-gradient(135deg, #10b981 0%, #059669 100%);
      border-radius: 6px;
      display: flex;
      align-items: center;
      justify-content: center;
      box-shadow: 0 2px 4px rgba(16, 185, 129, 0.3);
    }
    .pw-brand-title {
      font-weight: 700;
      font-size: 1.05rem;
      letter-spacing: -0.01em;
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }
    .pw-brand-badge {
      font-size: 0.7rem;
      font-weight: 600;
      text-transform: uppercase;
      padding: 0.15rem 0.5rem;
      border-radius: 9999px;
      background: rgba(255, 255, 255, 0.12);
      color: #e4e4e7;
    }
    .pw-nav-center {
      flex: 1;
      max-width: 480px;
      position: relative;
    }
    .pw-search-input {
      width: 100%;
      background: rgba(255, 255, 255, 0.08);
      border: 1px solid rgba(255, 255, 255, 0.15);
      border-radius: 6px;
      color: #fff;
      font-size: 0.85rem;
      padding: 0.45rem 2.2rem 0.45rem 0.75rem;
      outline: none;
      transition: all 0.15s ease;
      font-family: inherit;
    }
    .pw-search-input:focus {
      background: rgba(255, 255, 255, 0.14);
      border-color: var(--pw-green);
      box-shadow: 0 0 0 2px rgba(16, 185, 129, 0.25);
    }
    .pw-search-hint {
      position: absolute;
      right: 0.5rem;
      top: 50%;
      transform: translateY(-50%);
      font-size: 0.7rem;
      color: #a1a1aa;
      background: rgba(255, 255, 255, 0.1);
      padding: 0.1rem 0.35rem;
      border-radius: 4px;
      pointer-events: none;
    }
    .pw-nav-meta {
      display: flex;
      align-items: center;
      gap: 1.25rem;
      font-size: 0.85rem;
      color: #a1a1aa;
    }
    .pw-nav-chip {
      display: inline-flex;
      align-items: center;
      gap: 0.4rem;
    }
    
    .pw-container {
      max-width: 1300px;
      margin: 1.5rem auto;
      padding: 0 1.5rem;
    }
    
    .pw-dashboard {
      background: var(--pw-surface);
      border: 1px solid var(--pw-border);
      border-radius: 10px;
      padding: 1.25rem;
      margin-bottom: 1.5rem;
      box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
    }
    .pw-stats-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
      gap: 1rem;
      margin-bottom: 1rem;
    }
    .pw-stat-card {
      background: var(--pw-bg);
      border: 1px solid var(--pw-border);
      border-radius: 8px;
      padding: 0.85rem 1rem;
    }
    .pw-stat-label {
      font-size: 0.75rem;
      font-weight: 500;
      color: var(--pw-text-muted);
      text-transform: uppercase;
      letter-spacing: 0.03em;
      margin-bottom: 0.25rem;
    }
    .pw-stat-val {
      font-size: 1.4rem;
      font-weight: 700;
      color: var(--pw-text);
      display: flex;
      align-items: baseline;
      gap: 0.4rem;
    }
    .pw-stat-val.pass { color: var(--pw-green); }
    .pw-stat-val.fail { color: var(--pw-red); }
    .pw-progress-bar {
      height: 6px;
      border-radius: 3px;
      background: #e2e8f0;
      overflow: hidden;
      display: flex;
      margin-bottom: 1rem;
    }
    .pw-progress-fill {
      height: 100%;
      background: var(--pw-green);
      transition: width 0.3s ease;
    }
    
    .pw-filter-bar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 0.75rem;
      padding-top: 0.75rem;
      border-top: 1px solid var(--pw-border-subtle);
    }
    .pw-filter-tabs {
      display: flex;
      gap: 0.4rem;
    }
    .pw-filter-btn {
      background: transparent;
      border: 1px solid var(--pw-border);
      color: var(--pw-text-muted);
      font-size: 0.8rem;
      font-weight: 500;
      padding: 0.35rem 0.75rem;
      border-radius: 6px;
      cursor: pointer;
      transition: all 0.15s ease;
      display: flex;
      align-items: center;
      gap: 0.4rem;
      font-family: inherit;
    }
    .pw-filter-btn:hover {
      background: #f1f5f9;
      color: var(--pw-text);
    }
    .pw-filter-btn.active {
      background: var(--pw-header);
      color: #fff;
      border-color: var(--pw-header);
    }
    .pw-expand-toggles {
      display: flex;
      gap: 0.4rem;
    }
    .pw-btn-sm {
      background: transparent;
      border: 1px solid var(--pw-border);
      color: var(--pw-text-muted);
      font-size: 0.75rem;
      padding: 0.3rem 0.6rem;
      border-radius: 5px;
      cursor: pointer;
      font-family: inherit;
      transition: all 0.15s ease;
    }
    .pw-btn-sm:hover {
      background: #f1f5f9;
      color: var(--pw-text);
    }
    
    .pw-spec-card {
      background: var(--pw-surface);
      border: 1px solid var(--pw-border);
      border-radius: 8px;
      margin-bottom: 1rem;
      overflow: hidden;
      box-shadow: 0 1px 3px rgba(0, 0, 0, 0.03);
      transition: border-color 0.15s ease;
    }
    .pw-spec-header {
      padding: 0.85rem 1.25rem;
      background: var(--pw-surface);
      display: flex;
      justify-content: space-between;
      align-items: center;
      cursor: pointer;
      user-select: none;
      gap: 1rem;
    }
    .pw-spec-header:hover {
      background: #f8fafc;
    }
    .pw-spec-title-group {
      display: flex;
      align-items: center;
      gap: 0.6rem;
      flex: 1;
      overflow: hidden;
    }
    .pw-chevron {
      font-size: 1.1rem;
      color: var(--pw-text-muted);
      transition: transform 0.2s ease;
      display: inline-block;
      width: 14px;
      text-align: center;
    }
    .pw-spec-card.open .pw-spec-header .pw-chevron {
      transform: rotate(90deg);
    }
    .pw-file-icon {
      color: var(--pw-text-muted);
      flex-shrink: 0;
    }
    .pw-spec-name {
      font-family: var(--pw-font-mono);
      font-weight: 600;
      font-size: 0.9rem;
      color: var(--pw-text);
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }
    .pw-tags-list {
      display: flex;
      gap: 0.35rem;
      flex-wrap: wrap;
    }
    .pw-tag {
      font-size: 0.7rem;
      color: #475569;
      background: #f1f5f9;
      border: 1px solid #e2e8f0;
      padding: 0.1rem 0.45rem;
      border-radius: 4px;
      font-family: var(--pw-font-mono);
    }
    .pw-spec-meta-group {
      display: flex;
      align-items: center;
      gap: 0.85rem;
      flex-shrink: 0;
    }
    .pw-spec-dur {
      font-family: var(--pw-font-mono);
      font-size: 0.8rem;
      color: var(--pw-text-muted);
    }
    .pw-badge {
      display: inline-flex;
      align-items: center;
      gap: 0.35rem;
      font-size: 0.75rem;
      font-weight: 600;
      text-transform: uppercase;
      padding: 0.2rem 0.55rem;
      border-radius: 9999px;
    }
    .pw-badge-pass {
      background: var(--pw-green-bg);
      color: var(--pw-green-text);
      border: 1px solid var(--pw-green-border);
    }
    .pw-badge-fail {
      background: var(--pw-red-bg);
      color: var(--pw-red-text);
      border: 1px solid var(--pw-red-border);
    }
    
    .pw-spec-body {
      display: none;
      border-top: 1px solid var(--pw-border);
      background: #fff;
    }
    .pw-spec-card.open .pw-spec-body {
      display: block;
    }
    .pw-tabs-nav {
      display: flex;
      background: #f8fafc;
      border-bottom: 1px solid var(--pw-border);
      padding: 0 1rem;
    }
    .pw-tab-btn {
      background: transparent;
      border: none;
      border-bottom: 2px solid transparent;
      padding: 0.65rem 1rem;
      font-size: 0.8rem;
      font-weight: 600;
      color: var(--pw-text-muted);
      cursor: pointer;
      transition: all 0.15s ease;
      font-family: inherit;
    }
    .pw-tab-btn:hover {
      color: var(--pw-text);
    }
    .pw-tab-btn.active {
      color: var(--pw-blue);
      border-bottom-color: var(--pw-blue);
      background: #fff;
    }
    .pw-tab-pane {
      display: none;
      padding: 1.25rem;
    }
    .pw-tab-pane.active {
      display: block;
    }
    
    .pw-tc-card {
      border: 1px solid var(--pw-border);
      border-radius: 6px;
      margin-bottom: 0.75rem;
      overflow: hidden;
    }
    .pw-tc-header {
      background: #f8fafc;
      padding: 0.6rem 1rem;
      display: flex;
      align-items: center;
      gap: 0.6rem;
      cursor: pointer;
      user-select: none;
    }
    .pw-tc-header:hover {
      background: #f1f5f9;
    }
    .pw-tc-card.open .pw-tc-header .pw-chevron {
      transform: rotate(90deg);
    }
    .pw-status-icon {
      width: 18px;
      height: 18px;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      flex-shrink: 0;
    }
    .pw-status-icon.pass {
      background: var(--pw-green-bg);
      color: var(--pw-green);
    }
    .pw-status-icon.fail {
      background: var(--pw-red-bg);
      color: var(--pw-red);
    }
    .pw-tc-title {
      font-size: 0.85rem;
      font-weight: 600;
      color: var(--pw-text);
      flex: 1;
    }
    .pw-tc-dur {
      font-family: var(--pw-font-mono);
      font-size: 0.75rem;
      color: var(--pw-text-muted);
    }
    .pw-tc-body {
      display: none;
      border-top: 1px solid var(--pw-border);
    }
    .pw-tc-card.open .pw-tc-body {
      display: block;
    }
    
    .pw-steps-table {
      width: 100%;
      border-collapse: collapse;
      font-size: 0.8rem;
    }
    .pw-step-row:hover {
      background: #f8fafc;
    }
    .pw-step-row.pw-row-fail {
      background: var(--pw-red-bg);
    }
    .pw-steps-table td {
      padding: 0.45rem 0.75rem;
      border-bottom: 1px solid #f1f5f9;
      vertical-align: middle;
    }
    .pw-col-num {
      width: 40px;
      text-align: center;
      font-family: var(--pw-font-mono);
      color: var(--pw-text-subtle);
      font-size: 0.75rem;
    }
    .pw-col-icon {
      width: 30px;
      text-align: center;
    }
    .pw-step-icon.pass { color: var(--pw-green); font-weight: bold; }
    .pw-step-icon.fail { color: var(--pw-red); font-weight: bold; }
    .pw-col-action {
      width: 180px;
      font-weight: 600;
      color: #1e293b;
    }
    .pw-action-name {
      display: inline-block;
      background: #f1f5f9;
      border: 1px solid #e2e8f0;
      padding: 0.15rem 0.45rem;
      border-radius: 4px;
      font-family: var(--pw-font-mono);
      font-size: 0.75rem;
    }
    .pw-step-row.depth-1 td.pw-col-action { padding-left: 1.5rem; }
    .pw-step-row.depth-2 td.pw-col-action { padding-left: 2.25rem; }
    .pw-col-target {
      font-family: var(--pw-font-mono);
      font-size: 0.8rem;
      color: #334155;
    }
    .pw-col-target code {
      background: #f1f5f9;
      padding: 0.1rem 0.35rem;
      border-radius: 4px;
      border: 1px solid #e2e8f0;
      color: #0f172a;
    }
    .pw-col-dur {
      width: 80px;
      text-align: right;
      font-family: var(--pw-font-mono);
      color: var(--pw-text-muted);
      font-size: 0.75rem;
    }
    .pw-step-error {
      margin-top: 0.35rem;
      background: #fee2e2;
      border: 1px solid #fca5a5;
      padding: 0.4rem 0.6rem;
      border-radius: 4px;
      color: #991b1b;
      font-size: 0.75rem;
    }
    
    .pw-gallery-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
      gap: 1rem;
    }
    .pw-gallery-item {
      background: #fff;
      border: 1px solid var(--pw-border);
      border-radius: 6px;
      overflow: hidden;
      cursor: pointer;
      transition: all 0.15s ease;
    }
    .pw-gallery-item:hover {
      transform: translateY(-2px);
      box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
      border-color: var(--pw-blue);
    }
    .pw-gallery-thumb {
      height: 220px;
      background: #18181b;
      display: flex;
      align-items: center;
      justify-content: center;
      position: relative;
    }
    .pw-gallery-thumb img {
      max-height: 100%;
      max-width: 100%;
      object-fit: contain;
    }
    .pw-gallery-overlay {
      position: absolute;
      inset: 0;
      background: rgba(0, 0, 0, 0.4);
      display: flex;
      align-items: center;
      justify-content: center;
      opacity: 0;
      transition: opacity 0.15s ease;
      color: #fff;
    }
    .pw-gallery-item:hover .pw-gallery-overlay {
      opacity: 1;
    }
    .pw-gallery-caption {
      padding: 0.5rem 0.65rem;
      font-size: 0.7rem;
      font-family: var(--pw-font-mono);
      color: var(--pw-text-muted);
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      border-top: 1px solid var(--pw-border);
      background: #fafafa;
    }
    
    .pw-meta-card {
      background: #fff;
      border: 1px solid var(--pw-border);
      border-radius: 6px;
      overflow: hidden;
      max-width: 720px;
    }
    .pw-meta-table {
      width: 100%;
      border-collapse: collapse;
      font-size: 0.8rem;
    }
    .pw-meta-table tr:not(:last-child) td {
      border-bottom: 1px solid var(--pw-border-subtle);
    }
    .pw-meta-key {
      padding: 0.6rem 1rem;
      font-weight: 600;
      color: var(--pw-text-muted);
      width: 180px;
      background: #f8fafc;
    }
    .pw-meta-val {
      padding: 0.6rem 1rem;
      color: var(--pw-text);
      font-family: var(--pw-font-mono);
    }
    
    .pw-modal {
      display: none;
      position: fixed;
      inset: 0;
      background: rgba(15, 23, 42, 0.92);
      backdrop-filter: blur(4px);
      z-index: 1000;
      align-items: center;
      justify-content: center;
      padding: 1.5rem;
    }
    .pw-modal.open {
      display: flex;
    }
    .pw-modal-content {
      max-width: 90vw;
      max-height: 90vh;
      display: flex;
      flex-direction: column;
      align-items: center;
    }
    .pw-modal-header {
      width: 100%;
      display: flex;
      justify-content: space-between;
      align-items: center;
      color: #fff;
      margin-bottom: 0.75rem;
    }
    .pw-modal-title {
      font-family: var(--pw-font-mono);
      font-size: 0.9rem;
    }
    .pw-modal-close {
      background: rgba(255, 255, 255, 0.1);
      border: none;
      color: #fff;
      width: 32px;
      height: 32px;
      border-radius: 6px;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 1.1rem;
    }
    .pw-modal-close:hover {
      background: rgba(255, 255, 255, 0.2);
    }
    .pw-modal-img {
      max-width: 100%;
      max-height: 80vh;
      border-radius: 6px;
      box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5);
      border: 1px solid rgba(255, 255, 255, 0.1);
    }
  </style>
</head>
<body>

  <header class="pw-navbar">
    <div class="pw-brand">
      <div class="pw-logo-icon">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2.5"><polygon points="5 3 19 12 5 21 5 3"></polygon></svg>
      </div>
      <div class="pw-brand-title">
        Playwright Test Report
        <span class="pw-brand-badge">Possaku Mobile Suite</span>
      </div>
    </div>
    
    <div class="pw-nav-center">
      <input type="text" id="pw-search" class="pw-search-input" placeholder="Search tests, flows, tags, actions... (Press '/' to focus)" oninput="filterAll()">
      <span class="pw-search-hint">/</span>
    </div>
    
    <div class="pw-nav-meta">
      <div class="pw-nav-chip">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg>
        <span>__TOTAL_DURATION__</span>
      </div>
      <div class="pw-nav-chip">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect><line x1="16" y1="2" x2="16" y2="6"></line><line x1="8" y1="2" x2="8" y2="6"></line><line x1="3" y1="10" x2="21" y2="10"></line></svg>
        <span>__START_TIME__</span>
      </div>
    </div>
  </header>

  <main class="pw-container">
    <div class="pw-dashboard">
      <div class="pw-stats-grid">
        <div class="pw-stat-card">
          <div class="pw-stat-label">Total Test Cases</div>
          <div class="pw-stat-val">__TOTAL_TCS__</div>
        </div>
        <div class="pw-stat-card">
          <div class="pw-stat-label">Passed TCs</div>
          <div class="pw-stat-val pass">__PASSED_TCS__</div>
        </div>
        <div class="pw-stat-card">
          <div class="pw-stat-label">Failed TCs</div>
          <div class="pw-stat-val __FAIL_CLS__">__FAILED_TCS__</div>
        </div>
        <div class="pw-stat-card">
          <div class="pw-stat-label">TC Pass Rate</div>
          <div class="pw-stat-val pass">__PASS_RATE__%</div>
        </div>
        <div class="pw-stat-card">
          <div class="pw-stat-label">Total Actions</div>
          <div class="pw-stat-val">__TOTAL_ACTIONS__</div>
        </div>
        <div class="pw-stat-card">
          <div class="pw-stat-label">Target Device</div>
          <div class="pw-stat-val" style="font-size: 1rem; font-weight: 600;">Android 11</div>
        </div>
      </div>
      
      <div class="pw-progress-bar">
        <div class="pw-progress-fill" style="width: __PASS_RATE__%;"></div>
      </div>
      
      <div class="pw-filter-bar">
        <div class="pw-filter-tabs">
          <button class="pw-filter-btn active" onclick="setStatusFilter('ALL', this)">All (__TOTAL_TCS__)</button>
          <button class="pw-filter-btn" onclick="setStatusFilter('PASS', this)">✓ Passed (__PASSED_TCS__)</button>
          <button class="pw-filter-btn" onclick="setStatusFilter('FAIL', this)">✕ Failed (__FAILED_TCS__)</button>
        </div>
        <div class="pw-expand-toggles">
          <button class="pw-btn-sm" onclick="toggleAll(true)">Expand All</button>
          <button class="pw-btn-sm" onclick="toggleAll(false)">Collapse All</button>
        </div>
      </div>
    </div>

    <div class="pw-specs-container">
      __FLOWS_HTML__
    </div>
  </main>

  <div class="pw-modal" id="pwModal" onclick="closeLightbox(event)">
    <div class="pw-modal-content" onclick="event.stopPropagation()">
      <div class="pw-modal-header">
        <span class="pw-modal-title" id="pwModalTitle">Screenshot Preview</span>
        <button class="pw-modal-close" onclick="closeLightbox()">&times;</button>
      </div>
      <img src="" id="pwModalImg" class="pw-modal-img" alt="Screenshot Preview">
    </div>
  </div>

  <script>
    let currentStatusFilter = 'ALL';

    function toggleFlow(headerEl) {
      headerEl.closest('.pw-spec-card').classList.toggle('open');
    }

    function toggleTc(headerEl) {
      headerEl.closest('.pw-tc-card').classList.toggle('open');
    }

    function switchTab(btn, targetId) {
      const card = btn.closest('.pw-spec-card');
      card.querySelectorAll('.pw-tab-btn').forEach(b => b.classList.remove('active'));
      card.querySelectorAll('.pw-tab-pane').forEach(p => p.classList.remove('active'));
      btn.classList.add('active');
      document.getElementById(targetId).classList.add('active');
    }

    function toggleAll(expand) {
      document.querySelectorAll('.pw-spec-card').forEach(el => {
        expand ? el.classList.add('open') : el.classList.remove('open');
      });
      document.querySelectorAll('.pw-tc-card').forEach(el => {
        expand ? el.classList.add('open') : el.classList.remove('open');
      });
    }

    function setStatusFilter(status, btn) {
      currentStatusFilter = status;
      btn.parentElement.querySelectorAll('.pw-filter-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      filterAll();
    }

    function filterAll() {
      const q = (document.getElementById('pw-search')?.value || '').toLowerCase();
      document.querySelectorAll('.pw-spec-card').forEach(spec => {
        let specHasMatch = false;
        spec.querySelectorAll('.pw-tc-card').forEach(tc => {
          const tcText = tc.textContent.toLowerCase();
          const tcStatus = tc.getAttribute('data-tc-status');
          const matchStatus = currentStatusFilter === 'ALL' || tcStatus === currentStatusFilter;
          const matchText = !q || tcText.includes(q);
          
          if (matchStatus && matchText) {
            tc.style.display = '';
            specHasMatch = true;
          } else {
            tc.style.display = 'none';
          }
        });
        spec.style.display = specHasMatch ? '' : 'none';
      });
    }

    function openLightbox(src, title) {
      document.getElementById('pwModalImg').src = src;
      document.getElementById('pwModalTitle').textContent = title;
      document.getElementById('pwModal').classList.add('open');
    }

    function closeLightbox() {
      document.getElementById('pwModal').classList.remove('open');
    }

    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') {
        closeLightbox();
      }
      if (e.key === '/' && document.activeElement.id !== 'pw-search') {
        e.preventDefault();
        document.getElementById('pw-search')?.focus();
      }
    });

    document.addEventListener('DOMContentLoaded', () => {
      const firstSpec = document.querySelector('.pw-spec-card');
      if (firstSpec) firstSpec.classList.add('open');
      document.querySelectorAll('.pw-tc-card').forEach(tc => tc.classList.add('open'));
    });
  </script>
</body>
</html>"""


def generate_playwright_html(suite_data):
    total_duration = suite_data.get("duration", "N/A")
    start_time = suite_data.get("start_time", "N/A")
    flows = suite_data.get("flows", [])

    total_flows = len(flows)
    passed_flows = sum(1 for f in flows if f["status"] in ("PASSED", "SUCCESS"))
    failed_flows = total_flows - passed_flows

    all_tcs = []
    total_actions = 0
    for f in flows:
        all_tcs.extend(f.get("test_cases", []))
        for tc in f.get("test_cases", []):
            total_actions += len(tc.get("steps", []))

    total_tcs = len(all_tcs)
    passed_tcs = sum(1 for tc in all_tcs if tc["status"] == "PASS")
    failed_tcs = total_tcs - passed_tcs
    pass_rate = round((passed_tcs / total_tcs * 100), 1) if total_tcs > 0 else 100.0

    flows_html_list = []
    for f_idx, flow in enumerate(flows):
        f_name = flow.get("name", f"flow_{f_idx}")
        f_status = flow.get("status", "PASSED")
        f_dur = flow.get("duration", "N/A")
        f_tags = flow.get("tags", [])
        f_tcs = flow.get("test_cases", [])
        f_screens = flow.get("screenshots", [])
        f_meta = flow.get("metadata", {})

        is_flow_pass = f_status in ("PASSED", "SUCCESS")
        flow_status_badge = '<span class="pw-badge pw-badge-pass"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><polyline points="20 6 9 17 4 12"></polyline></svg> passed</span>' if is_flow_pass else '<span class="pw-badge pw-badge-fail"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg> failed</span>'

        tags_html = "".join([f'<span class="pw-tag">@{esc(t)}</span>' for t in f_tags])

        tcs_html_list = []
        for tc_idx, tc in enumerate(f_tcs):
            tc_title = tc.get("title", f"Test Case {tc_idx+1}")
            tc_status = tc.get("status", "PASS")
            tc_dur = tc.get("duration", "N/A")
            tc_steps = tc.get("steps", [])
            is_tc_pass = tc_status == "PASS"

            tc_icon = '<div class="pw-status-icon pass"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><polyline points="20 6 9 17 4 12"></polyline></svg></div>' if is_tc_pass else '<div class="pw-status-icon fail"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg></div>'

            steps_rows = []
            for st in tc_steps:
                st_num = st.get("number", "")
                st_action = st.get("action", "")
                st_target = st.get("target", "")
                st_dur = st.get("duration", "")
                st_stat = st.get("status", "PASS")
                st_err = st.get("error", "")
                st_depth = st.get("depth", 0)

                indent_cls = f"depth-{min(st_depth, 3)}" if st_depth > 0 else ""
                depth_prefix = "↳ " if st_depth > 0 else ""

                st_icon = '<span class="pw-step-icon pass">✓</span>' if st_stat in ("PASS", "COMPLETED") else '<span class="pw-step-icon fail">✕</span>'
                err_block = f'<div class="pw-step-error"><code>{esc(st_err)}</code></div>' if st_err else ""

                steps_rows.append(f"""
                <tr class="pw-step-row {indent_cls} {'pw-row-fail' if st_stat == 'FAIL' else ''}">
                  <td class="pw-col-num">{st_num}</td>
                  <td class="pw-col-icon">{st_icon}</td>
                  <td class="pw-col-action"><span class="pw-action-name">{depth_prefix}{esc(st_action)}</span></td>
                  <td class="pw-col-target">{st_target}{err_block}</td>
                  <td class="pw-col-dur">{st_dur}</td>
                </tr>
                """)

            tcs_html_list.append(f"""
            <div class="pw-tc-card open" data-tc-status="{tc_status}">
              <div class="pw-tc-header" onclick="toggleTc(this)">
                <span class="pw-chevron">›</span>
                {tc_icon}
                <span class="pw-tc-title">{esc(tc_title)}</span>
                <span class="pw-tc-dur">{tc_dur}</span>
              </div>
              <div class="pw-tc-body">
                <table class="pw-steps-table">
                  <tbody>
                    {''.join(steps_rows)}
                  </tbody>
                </table>
              </div>
            </div>
            """)

        screens_html_list = []
        for s_idx, screen in enumerate(f_screens):
            s_name = screen.get("name", f"screenshot_{s_idx+1}.png")
            s_uri = screen.get("data_uri", "")
            screens_html_list.append(f"""
            <div class="pw-gallery-item" onclick="openLightbox('{s_uri}', '{esc(s_name)}')">
              <div class="pw-gallery-thumb">
                <img src="{s_uri}" alt="{esc(s_name)}" loading="lazy">
                <div class="pw-gallery-overlay">
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line><line x1="11" y1="8" x2="11" y2="14"></line><line x1="8" y1="11" x2="14" y2="11"></line></svg>
                </div>
              </div>
              <div class="pw-gallery-caption" title="{esc(s_name)}">{esc(s_name)}</div>
            </div>
            """)

        screens_tab_content = f"""
        <div class="pw-gallery-grid">
          {''.join(screens_html_list)}
        </div>
        """ if screens_html_list else '<div class="pw-empty-state" style="padding: 2rem; text-align: center; color: #94a3b8; font-size: 0.9rem;">No screenshots captured for this flow.</div>'

        meta_rows = [
            ("Target Device", f_meta.get("device", "emulator-5554 (Android 11)")),
            ("App Package", f_meta.get("app_id", "com.cloudiex.possaku")),
            ("Flow Name", f_name),
            ("Flow Path", f_meta.get("flow_path", f"flows/lain_lain/{f_name}.yaml")),
            ("Duration", f_dur),
            ("Start Time", flow.get("start_time", start_time)),
            ("Test Cases Count", str(len(f_tcs))),
            ("Steps Executed", str(sum(len(tc.get("steps", [])) for tc in f_tcs))),
            ("Screenshots", str(len(f_screens)))
        ]
        meta_html = "".join([f'<tr><td class="pw-meta-key">{esc(k)}</td><td class="pw-meta-val">{esc(v)}</td></tr>' for k, v in meta_rows])

        flows_html_list.append(f"""
        <div class="pw-spec-card open" id="flow-{f_idx}" data-flow-status="{f_status}">
          <div class="pw-spec-header" onclick="toggleFlow(this)">
            <div class="pw-spec-title-group">
              <span class="pw-chevron">›</span>
              <svg class="pw-file-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg>
              <span class="pw-spec-name">{esc(f_name)}</span>
              <div class="pw-tags-list">{tags_html}</div>
            </div>
            <div class="pw-spec-meta-group">
              <span class="pw-spec-dur">{f_dur}</span>
              {flow_status_badge}
            </div>
          </div>
          <div class="pw-spec-body">
            <div class="pw-tabs-nav">
              <button class="pw-tab-btn active" onclick="switchTab(this, 'steps-{f_idx}')">Steps ({sum(len(tc.get('steps', [])) for tc in f_tcs)})</button>
              <button class="pw-tab-btn" onclick="switchTab(this, 'screens-{f_idx}')">Screenshots ({len(f_screens)})</button>
              <button class="pw-tab-btn" onclick="switchTab(this, 'meta-{f_idx}')">Metadata &amp; Info</button>
            </div>
            
            <div class="pw-tab-pane active" id="steps-{f_idx}">
              <div class="pw-tcs-container">
                {''.join(tcs_html_list)}
              </div>
            </div>
            
            <div class="pw-tab-pane" id="screens-{f_idx}">
              {screens_tab_content}
            </div>
            
            <div class="pw-tab-pane" id="meta-{f_idx}">
              <div class="pw-meta-card">
                <table class="pw-meta-table">
                  <tbody>
                    {meta_html}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
        """)

    html = PLAYWRIGHT_HTML_TEMPLATE
    html = html.replace("__TOTAL_DURATION__", esc(total_duration))
    html = html.replace("__START_TIME__", esc(start_time))
    html = html.replace("__TOTAL_TCS__", str(total_tcs))
    html = html.replace("__PASSED_TCS__", str(passed_tcs))
    html = html.replace("__FAILED_TCS__", str(failed_tcs))
    html = html.replace("__FAIL_CLS__", "fail" if failed_tcs > 0 else "")
    html = html.replace("__PASS_RATE__", str(pass_rate))
    html = html.replace("__TOTAL_ACTIONS__", str(total_actions))
    html = html.replace("__FLOWS_HTML__", "".join(flows_html_list))
    return html


def parse_existing_html_report(html_content):
    suite_data = {
        "title": "Possaku Maestro Mobile Suite",
        "duration": "N/A",
        "start_time": "N/A",
        "flows": []
    }

    dur_m = re.search(r'Duration:\s*([^\n<]+)', html_content)
    if dur_m:
        suite_data["duration"] = dur_m.group(1).strip()

    time_m = re.search(r'Start Time:\s*<time[^>]*>([^<]+)</time>', html_content)
    if time_m:
        suite_data["start_time"] = time_m.group(1).strip()

    flow_matches = list(re.finditer(r'<div class="collapse"\s+id="([A-Za-z0-9_-]+)">', html_content))

    for i, m in enumerate(flow_matches):
        collapse_id = m.group(1)
        start = m.start()
        end = flow_matches[i+1].start() if i+1 < len(flow_matches) else html_content.find('<!-- Lightbox Modal -->', start)
        if end == -1:
            end = len(html_content)
        flow_body = html_content[start:end]

        clean_name = re.sub(r"^flow-\d+-", "", collapse_id)
        flow_status = "PASSED" if "Status: SUCCESS" in flow_body or "Result: PASSED" in flow_body or "SUCCESS" in flow_body else "FAILED"

        f_dur_m = re.search(r'Duration:\s*([0-9.smh ]+)', flow_body)
        f_dur = f_dur_m.group(1).strip() if f_dur_m else suite_data["duration"]

        tags = re.findall(r'<span class="badge bg-primary me-1">([^<]+)</span>', flow_body)

        screens = []
        screen_matches = re.findall(r"openScreenshot\('(data:image/png;base64,[^']+)',\s*'([^']+)'\)", flow_body)
        for s_uri, s_name in screen_matches:
            screens.append({"name": s_name, "data_uri": s_uri})

        test_cases = []
        tc_splits = re.split(r'<tr class="border-top border-2">', flow_body)

        if len(tc_splits) > 0:
            setup_steps = re.findall(r'<tr class="([^"]*)">\s*<td class="text-center font-monospace small">(\d+)</td>\s*<td class="fw-semibold"[^>]*>(.*?)</td>\s*<td>(.*?)</td>\s*<td class="text-end font-monospace small text-muted">([^<]+)</td>\s*<td class="text-center"><span class="badge bg-([^"]+)">([^<]+)</span>', tc_splits[0])
            if setup_steps:
                parsed_setup = []
                for st_cls, st_num, st_action, st_target, st_dur, st_badge_cls, st_stat in setup_steps:
                    clean_action = st_action.replace("↳ ", "").strip()
                    depth = 1 if "↳" in st_action else 0
                    parsed_setup.append({
                        "number": st_num,
                        "action": clean_action,
                        "target": st_target.strip(),
                        "duration": st_dur.strip(),
                        "status": "PASS" if "PASS" in st_stat or "success" in st_badge_cls else "FAIL",
                        "depth": depth
                    })
                test_cases.append({
                    "title": "# [SETUP] Flow Preconditions & Navigation",
                    "status": "PASS",
                    "duration": "Setup",
                    "steps": parsed_setup
                })

        if len(tc_splits) > 1:
            for part in tc_splits[1:]:
                tc_head_m = re.search(r'<span class="[^\"]*font-monospace fw-bold">([^<]+)</span>.*?<td class="text-end font-monospace small[^\"]*\"[^>]*>([^<]+)</td>.*?<span class="badge bg-([^\"]+)">([^<]+)</span>', part, re.DOTALL)
                if not tc_head_m:
                    continue
                tc_title = tc_head_m.group(1).strip()
                tc_dur = tc_head_m.group(2).strip()
                tc_stat = "PASS" if "PASS" in tc_head_m.group(4) else "FAIL"

                steps = []
                step_matches = re.findall(r'<tr class="([^"]*)">\s*<td class="text-center font-monospace small">(\d+)</td>\s*<td class="fw-semibold"[^>]*>(.*?)</td>\s*<td>(.*?)</td>\s*<td class="text-end font-monospace small text-muted">([^<]+)</td>\s*<td class="text-center"><span class="badge bg-([^"]+)">([^<]+)</span>', part)
                for st_cls, st_num, st_action, st_target, st_dur, st_badge_cls, st_stat in step_matches:
                    clean_action = st_action.replace("↳ ", "").strip()
                    depth = 1 if "↳" in st_action else 0
                    steps.append({
                        "number": st_num,
                        "action": clean_action,
                        "target": st_target.strip(),
                        "duration": st_dur.strip(),
                        "status": "PASS" if "PASS" in st_stat or "success" in st_badge_cls else "FAIL",
                        "depth": depth
                    })

                test_cases.append({
                    "title": tc_title,
                    "status": tc_stat,
                    "duration": tc_dur,
                    "steps": steps
                })

        suite_data["flows"].append({
            "name": clean_name,
            "status": flow_status,
            "duration": f_dur,
            "tags": tags,
            "test_cases": test_cases,
            "screenshots": screens,
            "metadata": {
                "device": "emulator-5554 (Android 11)",
                "app_id": "com.cloudiex.possaku",
                "flow_path": f"flows/lain_lain/{clean_name}.yaml"
            }
        })

    return suite_data


def build_suite_data_from_debug(report_path, debug_dir):
    with open(report_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    suite_data = {
        "title": "Possaku Maestro Mobile Suite",
        "duration": "N/A",
        "start_time": "N/A",
        "flows": []
    }

    dur_m = re.search(r'Duration:\s*([^\n<]+)', html_content)
    if dur_m:
        suite_data["duration"] = dur_m.group(1).strip()

    time_m = re.search(r'Start Time:\s*<time[^>]*>([^<]+)</time>', html_content)
    if time_m:
        suite_data["start_time"] = time_m.group(1).strip()

    flow_ids = re.findall(r'<div class="collapse"\s+id="([A-Za-z0-9_-]+)">', html_content)
    if not flow_ids:
        # Fallback if no collapse IDs
        return None

    for flow_collapse_id in flow_ids:
        clean_name = re.sub(r"^flow-\d+-", "", flow_collapse_id)
        json_file = find_commands_json(debug_dir, clean_name)
        if not json_file:
            continue

        try:
            with open(json_file, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            print(f"Error reading {json_file}: {e}")
            continue

        items = [item for item in data if "timestamp" in item.get("metadata", {})]
        items.sort(key=lambda x: x["metadata"].get("sequenceNumber", x["metadata"]["timestamp"]))

        source_yaml = find_source_yaml(clean_name)
        yaml_comments = parse_yaml_sections(source_yaml)

        sections = []
        current_section = {"title": None, "is_tc": False, "steps": [], "duration": 0, "status": "PASS"}
        step_number = 1
        root_cmd_index = 0

        for item in items:
            cmd = item.get("command", {})
            meta = item.get("metadata", {})
            eval_cmd = meta.get("evaluatedCommand", {})
            dur = meta.get("duration", 0)
            status = meta.get("status", "COMPLETED")
            error_msg = meta.get("error", "")
            depth = meta.get("depth", 0)

            cmd_type = list(cmd.keys())[0] if cmd else ""
            if cmd_type in ("defineVariablesCommand", "applyConfigurationCommand"):
                continue

            if depth == 0 and root_cmd_index in yaml_comments:
                if current_section["title"] or current_section["steps"]:
                    sections.append(current_section)
                sec_title = yaml_comments[root_cmd_index]
                is_tc = any(char.isdigit() for char in sec_title)
                display_title = f"# {sec_title}" if (is_tc and not sec_title.startswith("#")) else sec_title
                current_section = {
                    "title": display_title,
                    "is_tc": is_tc,
                    "steps": [],
                    "duration": 0,
                    "status": "PASS",
                }

            if depth == 0:
                root_cmd_index += 1
                current_section["duration"] += dur

            if status == "FAILED":
                current_section["status"] = "FAIL"

            action_name, action_detail = format_command(cmd, eval_cmd)
            step_obj = {
                "number": step_number,
                "action": action_name,
                "target": action_detail,
                "duration": format_duration(dur),
                "status": "PASS" if status == "COMPLETED" else status,
                "depth": depth,
                "error": error_msg
            }
            current_section["steps"].append(step_obj)
            step_number += 1

        if current_section["title"] or current_section["steps"]:
            sections.append(current_section)

        test_cases = []
        for sec in sections:
            tc_title = sec["title"] or "# [EXEC] General Commands"
            test_cases.append({
                "title": tc_title,
                "status": sec["status"],
                "duration": format_duration(sec["duration"]),
                "steps": sec["steps"]
            })

        screenshots = []
        raw_screens = find_screenshots(json_file)
        for img_path in raw_screens:
            img_name = os.path.basename(img_path)
            try:
                with open(img_path, "rb") as img_f:
                    img_b64 = base64.b64encode(img_f.read()).decode("utf-8")
                    data_uri = f"data:image/png;base64,{img_b64}"
                    screenshots.append({"name": img_name, "data_uri": data_uri})
            except Exception:
                pass

        flow_status = "FAILED" if any(tc["status"] == "FAIL" for tc in test_cases) else "PASSED"
        flow_dur = format_duration(sum(sec["duration"] for sec in sections))

        tags = []
        if source_yaml and os.path.exists(source_yaml):
            with open(source_yaml, "r", encoding="utf-8") as yf:
                y_text = yf.read()
                tags = re.findall(r'-\s+([a-zA-Z0-9_\-]+)', y_text.split("---")[0]) if "tags:" in y_text else []
                tags = [t for t in tags if t != "tags"]

        suite_data["flows"].append({
            "name": clean_name,
            "status": flow_status,
            "duration": flow_dur,
            "tags": tags,
            "test_cases": test_cases,
            "screenshots": screenshots,
            "metadata": {
                "device": "emulator-5554 (Android 11)",
                "app_id": "com.cloudiex.possaku",
                "flow_path": source_yaml or f"flows/{clean_name}.yaml"
            }
        })

    return suite_data


def repolish_report(report_path):
    if not os.path.exists(report_path):
        print(f"File not found: {report_path}")
        return False
    try:
        with open(report_path, "r", encoding="utf-8") as f:
            html = f.read()
        suite_data = parse_existing_html_report(html)
        if not suite_data["flows"]:
            print(f"Skipping {report_path}: No flow data could be parsed.")
            return False
        polished_html = generate_playwright_html(suite_data)
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(polished_html)
        print(f"Successfully polished {report_path} into Playwright style!")
        return True
    except Exception as e:
        print(f"Error repolishing {report_path}: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Generate Playwright-style HTML reports for Maestro")
    parser.add_argument("--report", default="reports/report.html", help="Path to Maestro HTML report file")
    parser.add_argument("--debug", default="debug_out", help="Path to Maestro debug output directory")
    parser.add_argument("--repolish", help="Repolish an existing HTML report into Playwright format")
    parser.add_argument("--repolish-all", action="store_true", help="Repolish all HTML reports in reports/")
    args = parser.parse_args()

    if args.repolish_all:
        report_files = sorted(glob.glob("reports/*.html"))
        print(f"Repolishing {len(report_files)} reports in reports/...")
        success_count = sum(1 for rf in report_files if repolish_report(rf))
        print(f"Repolishing complete: {success_count}/{len(report_files)} reports updated.")
        return

    if args.repolish:
        repolish_report(args.repolish)
        return

    report_path = args.report
    if not os.path.exists(report_path) and os.path.exists(os.path.join("reports", report_path)):
        report_path = os.path.join("reports", report_path)

    if not os.path.exists(report_path):
        print(f"Error: Report file '{report_path}' does not exist.")
        sys.exit(0)

    # First attempt building from debug logs
    if os.path.exists(args.debug):
        suite_data = build_suite_data_from_debug(report_path, args.debug)
        if suite_data and suite_data["flows"]:
            playwright_html = generate_playwright_html(suite_data)
            with open(report_path, "w", encoding="utf-8") as f:
                f.write(playwright_html)
            print(f"Playwright-style HTML report generated at: {report_path}")
            return

    # Fallback: repolish existing report in-place
    print(f"Debug output not found. Repolishing existing report {report_path}...")
    repolish_report(report_path)


if __name__ == "__main__":
    main()
