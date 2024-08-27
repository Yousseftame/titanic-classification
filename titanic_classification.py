# -*- coding: utf-8 -*-
"""titanic classification.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1ZRbu_NLecWwgHZJi1N_C-7SFCCt291AN
"""

# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# You can write up to 20GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All"
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session

"""# Import Important Libraries"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split ,GridSearchCV
from sklearn.metrics import accuracy_score ,confusion_matrix,ConfusionMatrixDisplay,classification_report
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier

"""# Load data"""

df = pd.read_csv('/kaggle/input/titanic-dataset/Titanic-Dataset.csv')

"""# Explore data
    
"""

df.head(20)

df.shape

df.info()

df.describe()

df.duplicated().sum()

null_d=df.isnull().sum()
null_d[null_d>0]

sns.heatmap(df.isnull())

null_d[null_d>0].plot(kind='bar')

"""# Data Cleaning

"""

df.drop(['PassengerId','Name','Ticket','Cabin','Embarked','Fare'],axis =1 , inplace=True )

df.Age=df.Age.fillna(df.Age.mean())

df.isna().sum()

sns.heatmap(df.isnull())

"""# Data Aanlysis"""

num_cols = df.select_dtypes(include='number').columns

corr_matrix = df[num_cols].corr()
corr_matrix

sns.heatmap(corr_matrix,annot=True,fmt='.1f',linewidths=4)

df.Survived.value_counts()

df.Sex.value_counts()

sns.countplot(x='Survived',data=df,hue='Sex')

df.Survived.groupby(df.Pclass).value_counts()

sns.countplot(x='Pclass',data=df,hue='Survived')

age=df.Age.groupby(df.Survived).value_counts()
age

age=df.Age.groupby(df.Survived).value_counts()
age

df[df['Survived']==1 ] ['Age'].max()

df[df['Survived']==0 ] ['Age'].max()

df[df['Survived']==0 ] ['Age'].mode()

df[df['Survived']==1 ] ['Age'].mode()

sns.histplot(x='Age',data=df)

df.Sex.value_counts().plot.pie(autopct='%.2f%%')

gpsex=df.Survived.groupby(df.Sex).value_counts()
gpsex.plot.pie(autopct='%.2f%%')

"""# Data Transformation

"""

data=pd.get_dummies(df['Sex'],drop_first=True)
data=data.astype('int64')
data

df=pd.concat([df,data],axis=1)
df

df.drop('Sex',axis=1,inplace = True )

df.rename(columns={'male':'gender'})

"""# Split features & target

"""

x=df.drop('Survived',axis=1)
y=df.Survived

x.shape,y.shape

"""# Split train & test data

"""

x_train,x_test,y_train,y_test=train_test_split(x,y,train_size=0.8,random_state=42,shuffle=True)

"""# Bulid model

"""

log_reg=LogisticRegression()
rf_clf=RandomForestClassifier()
svc=SVC()
gbc= GradientBoostingClassifier()

def all(model):
    model.fit(x_train,y_train)
    y_pred=model.predict(x_test)
    accuracy_test=accuracy_score(y_pred,y_test)*100
    accuracy_train=model.score(x_train,y_train)*100
    print('accuracy after train model :',accuracy_train)
    print('accuracy after test  model :',accuracy_test)

all(gbc)

all(log_reg)

all(svc)

all(rf_clf)

"""# Evaluate model

"""

def cm(model):
    y_pred=model.predict(x_test)

    cm = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(8, 6))

    disp = ConfusionMatrixDisplay(confusion_matrix=cm,display_labels=model.classes_)
    disp.plot(cmap='Blues')
    plt.title('Confusion Matrix')
    plt.show()

cm(log_reg)

def class_report(model):
    y_pred=model.predict(x_test)
    report = classification_report(y_test, y_pred, target_names=['Benign', 'Malignant'])
    print("Classification Report:\n", report)

class_report(log_reg)
