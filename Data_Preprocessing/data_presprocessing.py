"""
Created on Thu Jul  9 12:24:05 2020
@author: Nur
"""
import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split


# Import the Dataset
dataset = pd.read_csv('Data.csv', sep=',')
_x = dataset.iloc[:, :-1].values
_y = dataset.iloc[:, -1].values


# Missing Data Manipulation
_imputer_class = SimpleImputer(
    strategy="mean"
)
_x[:, 1:3] = _imputer_class.fit_transform(_x[:, 1:3])


# Encode Categorical Data
# Independent Variable Encoding
_ct_class = ColumnTransformer(transformers=[('encoder', OneHotEncoder(), [0])], remainder='passthrough')
_x = np.array(_ct_class.fit_transform(_x))

# Dependent Variable Encoding
_label_encoder_y = LabelEncoder()
_y = _label_encoder_y.fit_transform(_y)


# Dataset Splitting into the Training set and Test set
x_train, x_test, y_train, y_test = train_test_split(_x, _y, test_size=0.2, random_state=42)


# Feature Scaling
_scalar_class = StandardScaler()
x_train[:, 3:] = _scalar_class.fit_transform(x_train[:, 3:])
x_test[:, 3:] = _scalar_class.transform(x_test[:, 3:])
