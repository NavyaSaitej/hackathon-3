import asyncio
import httpx
import logging
import json
import time
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - Eval Subagent - %(message)s')

CONFIG_FILE = "agentic_workflow/eval_config.json"

def load_config():
    if not os.path.exists(CONFIG_FILE):
        return {"url": "http://127.0.0.1:8000/health", "payload": {}, "headers": {}, "workers": 5, "interval": 60}
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

async def make_request(client, config, worker_id):
    start = time.time()
    try:
        method = "POST" if config.get("payload") else "GET"
        if method == "POST":
            response = await client.post(config["url"], json=config["payload"], headers=config.get("headers", {}), timeout=30.0)
        else:
            response = await client.get(config["url"], headers=config.get("headers", {}), timeout=30.0)
            
        elapsed = time.time() - start
        
        if response.status_code == 200:
            logging.info(f"Worker {worker_id}: Success in {elapsed:.2f}s")
        elif response.status_code == 429:
            logging.warning(f"Worker {worker_id}: Rate limited (429) in {elapsed:.2f}s (Expected under load)")
        else:
            logging.error(f"Worker {worker_id}: Failed with HTTP {response.status_code}")
            
    except Exception as e:
        logging.error(f"Worker {worker_id}: Exception occurred: {e}")

async def eval_round(config):
    workers = config.get("workers", 5)
    logging.info(f"Starting Eval round with {workers} concurrent requests to {config['url']}...")
    async with httpx.AsyncClient() as client:
        tasks = [make_request(client, config, i) for i in range(workers)]
        await asyncio.gather(*tasks)
    logging.info("Eval round complete.")

async def loop():
    while True:
        config = load_config()
        await eval_round(config)
        interval = config.get("interval", 60)
        logging.info(f"Sleeping for {interval} seconds before next round...")
        await asyncio.sleep(interval)

if __name__ == "__main__":
    asyncio.run(loop())
