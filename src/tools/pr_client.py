import os
import requests

def publish_pr_review(pr_number, verdict, comments, metrics):
    token = os.getenv("GITHUB_TOKEN")
    repo  = os.getenv("GITHUB_REPOSITORY")

    if not token or not repo or not pr_number:
        print("Missing GitHub context. Printing review locally:")
        print(f"\n{'='*50}")
        print(f"PR REVIEW: {verdict}")
        print(f"Coverage         : {metrics['coverage']}%")
        print(f"Complexity       : {metrics['complexity']}")
        print(f"Execution Time   : {metrics['execution_time_sec']}s")
        print(f"CPU              : {metrics['cpu_percent']}%")
        print(f"RAM              : {metrics['ram_percent']}%")
        print(f"RMA Utilization  : {metrics['rma_utilization']}%")
        print(f"RMA Threshold    : {metrics['rma_threshold']}%")
        print(f"RMA Status       : {'✅ OK' if metrics['rma_utilization'] <= metrics['rma_threshold'] else '❌ Exceeded'}")
        if comments:
            print("\nReview Notes:")
            for comment in comments:
                print(f"  - {comment}")
        print('='*50)
        return

    url     = f"https://api.github.com/repos/{repo}/pulls/{pr_number}/reviews"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept"       : "application/vnd.github.v3+json"
    }

    body  = f"### AI Autonomous Review: {verdict}\n\n"
    body += f"**Coverage:** {metrics['coverage']}%\n"
    body += f"**Complexity:** {metrics['complexity']}\n"
    body += f"**Execution Time:** {metrics['execution_time_sec']}s\n"
    body += f"**RMA Utilization:** {metrics['rma_utilization']}%\n"
    body += f"**RMA Threshold:** {metrics['rma_threshold']}%\n\n"

    if comments:
        body += "#### Review Notes:\n"
        for comment in comments:
            body += f"- {comment}\n"

    data = {"body": body, "event": verdict}
    requests.post(url, headers=headers, json=data)
    print(f"PR Review posted: {verdict}")
