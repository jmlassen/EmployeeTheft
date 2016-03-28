import re
from os import listdir
from receipt import Receipt

RECEIPT_DIRECTORY = "data/"
CUSTOMER_PATTERN = ".*Valued\sMember\s##\d{4}.*"
RECEIPT_TOTAL_PATTERN = "\*\*\*\sTotal\s*-\$\d{1,4}\."
TENDER_TYPE_PATTERN = "\w+\s+\-{0,1}\$\d+\.\d+"
VOID_RECEIPT_PATTERN = "VOID\s+Subtotal\sVoid\s+V"


class ReceiptDatabase:
    def __init__(self):
        """Initialize regex patterns to be used when loading receipts. This should probably not be done this way, but
        I do not care that much to implement it differently.
        """
        self.customer_pattern = re.compile(CUSTOMER_PATTERN)
        self.receipt_total_pattern = re.compile(RECEIPT_TOTAL_PATTERN)
        self.tender_type_pattern = re.compile(TENDER_TYPE_PATTERN)
        self.void_receipt_pattern = re.compile(VOID_RECEIPT_PATTERN)

    def load_receipts(self):
        """Loads receipts on disk into memory.
        """
        receipts = []
        receipt_file_names = listdir(RECEIPT_DIRECTORY)
        for filename in receipt_file_names:
            receipt_filename = "{}{}".format(RECEIPT_DIRECTORY, filename)
            receipt_lines = self._get_receipt_lines(receipt_filename)
            receipt = self._objectify_receipt_from_lines(receipt_lines)
            receipts.append(receipt)
        return receipts

    def _get_receipt_lines(self, receipt_filename):
        """Reads a receipt file into an array of strings.
        """
        lines = []
        with open(receipt_filename) as file:
            for line in file:
                lines.append(line)
        return lines

    def _objectify_receipt_from_lines(self, receipt_lines):
        """Transforms receipt lines into an object.
        """
        cashier = ""
        transaction_start_time = None
        transaction_location = None
        transaction_number = ""
        customer_entered = False
        register_number = 0
        transaction_total = 0.0
        tenders = []
        for line in receipt_lines:
            pass
        return Receipt(cashier, transaction_start_time, transaction_location, transaction_number, customer_entered,
                       register_number, transaction_total, tenders)


if __name__ == '__main__':
    receipts = ReceiptDatabase().load_receipts()
