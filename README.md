# Rekor Transparency Log Verifier

**A Python-based command-line tool for verifying software supply chain integrity using Sigstore's Rekor transparency log.**

 **CS-GY 9223: Software Supply Chain Security** 

---

## Overview

This project provides a CLI for interacting with the Sigstore Rekor transparency log. It helps validate artifact authenticity and transparency log integrity.


## Features

| Feature | Description |
|---|---|
| **Log Entry Retrieval** | Retrieve entries from the Rekor transparency log using their log indices. |
| **Inclusion Proof Verification** | Verify whether an entry belongs to a Merkle tree using its inclusion proof. |
| **Consistency Proof Verification** | Verify consistency between two transparency log checkpoints. |
| **Artifact Signature Verification** | Validate cryptographic signatures associated with artifacts. |
| **Debug Mode** | Enable additional diagnostic output for verification operations. |

## Technologys Used

| Component | Technology |
|---|---|
| Language | Python 3.12+ |
| Dependency Management | Poetry |
| Transparency Log | Sigstore Rekor |
| Formatting & Linting | Ruff |
| Static Type Checking | Mypy |
| Security Analysis | Bandit |

## Getting Started

### Prerequisites

To run the project, you need:

- Python 3.12 or newer
- Poetry
- An internet connection for accessing the Rekor API

## Installation

**1. Clone the repository**

```bash
git clone https://github.com/MariamRukhaia/mr6610-assignment1.git
cd mr6610-assignment1
```

**2. Install dependencies**

```bash
poetry install --no-root
```

**3. Run the program**

```bash
poetry run python main.py 
```

## Usage

**Get the latest checkpoint**
```bash
poetry run python main.py -c
```

**Verify inclusion of an artifact**
```bash
poetry run python main.py --inclusion <LOG_INDEX> --artifact <ARTIFACT_PATH>
```

**Verify consistency with a previous checkpoint**
```bash
poetry run python main.py --consistency --tree-id <TREE_ID> --tree-size <TREE_SIZE> --root-hash <ROOT_HASH>
```


## Project Structure

```text
.
├── main.py                  # CLI and Rekor API interactions
├── merkle_proof.py          # Merkle proof verification
├── util.py                  # Cryptographic utility functions
├── scripts/                 # Supporting scripts
├── pyproject.toml           # Dependencies and tool configuration
├── poetry.lock              # Locked dependency versions
├── README.md                # Project documentation
├── SECURITY.md              # Vulnerability reporting policy
├── CONTRIBUTING.md          # Contribution guidelines
├── LICENSE                  # Project license
└── .github/
    └── CODEOWNERS          # Code ownership rules
```

## Development

This project uses automated static analysis tools to maintain code quality and security.

### Code Formatting

```bash
poetry run ruff format .
```

### Linting

```bash
poetry run ruff check .
```

### Type Checking

```bash
poetry run mypy main.py merkle_proof.py util.py
```

### Security Scanning

```bash
poetry run bandit -r . -f txt
```

### Verify Formatting

```bash
poetry run ruff format --check .
```

## Code Quality

The project uses the following automated quality checks:

| Tool | Purpose | Latest Local Result |
|---|---|---|
| Ruff | Linting | Passed |
| Ruff Formatter | Code formatting | Passed |
| Mypy | Static type checking | Passed |
| Bandit | Security vulnerability scanning | No issues identified |


## Security

Security vulnerabilities should be reported responsibly. See [SECURITY.md](SECURITY.md) for supported versions, reporting procedures, and security update policies.

## Contributing

Contributions should follow the project's coding standards and testing requirements. See [CONTRIBUTING.md](CONTRIBUTING.md) for instructions on submitting issues and pull requests.

## License

See the [LICENSE](LICENSE) file for licensing terms.

---

**New York University — CS-GY 9223: Software Supply Chain Security**
