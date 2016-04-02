import numpy as np
from sklearn.metrics import accuracy_score
from sklearn.utils import shuffle
from sklearn.neighbors import KNeighborsClassifier

from receipt_database import ReceiptDatabase


def preprocess(data_set):
    tenders = list(np.unique(data_set.data[:, -1]))
    for point in data_set.data:
        point[-1] = tenders.index(point[-1])


class TestingFramework:
    def __init__(self, classifiers):
        self.classifiers = classifiers

    def run(self, data_set, cv, classifier_index):
        results = []
        return results.append(
            self._cross_val_score(self.classifiers[classifier_index], data_set.data, data_set.target, cv))

    def run_all(self, data_set, critical_value):
        overall_results = []
        for classifier in self.classifiers:
            preprocess(data_set)
            result = self._cross_val_score(classifier, data_set.data, data_set.target, critical_value)
            result = np.mean(result)
            overall_results.append(result)
        return overall_results

    def run_optimization_test(self):
        # Try bloating number of fraudulent records
        # for n_duplicate in range(0, 1000, 20):
        #     data_set = ReceiptDatabase().load_receipts(n_duplicate)
        #     preprocess(data_set)
        #     classifier = KNeighborsClassifier()
        #     accuracy = np.mean(self._cross_val_score(classifier, data_set.data, data_set.target, 7))
        #     with open('n_duplicate-test-knn.csv', "a") as file:
        #         file.write("{},{}\n".format(n_duplicate, accuracy))
        # Try different number of neighbors
        data_set = ReceiptDatabase().load_receipts()
        preprocess(data_set)
        for n_neighbors in range(1, 30):
            classifier = KNeighborsClassifier(n_neighbors=n_neighbors)
            accuracy = np.mean(self._cross_val_score(classifier, data_set.data, data_set.target, 7))
            with open('n_neighbors-test-knn.csv', "a") as file:
                file.write("{},{}\n".format(n_neighbors, accuracy))

    def predict(self, data_point, classifier_index=0):
        return self.classifiers[classifier_index].predict(data_point)[0]

    def _cross_val_score(self, classifier, data, target, cv):
        """Runs a cross validation test with a provided number of folds.

        :param classifier: The classifier we want to test, must have 'fit' and 'predict' methods implemented
        :param data:
        :param target:
        :param cv:
        :return:
        """
        data, target = shuffle(data, target)
        fold_len = int(len(data) / cv)
        results = []
        matrix = {}
        for i in range(cv):
            start_index = fold_len * i
            end_index = fold_len * (i + 1)
            train_data = np.concatenate((data[:start_index], data[end_index:]), axis=0)
            train_target = np.concatenate((target[:start_index], target[end_index:]), axis=0)
            classifier.fit(train_data, train_target)
            prediction = classifier.predict(data[start_index:end_index])
            accuracy = accuracy_score(target[start_index:end_index], prediction)
            # Calculate and print the confusion matrix
            self._print_confusion_matrix(prediction, target[start_index:end_index], matrix)
            results.append(accuracy)
        self._output_false_negatives(matrix)
        return np.array(results)

    def _print_confusion_matrix(self, prediction, target, matrix):
        for i in range(len(prediction)):
            if target[i] not in matrix:
                matrix[target[i]] = {}
            if prediction[i] not in matrix[target[i]]:
                matrix[target[i]][prediction[i]] = 1
            else:
                matrix[target[i]][prediction[i]] += 1

    def _output_false_negatives(self, matrix):
        with open('false-negatives-knn.csv', "a") as file:
            file.write("{}\n".format(int(matrix["fraudulent"]["legitimate"] / 7)))
