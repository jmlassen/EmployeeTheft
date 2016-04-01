from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC

from testing_framework import TestingFramework

class Driver:
    def __init__(self):
        pass

    def run_accuracy_test(self):
        # Create a list of classifiers
        nb = GaussianNB()
        svm = SVC()
        knc = KNeighborsClassifier()

        classifiers = [nb, svm, knc]

        # Create testing framework
        tf = TestingFramework(classifiers)

        # Run all classifiers

        # Show accuracy of each classifier
        pass


def main():
    pass

if __name__ == "__main__":
    main()
