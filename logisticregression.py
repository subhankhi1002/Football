# -*- coding: utf-8 -*-
"""LogisticRegression.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1FLXi3ua04lN65obejgoK3PYNmh49onfl
"""

import csv
def load_data(filename):
    dataset = []
    csvfile = open(filename, newline = '')
    reader = csv.reader(csvfile)
    for i in reader:
        dataset.append(i)
    return dataset

from google.colab import drive

drive.mount('/content/drive')

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sklearn

path_link = "/content/drive/MyDrive/ML Assignment/football.csv"
data = pd.read_csv(path_link)
dataframe=pd.DataFrame(data)
dataframe.head()

from sklearn.preprocessing import LabelEncoder

#perform label encoding on col1, col2 columns
dataframe[['league_name', 'preferred_foot','work_rate','body_type','player_traits','player_tags']] = dataframe[['league_name', 'preferred_foot','work_rate','body_type','player_traits','player_tags']].apply(LabelEncoder().fit_transform)

dataframe['value_eur'].fillna(dataframe['value_eur'].mean(), inplace=True)
dataframe['league_level'].fillna(dataframe['league_level'].mean(), inplace=True)
dataframe['release_clause_eur'].fillna(dataframe['release_clause_eur'].mean(), inplace=True)
dataframe['pace'].fillna(dataframe['pace'].mean(), inplace=True)
dataframe['shooting'].fillna(dataframe['shooting'].mean(), inplace=True)
dataframe['passing'].fillna(dataframe['passing'].mean(), inplace=True)
dataframe['dribbling'].fillna(dataframe['dribbling'].mean(), inplace=True)
dataframe['physic'].fillna(dataframe['physic'].mean(), inplace=True)
dataframe['defending'].fillna(dataframe['defending'].mean(), inplace=True)
dataframe=dataframe.drop(columns=['contribution_type'])
dataframe=dataframe.drop(columns=['goalkeeping_speed'])

dataframe.dropna(axis=1,how='any')

dataframe=dataframe.drop(columns=['short_name','club_name','club_team_id','wage_eur','preferred_foot'])

class Standardizer:
    def __init__(self, mean, stdev):
        self.mean = mean
        self.stdev = stdev
    def scale(self, x):
        return (x - self.mean)/self.stdev

for feature in dataframe.columns:
    if feature not in ('overall'):
        dataframe[feature] = dataframe[feature].apply(Standardizer(dataframe[feature].mean(), dataframe[feature].std()).scale)

dataframe.isna().sum()

dataframe=dataframe.drop(columns=['club_jersey_number','nation_jersey_number'])

dataframe.isna().sum()

def train_test(dataframe, split_value):
    n = int(split_value*len(dataframe))

    train_data = dataframe.iloc[:n, :]
    test_data =  dataframe.iloc[n:, :]

    return train_data,test_data

train_data, test_data = train_test(dataframe, 0.8)

X_train_multi_all = train_data.loc[:, train_data.columns != 'overall'].to_numpy()
X_test_multi_all = test_data.loc[:, test_data.columns != 'overall'].to_numpy()

Y_train = train_data.loc[:,train_data.columns == 'overall'].to_numpy()
Y_test = test_data['overall'].to_numpy()

import numpy as np

class MulticlassLogisticRegression:
    def __init__(self, learning_rate=0.01, num_iterations=1000):
        self.learning_rate = learning_rate
        self.num_iterations = num_iterations
        self.weights = None
        self.bias = None
        self.num_classes = None

    def softmax(self, z):
        exp_z = np.exp(z - np.max(z))  # Subtracting max(z) for numerical stability
        return exp_z / exp_z.sum(axis=0, keepdims=True)

    def one_hot_encoding(self, y):
        num_samples = len(y)
        num_classes = self.num_classes
        encoded = np.zeros((num_classes, num_samples))
        for i in range(num_samples):
            encoded[y[i], i] = 1
        return encoded

    def fit(self, X, y):
        num_samples, num_features = X.shape
        self.num_classes = len(np.unique(y))
        self.weights = np.zeros((self.num_classes, num_features))
        self.bias = np.zeros((self.num_classes, 1))
        y_encoded = self.one_hot_encoding(y)

        for _ in range(self.num_iterations):
            linear_model = np.dot(self.weights, X.T) + self.bias
            probabilities = self.softmax(linear_model)

            # Gradient descent
            dw = (1/num_samples) * np.dot((probabilities - y_encoded), X)
            db = (1/num_samples) * np.sum(probabilities - y_encoded, axis=1, keepdims=True)

            self.weights -= self.learning_rate * dw.T
            self.bias -= self.learning_rate * db

    def predict(self, X):
        linear_model = np.dot(self.weights, X.T) + self.bias
        probabilities = self.softmax(linear_model)
        predictions = np.argmax(probabilities, axis=0)
        return predictions
model = MulticlassLogisticRegression(learning_rate=0.1, num_iterations=1000)
model.fit(X_train_multi_all, Y_train)

Y_pred=model.predict(X_test_multi_all)

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.metrics import f1_score




print(mean_squared_error(Y_test,Y_pred))
print(mean_absolute_error(Y_test,Y_pred))



