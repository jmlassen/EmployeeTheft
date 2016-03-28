class Receipt:
    def __init__(self, cashier, transaction_start_time, transaction_location, transaction_number,
                 customer_entered, register_number, transaction_total, tenders):
        self.cashier = cashier
        self.transaction_start_time = transaction_start_time
        self.transaction_location = transaction_location
        self.transaction_number = transaction_number
        self.customer_entered = customer_entered
        self.register_number = register_number
        self.transaction_total = transaction_total
        self.tenders = tenders
