# risk_client/client.py
import redis
import json
import time
import os

def main():
    """Connects to Redis, subscribes to price stream, and displays P&L."""
    redis_host = os.environ.get("REDIS_HOST", "redis")
    
    print("Risk/UI Client starting...")

    while True:
        try:
            r = redis.Redis(host=redis_host, port=6379, db=0, decode_responses=True)
            r.ping()
            print("Successfully connected to Redis.")
            break
        except redis.exceptions.ConnectionError as e:
            print(f"Could not connect to Redis: {e}. Retrying in 5 seconds...")
            time.sleep(5)

    ENTRY_PRICE = 66.50 

    p = r.pubsub(ignore_subscribe_messages=True)
    p.subscribe('price-stream')
    print("Subscribed to 'price-stream' channel.")

    for message in p.listen():
        price_data = json.loads(message['data'])
        current_price = price_data['price']
        
        pnl = current_price - ENTRY_PRICE

        instrument = price_data['instrument']
        print(
            f"PRICE UPDATE | "
            f"Instrument: {instrument} | "
            f"Price: {current_price:6.2f} | "
            f"P&L: {pnl:+.2f}"
        )

if __name__ == '__main__':
    main()
