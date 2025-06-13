# pricing_engine/engine.py
import redis
import json
import time
import os

def calculate_bond_price(bond_yield, years=10, face_value=100):
    """Calculates the price of a simple zero-coupon bond."""
    return face_value / ((1 + bond_yield) ** years)

def main():
    """Connects to Redis, subscribes to market data, and publishes prices."""
    redis_host = os.environ.get("REDIS_HOST", "redis")
    
    print("Pricing Engine starting...")

    while True:
        try:
            r = redis.Redis(host=redis_host, port=6379, db=0, decode_responses=True)
            r.ping()
            print("Successfully connected to Redis.")
            break
        except redis.exceptions.ConnectionError as e:
            print(f"Could not connect to Redis: {e}. Retrying in 5 seconds...")
            time.sleep(5)

    p = r.pubsub(ignore_subscribe_messages=True)

    p.subscribe('market-data')
    print("Subscribed to 'market-data' channel.")

    for message in p.listen():
        market_data = json.loads(message['data'])
        bond_yield = market_data['yield']

        price = calculate_bond_price(bond_yield)

        price_data = {
            'instrument': market_data['instrument'],
            'price': price,
            'market_timestamp': market_data['timestamp']
        }

        r.publish('price-stream', json.dumps(price_data))
        
        print(f"Received Yield {bond_yield:.4f}, Published Price: {price:.2f}")

if __name__ == '__main__':
    main()
