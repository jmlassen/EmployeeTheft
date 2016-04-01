import numpy as np
from sklearn.metrics import accuracy_score
from sklearn.utils import shuffle


class TestingFramework:
    def __init__(self, classifiers):
        self.classifiers = classifiers

    def run(self, data_set, cv, classifier_index):
        results = []
        return results.append(self._cross_val_score(self.classifiers[classifier_index], data_set.data, data_set.target, cv))

    def run_all(self, data_set, cv):
        overall_results = []
        for i in range(self.classifiers.__len__()):
            result = self._cross_val_score(self.classifiers[i], data_set.data, data_set.target, cv)
            result = np.mean(result)
            overall_results.append(result)
        return overall_results

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
        for i in range(cv):
            start_index = fold_len * i
            end_index = fold_len * (i + 1)
            train_data = np.concatenate((data[:start_index], data[end_index:]), axis=0)
            train_target = np.concatenate((target[:start_index], target[end_index:]), axis=0)
            classifier.fit(train_data, train_target)
            prediction = classifier.predict(data[start_index:end_index])
            accuracy = accuracy_score(target[start_index:end_index], prediction)
            results.append(accuracy)
        return np.array(results)
