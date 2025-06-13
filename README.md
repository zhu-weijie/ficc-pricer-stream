# FICC Pricer Stream

This project is a conceptual model of a distributed Fixed Income, Currency, and Commodities (FICC) pricing platform. It was built to demonstrate core software engineering principles relevant to high-performance, data-intensive financial systems.

The application simulates a complete, end-to-end, real-time data pipeline for a US Treasury Bond, from market data ingestion to pricing and final risk/P&L calculation.

## Architecture

The project uses a decoupled, multi-service architecture communicating asynchronously via a Redis Pub/Sub message broker. This is a common and effective pattern for building scalable and resilient distributed systems that are central to modern trading platforms.

```
[Market Data Publisher] --(yield)--> (Redis Channel: 'market-data')
                                                   |
                                                   v
                                          [Pricing Engine] --(price)--> (Redis Channel: 'price-stream')
                                                                                 |
                                                                                 v
                                                                          [Risk Client] --(displays P&L)--> (STDOUT / Console)
```

### Relevance to a Trading Platform

*   **Distributed Systems:** The project is a hands-on implementation of a microservice architecture, demonstrating asynchronous communication (`Pub/Sub`), service decoupling, and data flow management in a multi-component system.
*   **FICC Domain:** It models a core workflow for a Fixed Income product (a zero-coupon bond), showing a practical interest in and understanding of the problem space.
*   **Data-Intensive & Real-Time:** It simulates the handling of a continuous, real-time stream of data—a key challenge in any trading technology platform.
*   **Modern Practices & DevOps:** The entire application is containerized with Docker and orchestrated with Docker Compose. This demonstrates competency in modern DevOps tooling and ensures a one-command, reproducible setup.

## Tech Stack

*   **Language:** Python 3.13
*   **Messaging:** Redis (Pub/Sub)
*   **Infrastructure:** Docker & Docker Compose

## How to Run

Ensure you have Docker and Docker Compose installed on your system.

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/zhu-weijie/ficc-pricer-stream.git
    cd ficc-pricer-stream
    ```

2.  **Build and run the services:**
    From the root directory, execute the following command:
    ```bash
    docker compose up --build
    ```
    This command will build the Docker images for all three services, start the Redis container, and then start the services.

3.  **View the output:**
    You will see the interleaved logs from all three services in your terminal, showing the real-time data flow from publication to final P&L calculation.

4.  **To stop the application:**
    Press `Ctrl+C` in the terminal.

### Expected Output

You will see a live feed of logs from all three services. The flow will look similar to this, demonstrating the end-to-end pipeline in action:

```log
pricing_engine-1         | Pricing Engine starting...
market_data_publisher-1  | Market Data Publisher starting...
risk_client-1            | Risk/UI Client starting...
pricing_engine-1         | Successfully connected to Redis.
pricing_engine-1         | Subscribed to 'market-data' channel.
market_data_publisher-1  | Successfully connected to Redis.
market_data_publisher-1  | Published Yield: 0.0424
risk_client-1            | Successfully connected to Redis.
risk_client-1            | Subscribed to 'price-stream' channel.
market_data_publisher-1  | Published Yield: 0.0420
pricing_engine-1         | Received Yield 0.0420, Published Price: 66.26
risk_client-1            | PRICE UPDATE | Instrument: US10Y | Price:  66.26 | P&L: -0.24
market_data_publisher-1  | Published Yield: 0.0420
pricing_engine-1         | Received Yield 0.0420, Published Price: 66.26
risk_client-1            | PRICE UPDATE | Instrument: US10Y | Price:  66.26 | P&L: -0.24
market_data_publisher-1  | Published Yield: 0.0429
risk_client-1            | PRICE UPDATE | Instrument: US10Y | Price:  65.73 | P&L: -0.77
```
