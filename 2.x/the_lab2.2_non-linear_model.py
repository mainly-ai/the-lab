from mirmod.workflow_object import WOB
wob = WOB(name="the_lab2.2_non-linear_model")
prefab_description = """
"""
prefab_labels=["The Lab"]
# ------------------- Code block -------------------
from mirmod import miranda
from mirmod.controls import Select

from sklearn.svm import SVR
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor

import numpy as np

@wob.init()
def init(self):
  self.x = None
  self.y = None
  self.selected_model_str = "SVM-Sigmoid"
  self.model = None

@wob.receiver("string", "model", control=Select(placeholder="SVM-Sigmoid", choices=["SVM-Sigmoid", "RandomForest", "GradientBoosting"]))
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
  if self.selected_model_str == "SVM-Sigmoid":
    self.model = SVR(kernel="sigmoid")
  elif self.selected_model_str == "RandomForest":
    self.model = RandomForestRegressor(n_estimators=100, n_jobs=-1)
  elif self.selected_model_str == "GradientBoosting":
    self.model = GradientBoostingRegressor(n_estimators=100)
  else:
    raise Exception("No model selected")

  self.model.fit(self.x, np.ravel(self.y))