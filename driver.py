from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC

from testing_framework import TestingFramework


class Driver:
    classifiers = {
        "Naive Bayes": GaussianNB(),
        "Support Vector Machines": SVC(),
        "K Nearest Neighbors": KNeighborsClassifier()
    }

    def __init__(self):
        pass

    def run_accuracy_test(self, data_set):
        # Create testing framework
        tf = TestingFramework(self.classifiers)

        # Run all classifiers
        accuracies = tf.run_all(data_set, 7)

        # Show accuracy of each classifier
        index = 0
        for key, value in self.classifiers.items():
            print(key + " Accuracy: {}%".format(accuracies[index]))
            index += 1


def main():
    pass

if __name__ == "__main__":
    main()
