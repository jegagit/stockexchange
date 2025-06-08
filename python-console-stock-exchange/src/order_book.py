import heapq
import itertools

class Order:
    """
    Represents a single buy or sell order in the stock exchange.
    """
    _ids = itertools.count(1)
    def __init__(self, side, quantity, price, symbol):
        """
        Initializes a new Order.

        Args:
            side (str): The side of the order ('buy' or 'sell').
            quantity (int): The total quantity of the order.
            price (float): The price of the order.
            symbol (str): The stock symbol for the order.
        """
        self.id = next(Order._ids)
        self.side = side
        self.order_quantity = quantity
        self.filled_quantity = 0
        self.remaining_quantity = quantity
        self.price = price
        self.symbol = symbol

    def __repr__(self):
        """
        Returns a string representation of the Order.
        """
        # Include symbol in the order representation
        return f"{self.symbol} {self.side.upper()} #{self.id} {self.remaining_quantity}/{self.order_quantity}@{self.price}"

class OrderBook:
    """
    Manages the collection of buy and sell orders for various stock symbols.
    It facilitates matching of orders and maintains a record of trades.
    """
    def __init__(self):
        """
        Initializes a new OrderBook.
        It sets up a dictionary to hold order books for each symbol, a list for trades,
        and a dictionary to track net market positions for each symbol.
        """
        self.books_by_symbol = {} 
        self.trades = []
        self.market_positions = {} # symbol: net_quantity

    def _get_or_create_book(self, symbol):
        """
        Retrieves or creates the order book (bids and asks heaps) for a given symbol.

        Args:
            symbol (str): The stock symbol.

        Returns:
            dict: A dictionary containing 'bids' and 'asks' heaps for the symbol.
        """
        if symbol not in self.books_by_symbol:
            self.books_by_symbol[symbol] = {'bids': [], 'asks': []}
        return self.books_by_symbol[symbol]

    def add_order(self, order):
        """
        Adds a new order to the order book and attempts to match it.

        Args:
            order (Order): The order to add.
        """
        if order.side == 'buy':
            self.match_buy(order)
        else:
            self.match_sell(order) 

    def match_buy(self, order): # incoming buy order
        """
        Matches an incoming buy order against existing sell orders (asks) for the same symbol.
        If the order is not fully filled, it's added to the bids for its symbol.
        Updates market positions based on executed trades.

        Args:
            order (Order): The incoming buy order.
        """
        book = self._get_or_create_book(order.symbol)
        asks_heap = book['asks']
        symbol = order.symbol # Get symbol for position tracking

        while order.remaining_quantity > 0 and asks_heap and \
              asks_heap[0][0] <= order.price: 
            
            best_ask_price, _, best_ask_order_obj = asks_heap[0] 
            
            executed_qty = min(order.remaining_quantity, best_ask_order_obj.remaining_quantity)
            self.trades.append(f"TRADE: {symbol} BUY {executed_qty}@{best_ask_price} (Buy #{order.id}, Sell #{best_ask_order_obj.id})")
            
            # Update market position: market sold 'executed_qty' of 'symbol'
            self.market_positions[symbol] = self.market_positions.get(symbol, 0) - executed_qty

            order.remaining_quantity -= executed_qty
            order.filled_quantity += executed_qty
            
            best_ask_order_obj.remaining_quantity -= executed_qty
            best_ask_order_obj.filled_quantity += executed_qty
            
            if best_ask_order_obj.remaining_quantity == 0:
                heapq.heappop(asks_heap)
            else:
                break 
        
        if order.remaining_quantity > 0:
            heapq.heappush(book['bids'], (-order.price, order.id, order))

    def match_sell(self, order): # incoming sell order 
        """
        Matches an incoming sell order against existing buy orders (bids) for the same symbol.
        If the order is not fully filled, it's added to the asks for its symbol.
        Updates market positions based on executed trades.

        Args:
            order (Order): The incoming sell order.
        """
        book = self._get_or_create_book(order.symbol)
        bids_heap = book['bids']
        symbol = order.symbol # Get symbol for position tracking

        while order.remaining_quantity > 0 and bids_heap and \
              -bids_heap[0][0] >= order.price: 
            
            best_bid_price_neg, _, best_bid_order_obj = bids_heap[0]
            actual_best_bid_price = -best_bid_price_neg
            
            executed_qty = min(order.remaining_quantity, best_bid_order_obj.remaining_quantity)
            self.trades.append(f"TRADE: {symbol} SELL {executed_qty}@{actual_best_bid_price} (Sell #{order.id}, Buy #{best_bid_order_obj.id})")

            # Update market position: market bought 'executed_qty' of 'symbol'
            self.market_positions[symbol] = self.market_positions.get(symbol, 0) + executed_qty

            order.remaining_quantity -= executed_qty
            order.filled_quantity += executed_qty

            best_bid_order_obj.remaining_quantity -= executed_qty
            best_bid_order_obj.filled_quantity += executed_qty
            
            if best_bid_order_obj.remaining_quantity == 0:
                heapq.heappop(bids_heap)
            else:
                break
        
        if order.remaining_quantity > 0:
            heapq.heappush(book['asks'], (order.price, order.id, order))

    def show_book(self, symbol_filter=None):
        """
        Displays the current state of the order book,
        formatted as a blotter with BID, PRICE, and ASK columns.
        If symbol_filter is provided, only shows the book for that symbol.

        Args:
            symbol_filter (str, optional): The specific symbol to display.
                                           If None, displays all symbols.
        """
        print("\nOrder Book Blotter:")

        books_to_display = {}
        if symbol_filter:
            symbol_filter_upper = symbol_filter.upper()
            if symbol_filter_upper in self.books_by_symbol:
                books_to_display = {symbol_filter_upper: self.books_by_symbol[symbol_filter_upper]}
            else:
                print(f"  (No order book found for symbol: {symbol_filter_upper})")
                return
        else:
            books_to_display = self.books_by_symbol

        if not books_to_display:
            # This case handles when self.books_by_symbol is empty and no filter is applied,
            # or when a filter is applied but results in no books to display (already handled above).
            if not self.books_by_symbol: # Check if the main book is empty
                 print("  (Empty)")
            return

        # Define column widths
        col_width_qty = 10
        col_width_price = 10

        for symbol, book_data in sorted(books_to_display.items()):
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

    def show_trades(self, show_all=False):
        """
        Displays trades recorded in the order book.
        By default, shows the last 10 trades.

        Args:
            show_all (bool, optional): If True, displays all trades. 
                                       Otherwise, displays the last 10 trades. 
                                       Defaults to False.
        """
        if show_all:
            print("\nAll Trades:")
        else:
            print("\nRecent Trades (last 10):")

        if not self.trades:
            print("  (No trades yet)")
            return
        
        trades_to_show = self.trades if show_all else self.trades[-10:]
        
        for trade in trades_to_show:
            print(" ", trade)

    def show_positions(self):
        """
        Displays the net market position for each symbol
        based on directly tracked positions.
        A positive position means the market has bought more than it sold.
        A negative position means the market has sold more than it bought.
        """
        print("\nNet Market Positions:")
        if not self.market_positions:
            print("  (No trades executed yet or no net positions)")
            return

        for symbol, net_qty in sorted(self.market_positions.items()):
            print(f"  {symbol}: {net_qty}")
