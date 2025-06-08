from order_book import OrderBook
from order_book import Order
import random # Import random for generating quantities

def run_sony_exhaust_simulation(ob: OrderBook):
    """
    Runs a simulation to exhaust bids and asks for the SONY symbol.
    Prints the order book and waits for Enter after each simulated order.
    """
    print("\n--- Starting SONY Exhaustion Simulation ---")
    symbol_to_simulate = "SONY"

    # --- Part 1: Exhaust Asks for SONY ---
    print(f"\n--- Simulating: Exhausting ASKS for {symbol_to_simulate} ---")
    while True:
        sony_book_data = ob.books_by_symbol.get(symbol_to_simulate)
        if not sony_book_data or not sony_book_data['asks']:
            print(f"No more ASKS for {symbol_to_simulate} to exhaust.")
            break
        
        # Peek at the best ask (lowest price sell order)
        # asks_heap stores (price, id, order_obj)
        best_ask_price, _, best_ask_order_obj = sony_book_data['asks'][0]
        
        print(f"\nSim: Current best ASK for {symbol_to_simulate}: {best_ask_order_obj}")
        print(f"Sim: Placing BUY order to match this ASK: Qty={best_ask_order_obj.remaining_quantity}, Price={best_ask_price}")
        
        sim_buy_order = Order(
            side="buy",
            quantity=best_ask_order_obj.remaining_quantity,
            price=best_ask_price, # Match the exact price to hit this specific order
            symbol=symbol_to_simulate
        )
        ob.add_order(sim_buy_order)
        
        print(f"Sim: Order {sim_buy_order} placed.")
        ob.show_book(symbol_to_simulate) # Pass symbol_to_simulate
        ob.show_trades()
        input("Press Enter to continue simulation...")

    # --- Part 2: Exhaust Bids for SONY ---
    print(f"\n--- Simulating: Exhausting BIDS for {symbol_to_simulate} ---")
    while True:
        sony_book_data = ob.books_by_symbol.get(symbol_to_simulate)
        if not sony_book_data or not sony_book_data['bids']:
            print(f"No more BIDS for {symbol_to_simulate} to exhaust.")
            break

        # Peek at the best bid (highest price buy order)
        # bids_heap stores (-price, id, order_obj)
        best_bid_neg_price, _, best_bid_order_obj = sony_book_data['bids'][0]
        actual_best_bid_price = -best_bid_neg_price

        print(f"\nSim: Current best BID for {symbol_to_simulate}: {best_bid_order_obj}")
        print(f"Sim: Placing SELL order to match this BID: Qty={best_bid_order_obj.remaining_quantity}, Price={actual_best_bid_price}")

        sim_sell_order = Order(
            side="sell",
            quantity=best_bid_order_obj.remaining_quantity,
            price=actual_best_bid_price, # Match the exact price
            symbol=symbol_to_simulate
        )
        ob.add_order(sim_sell_order)

        print(f"Sim: Order {sim_sell_order} placed.")
        ob.show_book(symbol_to_simulate) # Pass symbol_to_simulate
        ob.show_trades()
        input("Press Enter to continue simulation...")
    
    print("\n--- SONY Exhaustion Simulation Finished ---")


def main():
    """
    Runs the command-line interface for the stock exchange.
    Initializes the order book, pre-populates it with some orders,
    and then enters a loop to accept and process user commands.
    """
    ob = OrderBook()
    print("Demo Stock Exchange")

    # --- Pre-populate Order Book ---
    initial_symbols = ["SONY", "TM", "HMC"]
    min_qty = 50
    max_qty = 200

    print("Pre-populating order book...")
    for symbol in initial_symbols:
        # Create sell orders (asks)
        for price in range(101, 111): # Prices 101 to 110
            qty = random.randint(min_qty, max_qty)
            order = Order(side="sell", quantity=qty, price=float(price), symbol=symbol)
            ob.add_order(order)
        
        # Create buy orders (bids)
        for price in range(90, 100): # Prices 90 to 99
            qty = random.randint(min_qty, max_qty)
            order = Order(side="buy", quantity=qty, price=float(price), symbol=symbol)
            ob.add_order(order)

        # Orders at price 100
        qty_sell_100 = random.randint(min_qty, max_qty)
        order_sell_100 = Order(side="sell", quantity=qty_sell_100, price=100.0, symbol=symbol)
        ob.add_order(order_sell_100)
        
        qty_buy_100 = random.randint(min_qty, max_qty)
        order_buy_100 = Order(side="buy", quantity=qty_buy_100, price=100.0, symbol=symbol)
        ob.add_order(order_buy_100)
    print("Order book pre-populated.")
    # --- End of Pre-population ---

    help_message = "Commands: <BUY|B> [symbol] <qty> <price>, <SELL|S> [symbol] <qty> <price>, BOOK [symbol], TRADES, ALLTRADES, POS, HELP, SIMSONY, QUIT. Default symbol: SONY"
    print(help_message) # Print help message once at the start
    
    default_symbol = "SONY"

    while True:
        cmd_input = input("> ").strip()
        if not cmd_input:
            continue
            
        parts = cmd_input.split()
        command_action = parts[0].upper() 

        if command_action == "QUIT":
            break
        elif command_action == "BOOK":
            if len(parts) > 1:
                symbol_to_show = parts[1].upper()
                ob.show_book(symbol_to_show)
            else:
                ob.show_book()
        elif command_action == "TRADES":
            ob.show_trades() 
        elif command_action == "ALLTRADES": 
            ob.show_trades(show_all=True)
        elif command_action == "POS": # Changed from POSITIONS to POS
            ob.show_positions()
        elif command_action == "HELP": 
            print(help_message)
        elif command_action == "SIMSONY":
            run_sony_exhaust_simulation(ob)
        elif command_action in ("BUY", "B", "SELL", "S"):
            side = "buy" if command_action in ("BUY", "B") else "sell"
            
            params = parts[1:] # Parameters after the command token
            
            current_symbol = default_symbol # Default symbol
            qty_str, price_str = None, None

            if len(params) == 2: # Format: <CMD> <qty> <price>
                qty_str, price_str = params[0], params[1]
            elif len(params) == 3: # Format: <CMD> <symbol> <qty> <price>
                current_symbol = params[0].upper() 
                qty_str, price_str = params[1], params[2]
            else:
                print(f"Invalid order format. Use: <{command_action}> [symbol] <qty> <price>")
                continue
                        
            try:
                qty = int(qty_str)
                price = float(price_str)
                if qty <= 0 or price <= 0:
                     print("Quantity and price must be positive.")
                     continue
            except ValueError:
                print("Invalid quantity or price format.")
                continue
            
            order = Order(side=side, quantity=qty, price=price, symbol=current_symbol)
            ob.add_order(order)
            print(f"Order accepted: {order}")
        else:
            print("Unknown command. Type HELP for options.")
            continue

if __name__ == "__main__":
    main()