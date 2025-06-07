import heapq
import itertools

class Order:
    _ids = itertools.count(1)
    def __init__(self, side, quantity, price, symbol):
        self.id = next(Order._ids)
        self.side = side
        self.order_quantity = quantity
        self.filled_quantity = 0
        self.remaining_quantity = quantity
        self.price = price
        self.symbol = symbol

    def __repr__(self):
        # Include symbol in the order representation
        return f"{self.symbol} {self.side.upper()} #{self.id} {self.remaining_quantity}/{self.order_quantity}@{self.price}"

class OrderBook:
    def __init__(self):
        # Changed from self.bids and self.asks to a dictionary holding books by symbol
        self.books_by_symbol = {} 
        self.trades = []

    def _get_or_create_book(self, symbol):
        """Helper to get or initialize the bid/ask heaps for a symbol."""
        if symbol not in self.books_by_symbol:
            self.books_by_symbol[symbol] = {'bids': [], 'asks': []} # Heaps store (-price, id, order) for bids, (price, id, order) for asks
        return self.books_by_symbol[symbol]

    def add_order(self, order):
        if order.side == 'buy':
            self.match_buy(order)
        else:
            # Consistently using 'order' as parameter name for the incoming order
            self.match_sell(order) 

    def match_buy(self, order): # incoming buy order
        book = self._get_or_create_book(order.symbol)
        asks_heap = book['asks']

        while order.remaining_quantity > 0 and asks_heap and \
              asks_heap[0][0] <= order.price: # asks_heap[0][0] is price
            
            best_ask_price, _, best_ask_order_obj = asks_heap[0] 
            
            executed_qty = min(order.remaining_quantity, best_ask_order_obj.remaining_quantity)
            self.trades.append(f"TRADE: {order.symbol} BUY {executed_qty}@{best_ask_price} (Buy #{order.id}, Sell #{best_ask_order_obj.id})")
            
            order.remaining_quantity -= executed_qty
            order.filled_quantity += executed_qty
            
            best_ask_order_obj.remaining_quantity -= executed_qty
            best_ask_order_obj.filled_quantity += executed_qty
            
            if best_ask_order_obj.remaining_quantity == 0:
                heapq.heappop(asks_heap)
            else:
                # Partial fill of the best ask, it remains on book
                break 
        
        if order.remaining_quantity > 0:
            heapq.heappush(book['bids'], (-order.price, order.id, order))

    def match_sell(self, order): # incoming sell order 
        book = self._get_or_create_book(order.symbol)
        bids_heap = book['bids']

        while order.remaining_quantity > 0 and bids_heap and \
              -bids_heap[0][0] >= order.price: # -bids_heap[0][0] is actual bid price
            
            best_bid_price_neg, _, best_bid_order_obj = bids_heap[0]
            actual_best_bid_price = -best_bid_price_neg
            
            executed_qty = min(order.remaining_quantity, best_bid_order_obj.remaining_quantity)
            self.trades.append(f"TRADE: {order.symbol} SELL {executed_qty}@{actual_best_bid_price} (Sell #{order.id}, Buy #{best_bid_order_obj.id})")

            order.remaining_quantity -= executed_qty
            order.filled_quantity += executed_qty

            best_bid_order_obj.remaining_quantity -= executed_qty
            best_bid_order_obj.filled_quantity += executed_qty
            
            if best_bid_order_obj.remaining_quantity == 0:
                heapq.heappop(bids_heap)
            else:
                # Partial fill of the best bid, it remains on book
                break
        
        if order.remaining_quantity > 0:
            heapq.heappush(book['asks'], (order.price, order.id, order))

    def show_book(self):
        print("\nOrder Book Blotter:")
        if not self.books_by_symbol:
            print("  (Empty)")
            return

        # Define column widths
        col_width_qty = 10
        col_width_price = 10

        for symbol, book_data in sorted(self.books_by_symbol.items()):
            print(f"\n--- {symbol} ---")
            header = f"{'BID':<{col_width_qty}} | {'PRICE':<{col_width_price}} | {'ASK':<{col_width_qty}}"
            print(header)
            print(f"{'-'*(col_width_qty)} | {'-'*(col_width_price)} | {'-'*(col_width_qty)}")

            bids_heap = book_data['bids']  # Heap items are (-price, id, order_obj)
            asks_heap = book_data['asks']  # Heap items are (price, id, order_obj)

            # Aggregate quantities by price level
            bid_levels = {}  # {price: total_remaining_quantity}
            for neg_price, _, order_obj in bids_heap:
                if order_obj.remaining_quantity > 0:
                    price = -neg_price
                    bid_levels[price] = bid_levels.get(price, 0) + order_obj.remaining_quantity
            
            ask_levels = {}  # {price: total_remaining_quantity}
            for price, _, order_obj in asks_heap:
                if order_obj.remaining_quantity > 0:
                    ask_levels[price] = ask_levels.get(price, 0) + order_obj.remaining_quantity

            # Get all unique price levels and sort them descending
            all_price_levels = sorted(list(set(bid_levels.keys()) | set(ask_levels.keys())), reverse=True)

            if not all_price_levels:
                print("  (No orders for this symbol)")
                print("-" * (col_width_qty * 2 + col_width_price + 6)) # Match header separator length
                continue

            for price_level in all_price_levels:
                bid_qty_str = str(bid_levels.get(price_level, ""))
                ask_qty_str = str(ask_levels.get(price_level, ""))
                # Format price to 2 decimal places, assuming prices can be floats
                price_str = f"{price_level:.2f}" 

                print(f"{bid_qty_str:<{col_width_qty}} | {price_str:<{col_width_price}} | {ask_qty_str:<{col_width_qty}}")
            
            print("-" * (col_width_qty * 2 + col_width_price + 6)) # Match header separator length

    def show_trades(self):
        print("\nRecent Trades:")
        if not self.trades:
            print("  (No trades yet)")
            return
        for trade in self.trades[-10:]: # Display last 10 trades
            print(" ", trade)
