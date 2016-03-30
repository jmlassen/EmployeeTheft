from random import shuffle
import numpy as np
from sklearn.metrics import accuracy_score


class TestingFramework:
    def __init__(self, classifiers, classifiers_preprocessors):
        self.classifiers = classifiers
        self.classifiers_preprocessors = classifiers_preprocessors

    def run(self, data_set, cv, classifier_index):
        results = []
        self.classifiers_preprocessors[classifier_index](data_set)
        return results.append(self._cross_val_score(self.classifiers[classifier_index], data_set.data, data_set.target, cv))
    
    def run_all(self, data_set, cv):
        overall_results = []
        for i in range(self.calssifiers.__len__()):
            self.classifiers_preprocessors[i](data_set)
            overall_results.append(self._cross_val_score(self.classifiers[i], data_set.data, data_set.target, cv))
        return overall_results

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
