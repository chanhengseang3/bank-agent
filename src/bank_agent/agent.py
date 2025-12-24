from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from rich.console import Console

from .core_banking import Account, CoreBankingClient, Transaction


console = Console()


@dataclass
class ConversationContext:
    """Tracks a conversation between the agent and a banker."""

    messages: List[str] = field(default_factory=list)

    def add(self, message: str) -> None:
        self.messages.append(message)


@dataclass
class BankAgent:
    """A lightweight agent that guides bankers through common actions."""

    core_client: CoreBankingClient
    context: ConversationContext = field(default_factory=ConversationContext)

    def greet(self) -> str:
        greeting = "Hello! I'm your banking assistant. How can I help you today?"
        self.context.add(greeting)
        console.print(greeting)
        return greeting

    def show_accounts(self) -> List[Account]:
        accounts = self.core_client.list_accounts()
        if not accounts:
            message = "No accounts available."
            self.context.add(message)
            console.print(f"[yellow]{message}[/yellow]")
            return []
        for account in accounts:
            console.print(f"[cyan]{account.account_id}[/cyan]: {account.owner_name} - {account.balance} {account.currency}")
        self.context.add("Displayed account list.")
        return accounts

    def describe_account(self, account_id: str) -> str:
        account = self.core_client.get_account(account_id)
        if not account:
            message = f"Account {account_id} not found."
            self.context.add(message)
            console.print(f"[red]{message}[/red]")
            return message
        description = (
            f"Account {account.account_id} belongs to {account.owner_name} "
            f"with a balance of {account.balance} {account.currency}."
        )
        self.context.add(description)
        console.print(description)
        return description

    def process_transaction(self, transaction: Transaction) -> str:
        try:
            updated_account = self.core_client.record_transaction(transaction)
        except ValueError as exc:
            error_message = str(exc)
            self.context.add(error_message)
            console.print(f"[red]{error_message}[/red]")
            return error_message
        success_message = (
            f"Recorded transaction for account {updated_account.account_id}. "
            f"New balance: {updated_account.balance} {updated_account.currency}."
        )
        self.context.add(success_message)
        console.print(success_message)
        return success_message
