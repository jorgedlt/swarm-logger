# Swarm-Logger Agent

## Role
The swarm-logger is the dedicated logging agent for the swarm ecosystem. Its purpose is to capture, record, and store every event that flows across the NATS subjects without filtering, altering, or interpreting the messages. It provides observability, auditability, and long-term traceability of system events.

## Responsibilities
- Subscribe broadly to all NATS subjects using wildcard (`>`)
- Log messages in a consistent JSON format to durable storage
- Maintain stability and reliability without introducing backpressure
- Handle reconnections automatically
- Ensure no modification or analysis of messages

## Directory Structure
- `logger.py`: Main Python script for the logging agent
- `requirements.txt`: Python dependencies (nats-py)
- `Dockerfile`: Docker container definition based on python:3.11-slim
- `README.md`: Project overview, setup, and usage instructions
- `AGENT.md`: This file with agent-specific details
- `.gitignore`: Excludes sensitive and unnecessary files from version control

## Operational Notes
- **Dependencies**: Requires NATS server for message subscription
- **Environment Variables**:
  - `NATS_URL`: URL of the NATS server (default: nats://localhost:4222)
  - `LOG_FILE`: Path to the log file (default: /logs/swarm.log)
- **Storage**: Logs are written to a file in JSON lines format. Use Docker volumes for persistence.
- **Message Format**: Each log entry is a JSON object with `timestamp` (ISO format), `subject`, and `data` (stringified message data)
- **Reliability**: Uses asyncio for non-blocking operations and automatic NATS reconnections
- **Integration**: Part of the larger swarm ecosystem; communicates only via NATS subscription (no publishing)

## Assumptions
- NATS server is stable and accessible
- Log directory is writable and has sufficient space
- Messages are UTF-8 encodable; binary data is stringified

## Future Considerations
- Potential for log rotation or external storage integration
- Monitoring of log file size and health