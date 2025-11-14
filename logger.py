import asyncio
import json
import os
from datetime import datetime
from nats.aio.client import Client as NATS

async def message_handler(msg, log_file):
    timestamp = datetime.utcnow().isoformat()
    try:
        data = msg.data.decode('utf-8') if isinstance(msg.data, bytes) else str(msg.data)
    except UnicodeDecodeError:
        data = str(msg.data)  # Fallback to str representation
    log_entry = {
        "timestamp": timestamp,
        "subject": msg.subject,
        "data": data
    }
    with open(log_file, 'a') as f:
        f.write(json.dumps(log_entry) + '\n')

async def main():
    nc = NATS()
    nats_url = os.getenv("NATS_URL", "nats://localhost:4222")
    log_file = os.getenv("LOG_FILE", "/logs/swarm.log")

    # Ensure log directory exists
    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    await nc.connect(nats_url)
    await nc.subscribe(">", cb=lambda msg: message_handler(msg, log_file))

    print(f"Connected to NATS at {nats_url}, logging to {log_file}")

    # Keep the connection alive
    while True:
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())