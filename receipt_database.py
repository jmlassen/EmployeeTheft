import re
from os import listdir
import numpy as np
from receipt_data_container import ReceiptDataContainer

FRAUDULENT_RECEIPT_DIRECTORY = "data/fraudulent_receipts/"
LEGITIMATE_RECEIPT_DIRECTORY = "data/legitimate_receipts/"
CUSTOMER_PATTERN = ".*Valued\sMember\s##\d{4}.*"
RECEIPT_TOTAL_PATTERN = "\*\*\*\sTotal\s*-\$\d{1,4}\."
TENDER_TYPE_PATTERN = "[A-Z]{2,5}\s+\-{0,1}\$\d+.\d+"
VOID_RECEIPT_PATTERN = "VOID\s+Subtotal\sVoid\s+V"
REGISTER_TRANSACTION_PATTERN = "Reg\s#"
TIMESTAMP_PATTERN = "\w+,\s\w+\s\d+,\s\d+\s\d+:\d+:\d+"
RECEIPT_CHANGE_TENDER_TEXT = "Change"


class ReceiptDatabase:
    def __init__(self):
        """Initialize regex patterns to be used when loading receipts. This should probably not be done this way, but
        I do not care that much to implement it differently.
        """
        self.customer_pattern = re.compile(CUSTOMER_PATTERN)
        self.receipt_total_pattern = re.compile(RECEIPT_TOTAL_PATTERN)
        self.tender_type_pattern = re.compile(TENDER_TYPE_PATTERN)
        self.void_receipt_pattern = re.compile(VOID_RECEIPT_PATTERN)
        self.timestamp_pattern = re.compile(TIMESTAMP_PATTERN)
        self.register_transaction_pattern = re.compile(REGISTER_TRANSACTION_PATTERN)

    def load_receipts(self):
        """Loads receipts on disk into memory.
        """
        receipts = []
        target = []
        self._load_receipts_in_directory(FRAUDULENT_RECEIPT_DIRECTORY, 'fraudulent', receipts, target)
        self._load_receipts_in_directory(LEGITIMATE_RECEIPT_DIRECTORY, 'legitimate', receipts, target)
        return ReceiptDataContainer(np.array(receipts), np.array(target))

    def _load_receipts_in_directory(self, directory, label, receipts, target):
        receipt_file_names = listdir(directory)
        for filename in receipt_file_names:
            receipt_filename = "{}{}".format(directory, filename)
            receipt_lines = self._get_receipt_lines(receipt_filename)
            receipt = self._objectify_receipt_from_lines(receipt_lines)
            if receipt is not None:
                receipts.append(receipt)
                target.append(label)

    def _get_receipt_lines(self, receipt_filename):
        """Reads a receipt file into an array of strings.
        """
        lines = []
        with open(receipt_filename) as file:
            for line in file:
                # Strip whitespace from line and append our array
                lines.append(line.rstrip().lstrip())
        return lines

    def _objectify_receipt_from_lines(self, receipt_lines):
        """Transforms receipt lines into an object.
        """
        cashier = None
        # transaction_time = None
        transaction_location = None
        # transaction_number = ""
        customer_entered = 0
        register_number = 0
        transaction_total = 0.0
        tenders = []
        for line in receipt_lines:
            # Check if line indicates receipt is void
            if self.void_receipt_pattern.match(line):
                return None
            # Check if line shows customer was entered
            if self.customer_pattern.match(line):
                customer_entered = 1
            # Check if line is receipt total
            if self.receipt_total_pattern.match(line):
                # Receipts are implied to have a negative total.
                transaction_total = -1 * float(line.split('$')[-1])
            # Check if line is tender
            if self.tender_type_pattern.match(line):
                tender = line.split(' ')[0]
                if not tender == RECEIPT_CHANGE_TENDER_TEXT:
                    tenders.append(tender)
            # Check if line is register cashier transaction
            if self.register_transaction_pattern.match(line):
                line_split = line.split(' ')
                register_number = int(line_split[2])
                transaction_location = int(register_number / 100)
                cashier = int(line_split[6])
                # transaction_number = line_split[9]
        # Quick workaround for the tender issue.
        if len(tenders) > 1 and "CASH" in tenders:
            tenders = "CASH"
        elif len(tenders) == 1:
            tenders = tenders[0]
        else:
            return None
        return [transaction_location, customer_entered, register_number, transaction_total, tenders]


if __name__ == '__main__':
    ReceiptDatabase().load_receipts()
