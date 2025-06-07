# Python Console Stock Exchange

This project is a console-based demo stock exchange server that allows users to place buy and sell orders. It matches and fills orders based on price and quantity, providing a simple order book for tracking active orders and recent trades.

## Project Structure

```
python-console-stock-exchange
├── src
│   ├── main.py          # Entry point for the console-based demo stock exchange server
│   └── order_book.py    # Contains Order and OrderBook classes for managing orders
└── README.md            # Documentation for the project
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd python-console-stock-exchange
   ```

2. Ensure you have Python installed (version 3.6 or higher).

## Running the Server

To run the stock exchange server, navigate to the `src` directory and execute the following command:

```
python main.py
```

## Usage

Once the server is running, you can enter commands to place orders or view the order book and recent trades. The available commands are:

- `BUY <qty> <price>`: Place a buy order with the specified quantity and price.
- `SELL <qty> <price>`: Place a sell order with the specified quantity and price.
- `BOOK`: Display the current order book, showing active bids and asks.
- `TRADES`: Show the most recent trades that have been executed.
- `QUIT`: Exit the server.

## Example

```
> BUY 10 100.50
Order accepted: BUY #1 10@100.5
> SELL 5 99.00
Order accepted: SELL #2 5@99.0
> BOOK
Order Book:
BIDS:
  10@100.5 (#1)
ASKS:
  5@99.0 (#2)
> TRADES
Recent Trades:
```

## Features

- Supports placing buy and sell orders.
- Automatically matches orders based on price and quantity.
- Displays an order book with current bids and asks.
- Keeps a record of recent trades.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any enhancements or bug fixes.