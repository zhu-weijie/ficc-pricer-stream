# market_data_publisher/publisher.py
import redis
import time
import random
import json
import os

def main():
    """Connects to Redis and enters an infinite loop to publish market data."""

    redis_host = os.environ.get("REDIS_HOST", "redis")
    
    print("Market Data Publisher starting...")
    
    while True:
        try:
            r = redis.Redis(host=redis_host, port=6379, db=0, decode_responses=True)
            r.ping()
            print("Successfully connected to Redis.")
            break
        except redis.exceptions.ConnectionError as e:
            print(f"Could not connect to Redis: {e}. Retrying in 5 seconds...")
            time.sleep(5)

    base_yield = 0.0425

    while True:
        yield_change = random.uniform(-0.0005, 0.0005)
        current_yield = base_yield + yield_change

        market_data = {
            'instrument': 'US10Y',
            'timestamp': time.time(),
            'yield': current_yield
        }

        payload = json.dumps(market_data)

        r.publish('market-data', payload)
        
        print(f"Published Yield: {current_yield:.4f}")

        time.sleep(random.uniform(0.5, 1.5))

if __name__ == '__main__':
    main()
