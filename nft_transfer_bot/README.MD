## NFT Sales Tracking Bot

### Description

This bot detects NFT Sales and throw additional alert for Fragment sales. By  itself, this bot  will be  
quite noisy.

### Supported Chains

- TON

### Alerts

- NFT-SALES-1
  - Fired when any NFT sold 
  - Severity is always set to "low" (mention any conditions where it could be something else)
  - Type is always set to "suspicious" (mention any conditions where it could be something else)
  - Mention any other type of metadata fields included with this alert
  - Low confidence labels (0.3) for attacker address are emitted
  - Metadata exposes the anomaly_score for the alert
  - Metadata will contain amount funded, the nft, collection and marketplace address
