from sklearn.tree import DecisionTreeClassifier
from receipt_database import ReceiptDatabase
import numpy as np


def preprocess(data_set):
    tenders = list(np.unique(data_set.data[:, -1]))
    for point in data_set.data:
        point[-1] = tenders.index(point[-1])


def main():
    cv = 7

    # Create Receipt_Database
    rd = ReceiptDatabase()

    # Load receipts
    rdc = rd.load_receipts()

    preprocess(rdc)

    # Create Classifier
    dtc = DecisionTreeClassifier()

    # Train
    dtc.fit(rdc.data, rdc.target)

    while True:
        # Provide a user receipt file
        receipt_file = input("Please provide a user receipt file ('q' to quit) -> ")

        if receipt_file.lower() == 'q':
            break

        # Format file
        lines = rd._get_receipt_lines(receipt_file)
        receipt = rd._objectify_receipt_from_lines(lines)

        # Run test
        prediction = dtc.predict(receipt)[0]

        # Show prediction
        print("This receipt is {}".format(prediction))


if __name__ == '__main__':
    main()
