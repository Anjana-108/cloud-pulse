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
| **IAM** | Separate permissions per function, listed below. |

**IAM permissions** (policy files are in [`iam/`](iam/)). Each custom policy is scoped to one resource:

| Function | Action | Resource |
|---|---|---|
| Write Lambda | `dynamodb:PutItem` | `CloudPulseAssets` table |
| Write Lambda | `sns:Publish` | `cloudpulse-alerts` topic |
| Read Lambda | `dynamodb:Scan` | `CloudPulseAssets` table |
| Both | CloudWatch Logs | AWS-managed `AWSLambdaBasicExecutionRole` |

## Test event

```json
{
  "asset_id": "A001",
  "rfid_id": "RF001",
  "status": "SECURE",
  "authentication": "AUTHENTICATED",
  "tamper": false,
  "temperature": 28.5,
  "latitude": 10.5276,
  "longitude": 76.2144,
  "timestamp": "2026-09-17T06:00:00Z"
}
```

An event with `"tamper": true` (status `TAMPER_ALERT`) triggers the SNS alert, which I received by email. The `/assets` endpoint returned the stored records as JSON.

## Evidence

| Component | Screenshot |
|---|---|
| IoT rule routing MQTT to Lambda | [View](docs/screenshots/iot-core-mqtt-rule.png) |
| Lambda test, status 200 | [View](docs/screenshots/lambda-test-success.png) |
| SNS tamper email | [View](docs/screenshots/sns-tamper-alert-email.png) |
| DynamoDB table | [View](docs/screenshots/dynamodb-table-cloudpulseassets.png) |
| Stored records | [View](docs/screenshots/dynamodb-scan-items.png) |
| IAM role for the write Lambda | [View](docs/screenshots/iam-lambda-role-permissions.png) |
| CloudWatch Lambda metrics | [View](docs/screenshots/lambda-monitor-metrics.png) |
| API Gateway response | [View](docs/screenshots/api-gateway-assets-response.png) |

## What I learned

- **Data types matter in DynamoDB.** It rejects Python floats, so the write Lambda converts numeric telemetry such as temperature and coordinates to `Decimal` before storing it.
- **Least privilege is designed per function.** Instead of one broad role, each Lambda has its own policy scoped to one resource. The write function can only `PutItem` on one table and `Publish` to one topic, and the read function can only `Scan` that table, so the public API cannot modify data or send alerts.
- **Separate read and write paths.** Splitting ingestion from retrieval kept the permissions small and let me test each path on its own.
- **Event-driven design.** An IoT Rule triggers the Lambda for each MQTT message, so there are no servers to run and each event is processed once.
- **Test the cloud without hardware.** Simulated JSON events let me validate the whole workflow, including the SNS email, before any physical sensor existed.
- **Know the design limits.** Because `asset_id` is the only key, the table keeps the latest state per asset rather than a full history. Adding a timestamp sort key is my next change.

## Limitations and next steps

| Limitation | Next step |
|---|---|
| The table keeps the **latest state per asset**, so earlier events are overwritten | Add `timestamp` as a sort key for full history |
| `/assets` has no authentication | Add an API key or authorizer |
| No CloudWatch alarms | Add alarms on Lambda errors |
| Built in the console | Define it in Terraform |
| Telemetry is simulated | Connect a real ESP32 |

## Author

**Anjana J** — Electronics & Communication Engineering, Jyothi Engineering College
Aspiring Cloud Engineer | AWS · [GitHub](https://github.com/Anjana-108)
