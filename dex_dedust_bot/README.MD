## DeDust Swaps Tracking

### Description

This bot detects all swaps on DeDust DEX (buy, sell, swap).

### Supported Chains

- TON

### Alerts

- DEX-SWAP-1
  - Fired when a swap is made using DeDust 
  - Severity is always set to "low" 
  - Type is always set to "Medium" 
  - Low confidence labels (0.3) 
  - Metadata exposes the anomaly_score for the alert
  - Metadata will contain amount funded, the funded address, as well as the name of the DEX