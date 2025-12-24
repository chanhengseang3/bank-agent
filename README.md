# bank-agent

An AI agent starter project that connects to a core banking backend and helps bankers complete day-to-day banking tasks.

## Features
- Lightweight `BankAgent` class to greet bankers, list accounts, describe a specific account, and process transactions.
- In-memory mock core banking client for local experimentation.
- Typer-powered CLI to interact with the agent.
- Sample data seeded in `data/accounts.json`.
- Pytest-based test suite.

## Getting started
1. Install dependencies:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -e .
   ```
2. Run the CLI:
   ```bash
   python -m bank_agent.cli greet
   python -m bank_agent.cli list
   python -m bank_agent.cli describe CHK-1001
   python -m bank_agent.cli transact CHK-1001 100 --description "Deposit"
   ```
3. Run tests:
   ```bash
   pytest
   ```
