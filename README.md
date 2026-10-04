# Cloud-Pulse — IoT-Based Asset Security & Chain-of-Custody Framework

Cloud-Pulse is an IoT-based asset security and chain-of-custody system designed to monitor assets in real time, detect tampering or abnormal conditions, and maintain a digital history of asset-related events.

The project combines IoT sensing, cloud services, event processing, storage, alerting, and monitoring to provide a secure and traceable asset-monitoring workflow.

## Project Objective

The objective of Cloud-Pulse is to create a cloud-connected asset security system that can:

- Monitor asset-related sensor events in real time
- Detect tampering and abnormal conditions
- Process incoming IoT data in the cloud
- Maintain asset and event history
- Generate alerts when defined conditions occur
- Support secure tracking of asset custody and status

## System Architecture

```text
                    IoT / Sensor Events
                           |
                           v
                    AWS IoT Core
                           |
                    IoT Rules Engine
                           |
                           v
                    AWS Lambda
                    (Python Backend)
                      /        \
                     /          \
                    v            v
             DynamoDB           SNS
          Asset/Event Data    Alerts & Notifications
                    |
                    v
               CloudWatch
          Logging & Monitoring
AWS Cloud Backend

The cloud backend is built around an event-driven architecture.

AWS IoT Core

AWS IoT Core acts as the communication layer between IoT devices or test clients and the AWS cloud.

Example event types include:

Asset authentication
RFID scan
Tamper detection
Temperature readings
Location/GPS updates
Asset status changes

Example JSON event:
{
  "asset_id": "ASSET-001",
  "event_type": "tamper",
  "status": "detected"
}
AWS Lambda

AWS Lambda provides the serverless backend processing layer.

The Lambda backend processes incoming event data and performs the required cloud-side logic.

Python is used for the Lambda implementation.

Amazon DynamoDB

DynamoDB provides persistent storage for asset and event information.

The stored information can include:

Asset ID
Event type
Status
Timestamp
Sensor/event information

This provides a history of asset-related events.

Amazon SNS

Amazon SNS is used for security-related notifications.

When a relevant condition such as tampering or an abnormal threshold is detected, the backend can trigger an SNS notification.
Security Event
      |
      v
    Lambda
      |
      v
     SNS
      |
      v
    Alert
Amazon CloudWatch

CloudWatch provides monitoring and logging for the AWS backend.

It is used to observe backend activity and support troubleshooting.

Event Processing Flow
IoT / MQTT JSON Event
          |
          v
    AWS IoT Core
          |
          v
    IoT Rule / Routing
          |
          v
      Lambda
          |
     +----+----+
     |         |
     v         v
 DynamoDB     SNS
     |         |
     v         v
Event History Alert
     |
     v
 CloudWatch
Example Event Payloads
Asset Authentication
{
  "asset_id": "ASSET-001",
  "event_type": "authentication",
  "status": "authenticated"
}
Tamper Detection
{
  "asset_id": "ASSET-001",
  "event_type": "tamper",
  "status": "detected"
}
Temperature Monitoring
{
  "asset_id": "ASSET-001",
  "event_type": "temperature",
  "temperature": 38.5,
  "unit": "C"
}
Security

Security is an important part of the cloud architecture.

IAM permissions are designed around the principle of least privilege so that cloud components receive only the permissions required for their operations.

My Contribution

My primary contribution to Cloud-Pulse is the AWS cloud/backend implementation.

My work includes:

AWS cloud architecture
AWS IoT Core
Lambda backend development using Python
DynamoDB data storage
SNS notification flow
IAM permissions and access control
CloudWatch monitoring and logging
Testing cloud-side event processing using JSON/MQTT-style events

The hardware and sensor implementation is treated separately from the AWS backend documented in this repository.

Technologies Used
AWS
AWS IoT Core
AWS Lambda
Amazon DynamoDB
Amazon SNS
Amazon CloudWatch
AWS IAM
Backend
Python
JSON
MQTT
Key Cloud Concepts Demonstrated
Event-driven cloud architecture
IoT-to-cloud communication
Serverless computing
NoSQL data storage
Cloud-based alerting
IAM and least-privilege access
Cloud monitoring and logging
JSON event processing
Repository Structure
cloud-pulse/
│
├── README.md
│
├── lambda/
│   └── ...
│
├── sample-events/
│   ├── authentication.json
│   ├── tamper.json
│   └── temperature.json
│
└── docs/
    ├── architecture/
    └── screenshots/
Additional backend source code, sample event payloads, architecture documentation, and screenshots will be added as the project documentation is organized.

Project Status

This repository documents the AWS cloud/backend portion of the Cloud-Pulse academic project and my contribution to its implementation.

Author

Anjana J

Electronics & Communication Engineering
Jyothi Engineering College

GitHub: [Anjana-108](https://github.com/Anjana-108)
