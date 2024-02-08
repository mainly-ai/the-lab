from mirmod.workflow_object import WOB
wob = WOB(name="the_lab2.2_combine_dataset")
prefab_description = """
"""
prefab_labels=["The Lab"]
# ------------------- Code block -------------------
from mirmod import miranda
import pandas as pd

@wob.init()
def init(self):
  self.x1 = None
  self.x2 = None
  self.y1 = None
  self.y2 = None
  self.x = None
  self.y = None


@wob.receiver("dataframe","x1")
def receive_x1(self, x1):
  self.x1 = x1
@wob.receiver("dataframe","x2")
def receive_x2(self, x2):
  self.x2 = x2
@wob.receiver("dataframe","y1")
def receive_y1(self, y1):
  self.y1 = y1
@wob.receiver("dataframe","y2")
def receive_y2(self, y2):
  self.y2 = y2

@wob.transmitter("dataframe", "x")
def transmit_x(self):
  return self.x

@wob.transmitter("dataframe", "y")
def transmit_y(self):
  return self.y

@wob.execute()
def execute(self):
  def combine_train_val(x_train,x_val,y_train,y_val):
    x_full_train = pd.concat([x_train,x_val], axis=0)
    y_train_full = pd.concat([y_train,y_val], axis=0)
    return x_full_train, y_train_full
  
  self.x, self.y = combine_train_val(self.x1, self.x2, self.y1, self.y2)