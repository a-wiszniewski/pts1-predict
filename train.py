import pandas as pd
from sklearn.model_selection import train_test_split
from utils.encoder import SequenceSubsetter,SequenceEncoder
from utils.parser import read_fasta
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report
from sklearn.ensemble import RandomForestClassifier
import pickle

# parameters
test_size = 0.2
random_state = 101
start = -20
stop = None
encoding = 'blosum62'
n_estimators = 1000
class_weight = 'balanced'

# Read the fasta files
nonpts1 = read_fasta('data/train/nonpts1.fasta')
pts1 = read_fasta('data/train/pts1.fasta')

# Create a dataframe with the sequences and their labels
nonpts1['pts1'], pts1['pts1'] = 0, 1
df = pd.concat([pts1, nonpts1], axis=0)

# Split the data into train and test
X, y = df['sequence'], df['pts1']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)

# Create and fit the pipeline
pipe = Pipeline([('subset', SequenceSubsetter(start=start,stop=stop)),
                    ('encoder', SequenceEncoder(encoding=encoding)), 
                    ('clf', RandomForestClassifier(n_estimators=n_estimators,class_weight=class_weight))])
pipe.fit(X_train, y_train)

# Predict the test set and print the classification report
y_pred = pipe.predict(X_test)
print(classification_report(y_test, y_pred))

with open('model/log.txt', 'w') as f:
    f.write(f'test_size={test_size}\n')
    f.write(f'random_state={random_state}\n')
    f.write(f'start={start}\n')
    f.write(f'stop={stop}\n')
    f.write(f'encoding={encoding}\n')
    f.write(f'n_estimators={n_estimators}\n')
    f.write(f'class_weight={class_weight}\n')
    f.write(f'\n--------------- classification report ---------------\n')
    f.write(classification_report(y_test, y_pred))
    
# Fit the pipeline on the whole dataset and save the model
pipe.fit(X, y)
pickle.dump(pipe, open('model/model.pkl', 'wb'))