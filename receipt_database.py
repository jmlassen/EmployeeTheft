from os import listdir

RECEIPT_DIRECTORY = "data/"


class ReceiptDatabase:
    def load_receipts(self):
        """Loads receipts on disk into memory.
        """
        receipts = []
        receipt_filenames = []
        print(listdir(RECEIPT_DIRECTORY))


if __name__ == '__main__':
    ReceiptDatabase().load_receipts()