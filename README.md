# Cloud-Pulse — IoT Asset Security & Chain-of-Custody (AWS Backend)

An event-driven AWS backend for an IoT asset-security project. It receives asset telemetry, detects tampering, stores asset state, sends an email alert and serves the data through an API, using only serverless services.

I built and tested it with **simulated JSON/MQTT events**, so the cloud side did not depend on the physical sensor hardware.

## Architecture

![Cloud-Pulse Architecture](docs/cloudpulse-architecture.png)

**Write path:** simulated event → IoT Core → IoT Rule → Write Lambda → DynamoDB, plus an SNS email when `tamper` is `true`.
**Read path:** API Gateway → Read Lambda → DynamoDB → JSON response.

| Item | Value |
|---|---|
| Region | ap-south-1 (Mumbai) |
| MQTT topic | `cloudpulse/telemetry` |
| IoT Rule | `cloudpulse_mqtt_to_lambda` |
| Table | `CloudPulseAssets` (partition key `asset_id`, on-demand) |

## What I built

| Service | Role |
|---|---|
| **IoT Core** | MQTT entry point. An IoT Rule forwards each message to the write Lambda. |
| **Lambda (write)** | Validates `asset_id`, converts numbers to `Decimal`, stores the item, checks `tamper`, publishes the SNS alert. |
| **Lambda (read)** | Scans the table and returns the assets as JSON. |
| **DynamoDB** | Stores asset ID, status, temperature, tamper state, RFID ID, location and timestamp. |
| **SNS** | Sends tamper alerts to an email subscription. |
| **API Gateway** | `/assets` endpoint that invokes the read Lambda. |
| **CloudWatch** | Lambda logs and invocation, duration and error metrics. |
| **IAM** | Separate permissions per
