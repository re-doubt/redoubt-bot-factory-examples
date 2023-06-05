## DEXes Swaps Tracking

### Description

TThis bot detects all swaps on all DEXes (buy, sell, swap).

### Supported Chains

- TON

### Alerts

- DEX-SWAP-2
  - Fired when a swap is made using any DEX 
  - Severity is always set to "low" 
  - Type is always set to "Medium" 
  - Low confidence labels (0.3) 
  - Metadata exposes the anomaly_score for the alert
  - Metadata will contain amount funded, the funded address, as well as the name of the DEX