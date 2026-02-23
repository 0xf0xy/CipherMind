"""
MIT License

Copyright (c) 2026 0xf0xy

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import pickle
import json


class MultinomialNaiveBayes:
    """
    Multinomial Naive Bayes classifier for text classification.
    """

    def __init__(self, alpha: float):
        """
        Initialize the Multinomial Naive Bayes classifier instance.

        Args:
            alpha (float): Smoothing parameter (Laplace smoothing)
        """
        self.alpha = alpha
        self.classes = None
        self.class_log_prior = None
        self.feature_log_prob = None

    def fit(self, X: np.ndarray, y: np.ndarray):
        """
        Fit the model according to the given training data.

        Args:
            X (ndarray): Training data of shape (n_samples, n_features)
            y (ndarray): Target labels of shape (n_samples,)
        """
        self.classes = np.unique(y)
        n_classes = len(self.classes)
        n_features = X.shape[1]

        feature_count = np.zeros((n_classes, n_features))
        class_count = np.zeros(n_classes)

        for idx, c in enumerate(self.classes):
            X_c = X[y == c]
            feature_count[idx, :] = X_c.sum(axis=0)
            class_count[idx] = X_c.shape[0]

        self.class_log_prior = np.log(class_count / class_count.sum())

        smoothed_fc = feature_count + self.alpha
        smoothed_cc = smoothed_fc.sum(axis=1, keepdims=True)

        self.feature_log_prob = np.log(smoothed_fc / smoothed_cc)

    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Predict the class labels for the input samples X.

        Args:
            X (ndarray): Input data of shape (n_samples, n_features)

        Returns:
            ndarray: Predicted class labels of shape (n_samples,)
        """
        log_probs = X @ self.feature_log_prob.T + self.class_log_prior

        return self.classes[np.argmax(log_probs, axis=1)]


def prepare_data(data: dict[str, list]) -> tuple[list[str], list[str]]:
    """
    Prepare the data for training the model.

    Args:
        data (dict[str, list]): A dictionary where keys are class labels and values are lists of text samples

    Returns:
        tuple[list[str], list[str]]: A tuple containing two lists: (texts, labels)
    """
    with open(data, "r") as f:
        data = json.load(f)

    texts = []
    labels = []

    for label, examples in data.items():
        for text in examples:
            texts.append(text)
            labels.append(label)

    return texts, labels


def train(data: str, model_path: str):
    """
    Train the Multinomial Naive Bayes model on the given data and save it to a file.

    Args:
        data (str): Path to the training data file (JSON format)
        model_path (str): Path to save the trained model
    """
    texts, labels = prepare_data(data)

    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(texts).toarray()

    y = np.array(labels)

    model = MultinomialNaiveBayes(alpha=1.0)
    model.fit(X, y)

    with open(model_path, "wb") as f:
        pickle.dump((vectorizer, model), f)


def predict(sentence: str, model: str) -> str:
    """
    Predict the intent of the given text using the trained model.

    Args:
        sentence (str): The input text to classify
        model (str): Path to the trained model file

    Returns:
        str: The predicted intent label
    """
    with open(model, "rb") as f:
        vectorizer, model = pickle.load(f)

    X = vectorizer.transform([sentence]).toarray()
    prediction = model.predict(X)

    return prediction[0]
