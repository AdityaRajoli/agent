import os
import sys

sys.path.insert(0, os.path.abspath("src"))

from analyzer.code_analyzer import parse_code_constraints
from generator.test_generator import generate_tests
from monitor.perf_monitor import run_adaptive_tests
from tools.pr_client import publish_pr_review

def main():
    print("Starting BabyAGI Loop...\n")

    # Files to analyze
    code_changes = []
    for f in os.listdir("app"):
        if f.endswith('.py') or f.endswith('.c'):
            code_changes.append(f"app/{f}")

    if not code_changes:
        print("No Python or C files found in app/")
        sys.exit(0)

    print(f"Analyzing: {code_changes}\n")

    # Step 1: Extract constraints
    constraints = parse_code_constraints(code_changes)

    # Step 2: Generate tests using RTM + PCM
    test_files = generate_tests(
        constraints,
        rtm_path="rtm/",
        pcm_path="pcm/"
    )

    # Step 3: Run tests + measure performance
    metrics = run_adaptive_tests(test_files)
    print("\n--- AI PERFORMANCE METRICS ---")
    print(metrics)
    print("------------------------------\n")

    # Step 4: Decision
    verdict  = "APPROVE"
    comments = []

    if metrics['coverage'] < 80.0:
        verdict = "REQUEST_CHANGES"
        comments.append(
            f"Coverage is {metrics['coverage']}%. Minimum required is 80%."
        )

    if metrics['complexity'] > 10:
        verdict = "REQUEST_CHANGES"
        comments.append(
            f"Complexity is {metrics['complexity']}. Refactor required."
        )

    if not metrics['tests_passed']:
        verdict = "REQUEST_CHANGES"
        comments.append(
            "Tests failed. Fix before merging."
        )

    # Step 5: Publish review
    publish_pr_review(
        pr_number=os.getenv("PR_NUMBER"),
        verdict=verdict,
        comments=comments,
        metrics=metrics
    )

    print(f"\nFinal Status: {'pass' if verdict == 'APPROVE' else 'fail'}")

if __name__ == "__main__":
    main()
