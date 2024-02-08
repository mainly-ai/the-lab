from mirmod.workflow_object import WOB
wob = WOB(name="the_lab2.1_dataset")
prefab_description = """
"""
prefab_labels=["The Lab"]
# ------------------- Code block -------------------
from mirmod import miranda
from ucimlrepo import fetch_ucirepo
from sklearn.model_selection import train_test_split
import pandas as pd

@wob.init()
def init(self):
  self.data = None
  self.df = None
  self.x_train = None
  self.x_val = None
  self.x_test = None
  self.y_train = None
  self.y_val = None
  self.y_test = None

@wob.transmitter("dataframe", "Dataset")
def transmit_value(self):
  return self.df

@wob.transmitter("dataframe", "x_train")
def transmit_x_train(self):
  return self.x_train
@wob.transmitter("dataframe", "x_val")
def transmit_x_val(self):
  return self.x_val
@wob.transmitter("dataframe", "x_test")
def transmit_x_test(self):
  return self.x_test
@wob.transmitter("dataframe", "y_train")
def transmit_y_train(self):
  return self.y_train
@wob.transmitter("dataframe", "y_val")
def transmit_y_val(self):
  return self.y_val
@wob.transmitter("dataframe", "y_test")
def transmit_y_test(self):
  return self.y_test

@wob.execute()
def execute(self):
  self.data = fetch_ucirepo(id=544)
  X = self.data.data.features 
  y = self.data.data.targets

  self.df = pd.concat([X,y], axis=1, join="inner")

  def binarize_y(target:str):
    """"""
    if target in ["Insufficient_Weight", "Normal_Weight"]:
        return "Not Obese"
    else:
        return "Obese"
    
  self.df["target"] = self.df.NObeyesdad.apply(binarize_y)

  features = ['Gender', 'Age', 'Height', 'Weight', 'family_history_with_overweight',
       'FAVC', 'FCVC', 'NCP', 'CAEC', 'SMOKE', 'CH2O', 'SCC', 'FAF', 'TUE',
       'CALC', 'MTRANS']
  target = ["target"]

  DATA_RS, MODEL_RS = 100,100

  def deobjectify_df(X:pd.DataFrame):
    """"""

    # List to store Categorical Columns
    cat_cols = list(X.columns[X.dtypes == 'object'])
    print("Categorical Columns: ",cat_cols)

    # List to store Numerical Columns
    num_cols = list(X.columns[X.dtypes != 'object'])
    print("\nNumerical Columns:" ,num_cols)

    ## One-Hot Encoding Categorical Columns
    x_dummy =  pd.get_dummies(X[cat_cols], drop_first=True)

    ## Joining New dummified and Numerical columns
    x_new = pd.concat([x_dummy, X[num_cols]], axis=1, join='inner')
    return x_new

  x_new = deobjectify_df(X=self.df[features])

  def get_train_val_test(X,y):
    x_train, x_int, y_train, y_int = train_test_split(X,y, random_state=DATA_RS,test_size=0.5, stratify=y)
    x_val, x_test, y_val, y_test = train_test_split(x_int,y_int, random_state=DATA_RS,test_size=0.5, stratify=y_int)
    return x_train,x_val,x_test, y_train,y_val,y_test

  self.x_train,self.x_val,self.x_test, self.y_train,self.y_val,self.y_test = get_train_val_test(X=x_new,y=self.df[target])
