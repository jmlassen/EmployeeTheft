from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

from testing_framework import TestingFramework
from receipt_database import ReceiptDatabase


class Driver:
    classifiers_names = [
        # "Naive Bayes",
        "Support Vector Machines",
        "K Nearest Neighbors",
        "Decision Tree"
    ]
    classifiers = [
        # GaussianNB(),
        SVC(),
        KNeighborsClassifier(),
        DecisionTreeClassifier()
    ]

    def __init__(self):
        pass

    def run_accuracy_test(self):
        # Create testing framework
        testing_framework = TestingFramework(self.classifiers)

        # Run all classifiers
        testing_framework.run_optimization_test()

        # Show accuracy of each classifier
        # for index in range(0, len(self.classifiers_names)):
        #     print(self.classifiers_names[index] + " Accuracy: {}".format(accuracies[index]))


def main():
    # Create Receipt_Database
    # rd = ReceiptDatabase()

    # Load receipts
    # rdc = rd.load_receipts()

    Driver().run_accuracy_test()


if __name__ == "__main__":
    main()
