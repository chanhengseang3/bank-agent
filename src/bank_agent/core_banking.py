from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class Account(BaseModel):
    """Represents a simplified bank account record."""

    account_id: str
    owner_name: str
    balance: float = Field(..., ge=0)
    currency: str = "USD"


class Transaction(BaseModel):
    """Represents a transaction on an account."""

    account_id: str
    amount: float
    description: str


class CoreBankingClient:
    """Abstracts the core banking operations the agent relies on."""

    def list_accounts(self) -> List[Account]:
        raise NotImplementedError

    def get_account(self, account_id: str) -> Optional[Account]:
        raise NotImplementedError

    def record_transaction(self, transaction: Transaction) -> Account:
        raise NotImplementedError


@dataclass
class InMemoryCoreBanking(CoreBankingClient):
    """Simple in-memory mock of a core banking system."""

    accounts: Dict[str, Account] = field(default_factory=dict)

    def list_accounts(self) -> List[Account]:
        return list(self.accounts.values())

    def get_account(self, account_id: str) -> Optional[Account]:
        return self.accounts.get(account_id)

    def record_transaction(self, transaction: Transaction) -> Account:
        account = self.accounts.get(transaction.account_id)
        if account is None:
            raise ValueError(f"Account {transaction.account_id} not found.")
        new_balance = account.balance + transaction.amount
        if new_balance < 0:
            raise ValueError("Insufficient funds for this transaction.")
        updated = account.copy(update={"balance": new_balance})
        self.accounts[transaction.account_id] = updated
        return updated
