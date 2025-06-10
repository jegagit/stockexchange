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
    
Demo Stock Exchange
Pre-populating order book...
Order book pre-populated.
Commands: <BUY|B> [symbol] <qty> <price>, <SELL|S> [symbol] <qty> <price>, BOOK [symbol], TRADES, ALLTRADES, POS, HELP, SIMSONY, QUIT. Default symbol: SONY
> 
B hsbc 1000 100
Order accepted: HSBC BUY #67 1000/1000@100.0
> 
S hsbc 1000 100
Order accepted: HSBC SELL #68 0/1000@100.0
> 
ALLTRADES

All Trades:
  TRADE: SONY BUY 58@100.0 (Buy #22, Sell #21)
  TRADE: TM BUY 54@100.0 (Buy #44, Sell #43)
  TRADE: HMC BUY 145@100.0 (Buy #66, Sell #65)
  TRADE: HSBC SELL 1000@100.0 (Sell #68, Buy #67)
> 
POS

Net Market Positions:
  HMC: -145
  HSBC: 1000
  SONY: -58
  TM: -54
> 
SIMSONY

--- Starting SONY Exhaustion Simulation ---

--- Simulating: Exhausting ASKS for SONY ---

Sim: Current best ASK for SONY: SONY SELL #21 135/193@100.0
Sim: Placing BUY order to match this ASK: Qty=135, Price=100.0
Sim: Order SONY BUY #69 0/135@100.0 placed.

Order Book Blotter:

--- SONY ---
BID        | PRICE      | ASK       
---------- | ---------- | ----------
           | 110.00     | 96        
           | 109.00     | 145       
           | 108.00     | 190       
           | 107.00     | 121       
           | 106.00     | 61        
           | 105.00     | 146       
           | 104.00     | 180       
           | 103.00     | 188       
           | 102.00     | 144       
           | 101.00     | 141       
182        | 99.00      |           
95         | 98.00      |           
141        | 97.00      |           
133        | 96.00      |           
124        | 95.00      |           
128        | 94.00      |           
128        | 93.00      |           
70         | 92.00      |           
123        | 91.00      |           
155        | 90.00      |           
------------------------------------

Recent Trades (last 10):
  TRADE: SONY BUY 58@100.0 (Buy #22, Sell #21)
  TRADE: TM BUY 54@100.0 (Buy #44, Sell #43)
  TRADE: HMC BUY 145@100.0 (Buy #66, Sell #65)
  TRADE: HSBC SELL 1000@100.0 (Sell #68, Buy #67)
  TRADE: SONY BUY 135@100.0 (Buy #69, Sell #21)
Press Enter to continue simulation...


Sim: Current best ASK for SONY: SONY SELL #1 141/141@101.0
Sim: Placing BUY order to match this ASK: Qty=141, Price=101.0
Sim: Order SONY BUY #70 0/141@101.0 placed.

Order Book Blotter:

--- SONY ---
BID        | PRICE      | ASK       
---------- | ---------- | ----------
           | 110.00     | 96        
           | 109.00     | 145       
           | 108.00     | 190       
           | 107.00     | 121       
           | 106.00     | 61        
           | 105.00     | 146       
           | 104.00     | 180       
           | 103.00     | 188       
           | 102.00     | 144       
182        | 99.00      |           
95         | 98.00      |           
141        | 97.00      |           
133        | 96.00      |           
124        | 95.00      |           
128        | 94.00      |           
128        | 93.00      |           
70         | 92.00      |           
123        | 91.00      |           
155        | 90.00      |           
------------------------------------

Recent Trades (last 10):
  TRADE: SONY BUY 58@100.0 (Buy #22, Sell #21)
  TRADE: TM BUY 54@100.0 (Buy #44, Sell #43)
  TRADE: HMC BUY 145@100.0 (Buy #66, Sell #65)
  TRADE: HSBC SELL 1000@100.0 (Sell #68, Buy #67)
  TRADE: SONY BUY 135@100.0 (Buy #69, Sell #21)
  TRADE: SONY BUY 141@101.0 (Buy #70, Sell #1)```

## Features

- Supports placing buy and sell orders.
- Automatically matches orders based on price and quantity.
- Displays an order book with current bids and asks.
- Keeps a record of recent trades.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any enhancements or bug fixes.
