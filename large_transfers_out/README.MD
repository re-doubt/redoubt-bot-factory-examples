## Large Transfer Out Bot

### Description

This bot detects transactions with large TON native transfers (>50k TON). By itself, this bot will be quite noisy.

### Supported Chains

- TON

### Alerts

- LARGE-TRANSFER-OUT
  - Fired when a transaction contains a large native transfer 
  - Severity is always set to "low" (mention any conditions where it could be something else)
  - Type is always set to "suspicious" (mention any conditions where it could be something else)
  - Mention any other type of metadata fields included with this alert
  - Low confidence labels (0.3) for attacker address are emitted
  - Metadata exposes the anomaly_score for the alert
