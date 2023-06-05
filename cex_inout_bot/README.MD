## CEX Funding Bot

### Description

This bot detects transactions with large TON native transfers in/out CEXes (>25k TON).

### Supported Chains

- TON

### Alerts

- CEX-FUNDING
  - Fired when a funding transaction is made using native asset 
  - Severity is always set to "low" 
  - Type is always set to "suspicious" 
  - Low confidence labels (0.3) 
  - Metadata exposes the anomaly_score for the alert
  - Metadata will contain amount funded, the funded address, as well as the name of the CEX