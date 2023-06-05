## DeDust Swaps Tracking

### Description

This bot detects all transactions of traded Jettons if transaction amount more than 3% of daily volume or 
more than 1k TON

### Supported Chains

- TON

### Alerts

- JETON-TRACKING-1
  - Fired when any Jetton transaction amount more than defined threshold 
  - Severity is always set to "low" 
  - Type is always set to "Medium" 
  - Low confidence labels (0.3) 
  - Metadata exposes the anomaly_score for the alert
  - Metadata will contain amount funded, the funded address