from mirmod.workflow_object import WOB
wob = WOB(name="the_lab2.1_logistic_regression")
prefab_description = """
"""
prefab_labels=["The Lab"]
# ------------------- Code block -------------------
from mirmod import miranda
from mirmod.controls import Select
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
import pandas as pd
import numpy as np

@wob.init()
def init(self):
  self.x = None
  self.y = None
  self.model = None
  self.std = "No"

@wob.receiver("dataframe","x_train")
def receive_x(self, x):
  self.x = x

@wob.receiver("dataframe","y_train")
def receive_y(self, y):
  self.y = y

@wob.receiver("string","Standardized", connectable=False, control=Select(choices=['Yes', 'No'], placeholder="No"))
def receive_std(self, std):
  self.std = std

@wob.transmitter("modelcard", "Trained Model")
def transmit_model(self):
  return self.model

@wob.execute()
def execute(self):
  DATA_RS, MODEL_RS = 100,100

  lr = LogisticRegression(penalty="none", random_state=MODEL_RS, max_iter=1000)
  if self.std == "Yes":
    lr_std= LogisticRegression(penalty="none", random_state=MODEL_RS, max_iter=1000)
    std_steps = [("Scaling", StandardScaler()), ("Modeling", lr_std)]
    self.model = Pipeline(steps=std_steps)
  else:
    self.model = lr
  
  self.model.fit(self.x, np.ravel(self.y))