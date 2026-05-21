# Protocol Context Model (PCM)

## Communication Protocol

### main_reviewer.py
- Input  : changed files from GitHub PR
- Output : PR review decision
- Protocol: function calls

### ast_parser.py
- Input  : file path (string)
- Output : functions, branches, language
- Protocol: Python AST parsing

### ai_test_gen.py
- Input  : constraints, rtm_path, pcm_path
- Output : generated test files
- Protocol: OpenRouter AI API call

### performance_monitor.py
- Input  : test files list
- Output : metrics dict (coverage, complexity, time)
- Protocol: subprocess (pytest, lizard)

### github_client.py
- Input  : pr_number, verdict, comments, metrics
- Output : PR review posted to GitHub
- Protocol: GitHub REST API
