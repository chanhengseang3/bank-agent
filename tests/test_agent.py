from bank_agent.agent import BankAgent
from bank_agent.core_banking import Account, InMemoryCoreBanking, Transaction


def build_client() -> InMemoryCoreBanking:
    client = InMemoryCoreBanking()
    client.accounts = {
        "A1": Account(account_id="A1", owner_name="Casey", balance=100.0),
    }
    return client


def test_greet_records_context(capsys):
    agent = BankAgent(core_client=build_client())
    message = agent.greet()
    captured = capsys.readouterr().out
    assert "Hello! I'm your banking assistant" in message
    assert "Hello! I'm your banking assistant" in captured
    assert agent.context.messages[-1] == message


def test_show_accounts_lists_accounts(capsys):
    agent = BankAgent(core_client=build_client())
    accounts = agent.show_accounts()
    captured = capsys.readouterr().out
    assert len(accounts) == 1
    assert "Casey" in captured
    assert agent.context.messages[-1] == "Displayed account list."


def test_describe_missing_account(capsys):
    agent = BankAgent(core_client=build_client())
    message = agent.describe_account("missing")
    captured = capsys.readouterr().out
    assert "not found" in message
    assert "not found" in captured


def test_process_transaction_updates_balance(capsys):
    agent = BankAgent(core_client=build_client())
    txn = Transaction(account_id="A1", amount=50.0, description="Deposit")
    message = agent.process_transaction(txn)
    captured = capsys.readouterr().out
    assert "New balance" in message
    assert "150.0" in message
    assert "150.0" in captured


def test_process_transaction_insufficient_funds(capsys):
    agent = BankAgent(core_client=build_client())
    txn = Transaction(account_id="A1", amount=-200.0, description="Withdrawal")
    message = agent.process_transaction(txn)
    captured = capsys.readouterr().out
    assert "Insufficient funds" in message
    assert "Insufficient funds" in captured
