import pandas as pd
import numpy as np
import pickle
from sklearn.base import BaseEstimator, TransformerMixin

class SequenceSubsetter(BaseEstimator, TransformerMixin):

    def __init__(self, start=0, stop=100):
        self.start = start
        self.stop = stop
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X, y=None):

        X_ = X.copy()
        X_transformed = pd.DataFrame()

        if isinstance(X_, pd.DataFrame):
            for column in X_.columns:
                if (X_[column].apply(isinstance, args=[str])).all():
                    X_column = X_[column].apply(lambda x: x[self.start:self.stop])
                    X_transformed = pd.concat([X_transformed, X_column], axis=1)

        elif isinstance(X_, pd.Series):
            if (X_.apply(isinstance, args=[str])).all():
                X_transformed = X_.apply(lambda x: x[self.start:self.stop])
        
        else:
            raise TypeError('X must be a pd.DataFrame or pd.Series')

        return X_transformed

class SequenceEncoder(BaseEstimator, TransformerMixin):

    def __init__(self, encoding='blosum62'):
        self.encoding = encoding

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):

        file = open('utils/encodings.pkl','rb')
        encoding = pickle.load(file).get(self.encoding)
        file.close()

        X_ = X.copy()

        X_transformed = pd.DataFrame()

        def seq_vectorizer(sequence,encoding):
            vectors = []
            for aminoacid in sequence:
                vector = encoding.get(aminoacid, [np.nan] * len(list(encoding.values())[0]))
                vectors.extend(vector)
            return pd.Series(vectors,dtype=np.float64)

        if isinstance(X_, pd.DataFrame):
            for column in X_.columns:
                if (X_[column].apply(isinstance, args=[str])).all():
                    X_column = X_[column].apply(seq_vectorizer,encoding=encoding)
                    X_transformed = pd.concat([X_transformed, X_column], axis=1)

        elif isinstance(X_, pd.Series):
            if (X_.apply(isinstance, args=[str])).all():
                X_transformed = X_.apply(seq_vectorizer,encoding=encoding)

        else:
            raise TypeError('X must be a pd.DataFrame or pd.Series')

        min_value = (X_transformed.min(numeric_only=True).min())

        X_transformed = X_transformed.fillna(value=min_value)

        return X_transformed
