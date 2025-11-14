import asyncio
import json
import os
from datetime import datetime
from nats.aio.client import Client as NATS

async def main():
    nc = NATS()
    nats_url = os.getenv("NATS_URL", "nats://localhost:4222")
    log_file = os.getenv("LOG_FILE", "/logs/swarm.log")

    # Ensure log directory exists
    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    async def message_handler(msg):
        timestamp = datetime.utcnow().isoformat()
        data = msg.data.decode('utf-8') if isinstance(msg.data, bytes) else str(msg.data)
        log_entry = {
            "timestamp": timestamp,
            "subject": msg.subject,
            "data": data
        }
        with open(log_file, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')

    await nc.connect(nats_url)
    await nc.subscribe(">", cb=message_handler)

    print(f"Connected to NATS at {nats_url}, logging to {log_file}")

    # Keep the connection alive
    while True:
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())