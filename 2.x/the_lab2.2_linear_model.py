from mirmod.workflow_object import WOB
wob = WOB(name="the_lab2.2_linear_model")
prefab_description = """
"""
prefab_labels=["The Lab"]
# ------------------- Code block -------------------
from mirmod import miranda
from mirmod.controls import Select

from sklearn.linear_model import LinearRegression, ElasticNet
import numpy as np

DATA_RS, MODEL_RS = 100,100

@wob.init()
def init(self):
  self.x = None
  self.y = None
  self.selected_model_str = "LinearRegression"
  self.model = None

@wob.receiver("string", "model", control=Select(placeholder="LinearRegression", choices=["LinearRegression", "LASSO", "ElasticNet"]))
def receive_selected_model_str(self, selected_model_str):
  self.selected_model_str = selected_model_str

@wob.receiver("dataframe","x")
def receive_x(self, x):
  self.x = x

@wob.receiver("dataframe","y")
def receive_y(self, y):
  self.y = y

@wob.transmitter("modelcard", "Trained Model")
def transmit_model(self):
  return self.model

@wob.execute()
def execute(self):
  if self.selected_model_str == "LinearRegression":
    self.model = LinearRegression(n_jobs=-1)
  elif self.selected_model_str == "LASSO":
    self.model = ElasticNet(l1_ratio=1, random_state=MODEL_RS)
  elif self.selected_model_str == "ElasticNet":
    self.model = ElasticNet(l1_ratio=0.5, random_state=MODEL_RS)
  else:
    raise Exception("No model selected")

  self.model.fit(self.x, np.ravel(self.y))