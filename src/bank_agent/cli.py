from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

import typer
from rich import print

from .agent import BankAgent
from .core_banking import Account, InMemoryCoreBanking, Transaction

app = typer.Typer(help="Bank Agent CLI to interact with the core banking mock.")


DATA_PATH = Path("data/accounts.json")


def load_accounts() -> InMemoryCoreBanking:
    client = InMemoryCoreBanking()
    if not DATA_PATH.exists():
        return client
    content = json.loads(DATA_PATH.read_text())
    for row in content:
        account = Account.model_validate(row)
        client.accounts[account.account_id] = account
    return client


@app.command()
def greet() -> None:
    """Send a greeting from the agent."""
    agent = BankAgent(core_client=load_accounts())
    agent.greet()


@app.command("list")
def list_accounts() -> None:
    """List all accounts."""
    agent = BankAgent(core_client=load_accounts())
    agent.show_accounts()


@app.command()
def describe(account_id: str = typer.Argument(..., help="Target account id")) -> None:
    """Describe a specific account."""
    agent = BankAgent(core_client=load_accounts())
    agent.describe_account(account_id)


@app.command()
def transact(
    account_id: str = typer.Argument(..., help="Target account id"),
    amount: float = typer.Argument(..., help="Positive for deposit, negative for withdrawal"),
    description: Optional[str] = typer.Option(None, "--description", "-d", help="Transaction note"),
) -> None:
    """Record a transaction against an account."""
    agent = BankAgent(core_client=load_accounts())
    txn = Transaction(account_id=account_id, amount=amount, description=description or "Agent transaction")
    agent.process_transaction(txn)


def main() -> None:
    app()


if __name__ == "__main__":
    main()
