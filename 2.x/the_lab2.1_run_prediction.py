from mirmod.workflow_object import WOB
wob = WOB(name="the_lab2.1_run_prediction")
prefab_description = """
"""
prefab_labels=["The Lab"]
# ------------------- Code block -------------------
from mirmod import miranda

@wob.init()
def init(self):
  self.model = None
  self.x = None
  self.y_pred = None

@wob.receiver("dataframe","x")
def receive_x(self, x):
  self.x = x

@wob.receiver("modelcard","Trained Model")
def receive_model(self, model):
  self.model = model

@wob.transmitter("dataframe", "y_pred")
def transmit_y_pred(self):
  return self.y_pred

@wob.execute()
def execute(self):
  self.y_pred = self.model.predict(self.x)