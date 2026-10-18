# Security Policy

## Reporting a Vulnerability

Please **do not** open a public GitHub issue for security vulnerabilities.

Report vulnerabilities privately through GitHub's private vulnerability reporting
(Security tab → "Report a vulnerability"), or by emailing the maintainer at mr6610@nyu.edu.

Please include:

- A description of the vulnerability and its potential impact
- Steps to reproduce it
- The affected file(s) and version or commit
- Any suggested fix, if you have one

## How Security Updates Are Handled

- **Acknowledgement:** within 2 business days of the report.
- **Assessment:** the maintainer confirms the issue and determines its severity.
- **Fix:** a patch is developed on a separate branch and merged into `main` through a pull request.

## Security Practices

- **Bandit** for static security analysis
- **TruffleHog** in a pre-commit hook to block secrets from being committed
- **Branch protection** on `main`, requiring pull requests and linear history
- **Pinned dependencies** through `poetry.lock`
