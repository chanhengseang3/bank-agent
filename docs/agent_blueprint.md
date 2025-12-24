# Bank Agent Functional Blueprint

This blueprint describes how the agent can support day-to-day banking roles. It maps role-specific responsibilities to the agent's capabilities and clarifies architectural components that enable safe, auditable automations.

## Purpose and scope

- Provide a role-aware assistant that adapts prompts, guardrails, and outputs to bankers such as tellers, credit officers, branch managers, and compliance analysts.
- Offer a single interaction layer for account servicing, transaction handling, and credit workflows, backed by the core banking client abstractions in `src/bank_agent`.
- Emphasize auditability and safety via conversation logging and validation before executing actions.

## Core building blocks

- **Conversation context** (`ConversationContext` in `src/bank_agent/agent.py`): records sequential messages to preserve intent and create audit trails.
- **Agent orchestration** (`BankAgent` in `src/bank_agent/agent.py`): routes intents to core banking operations such as greetings, account lookups, descriptions, and transaction processing.
- **Core banking abstraction** (`CoreBankingClient` in `src/bank_agent/core_banking.py`): defines the contract for listing accounts, fetching account details, and recording transactions. `InMemoryCoreBanking` provides a mock for local use.
- **Interfaces** (`src/bank_agent/cli.py`): Typer CLI entry points that exercise the agent with seeded data in `data/accounts.json`.
- **Controls**: validation via Pydantic models (`Account`, `Transaction`) and error handling in `BankAgent.process_transaction` to prevent overdrafts or invalid accounts.

## Role-specific functions

### Teller

- **Account servicing**: quickly retrieve account summaries and balances (via `describe_account`) and list portfolios assigned to the branch (via `show_accounts`).
- **Cash transactions**: record deposits or withdrawals by passing signed transaction amounts to `process_transaction`, with balance validation.
- **Customer communication**: use `greet` and contextual responses from `ConversationContext` to keep a consistent, friendly tone while confirming actions.

### Credit officer / underwriter

- **Application intake**: collect applicant identifiers and link to existing accounts through `get_account` lookups in the core client.
- **Balance and history checks**: pull account details and recent transaction outcomes to inform credit decisions (future extension: transaction history feed).
- **Decisioning workflow**: propose credit decisions with auditable rationale stored in `ConversationContext`; enqueue approved disbursements as transactions when ready.

### Branch manager

- **Oversight**: review teller activity through conversation logs and account updates to monitor cash movements and service quality.
- **Approvals**: apply dual-control by requiring manager confirmation before high-value withdrawals; implement via wrappers around `process_transaction` that check limits.
- **Branch reporting**: produce daily summaries of account activity and exceptions pulled from core client aggregates.

### Operations / back office

- **Reconciliation support**: verify that recorded transactions align with expected balances; flag mismatches for manual review.
- **Adjustments**: post manual corrections as signed transactions with descriptive metadata for audit.
- **Batch processing**: orchestrate scheduled tasks (e.g., interest accrual, fee posting) using the same `record_transaction` pathway with role-based templates.

### Compliance and risk

- **Policy enforcement**: check transactions against thresholds, sanctioned parties, and watchlists before committing; block or escalate when rules trigger (to be implemented as pre-transaction validators).
- **Audit trails**: export `ConversationContext` logs and transaction metadata for regulatory review.
- **KYC refresh**: prompt bankers when account lookups reveal stale customer data (future extension: data freshness checks on accounts).

### Customer service / contact center

- **Inquiry handling**: surface balances, account ownership, and recent actions in plain language via `describe_account` outputs.
- **Guided resolution**: follow scripted flows that branch on customer intent, using stored context to avoid repeated questions.
- **Secure verification**: embed authentication steps before sharing sensitive account details (to be layered on top of CLI or chat interface).

### Technology / support

- **Environment diagnostics**: verify connectivity to the configured `CoreBankingClient` implementation and raise actionable errors when dependencies are missing.
- **Feature toggling**: enable or disable role packs (e.g., credit, teller, compliance) at runtime to align with deployment policies.
- **Observability**: instrument agent actions (account lookups, transactions, approvals) for metrics and alerting.

## Interaction patterns

1. Banker initiates a request through CLI or chat UI.
2. Agent captures the message in `ConversationContext` and determines intent by role and action type.
3. Agent performs safe read/write operations through the `CoreBankingClient` implementation, validating inputs with Pydantic models.
4. Responses are echoed to the console (or chat channel) and appended to context for traceability.
5. Downstream systems (approvals, compliance checks, audit exports) can subscribe to context and transaction events.

## Extensibility roadmap

- Add role-aware prompt templates and guardrails per function (e.g., teller cash limits, credit underwriting checklists).
- Integrate transaction history and customer profile services to enrich `describe_account` responses.
- Introduce approval workflows and segregation of duties before executing sensitive actions.
- Expand interfaces beyond CLI to chat and case-management tools while reusing the same agent orchestration and core client contract.
