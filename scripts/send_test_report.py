import json
import os
import sys
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path


def main():
    xml_file = Path("test-report") / "testreport.xml"

    if not xml_file.exists():
        raise FileNotFoundError(
            f"JUnit report not found: {xml_file.resolve()}"
        )

    root = ET.parse(xml_file).getroot()

    test_cases = root.findall(".//testcase")
    tests = []

    for case in test_cases:
        failure = case.find("failure")
        error = case.find("error")
        skipped = case.find("skipped")

        if failure is not None or error is not None:
            result = "failed"
            issue = failure if failure is not None else error
            failure_message = (
                issue.get("message") or (issue.text or "").strip()
            )
        elif skipped is not None:
            result = "skipped"
            failure_message = ""
        else:
            result = "passed"
            failure_message = ""

        tests.append({
            "name": case.get("name", "Unknown test"),
            "result": result,
            "failure_message": failure_message
        })

    total = len(tests)
    passed = sum(t["result"] == "passed" for t in tests)
    failed = sum(t["result"] == "failed" for t in tests)
    skipped_count = sum(t["result"] == "skipped" for t in tests)

    report = {
        "repository_name": os.environ.get("GITHUB_REPOSITORY", "unknown"),
        "branch": os.environ.get("GITHUB_REF_NAME", "unknown"),
        "commit_sha": os.environ.get("GITHUB_SHA", "unknown"),
        "pipeline_run_id": os.environ.get("GITHUB_RUN_ID", "unknown"),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "tests": tests,
        "total_tests": total,
        "passed_tests": passed,
        "failed_tests": failed,
        "skipped_tests": skipped_count,
        "overall_status": "failed" if failed > 0 else "passed"
    }

    token = os.environ.get("REPORT_RECEIVER_TOKEN")
    if not token:
        raise RuntimeError("REPORT_RECEIVER_TOKEN secret is missing.")

    data = json.dumps(report, indent=2).encode("utf-8")
    request = urllib.request.Request(
        "http://127.0.0.1:8765/report",
        data=data,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        },
        method="POST"
    )

    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            print("Receiver response:", response.read().decode("utf-8"))
    except urllib.error.URLError as exc:
        print("Could not deliver report:", exc)
        sys.exit(1)

    print(f"Repository: {report['repository_name']}")
    print(f"Branch: {report['branch']}")
    print(f"Total: {total}, Passed: {passed}, Failed: {failed}")
    print(f"Overall status: {report['overall_status']}")


if __name__ == "__main__":
    main()