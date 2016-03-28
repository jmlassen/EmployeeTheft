import os
from os import listdir

from receipt import Receipt

RECEIPT_DIRECTORY = "data/"


class ReceiptDatabase:
    def load_receipts(self):
        """Loads receipts on disk into memory.
        """
        receipts = []
        receipt_filenames = listdir(RECEIPT_DIRECTORY)
        for filename in receipt_filenames:
            receipt_filename = "{}{}".format(RECEIPT_DIRECTORY, filename)
            receipt_lines = self._get_receipt_lines(receipt_filename)
            receipt = self._objectify_receipt_from_lines(receipt_lines)
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
        return Receipt()


if __name__ == '__main__':
    receipts = ReceiptDatabase().load_receipts()
