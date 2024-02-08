from mirmod.workflow_object import WOB
wob = WOB(name="the_lab2_histogram")
prefab_description = """
"""
prefab_labels=["The Lab"]
# ------------------- Code block -------------------
from mirmod import miranda
from mirmod.controls import Textbox, Plotly
import plotly.express as px
import pandas as pd
import json

@wob.init()
def init(self):
  self.df = None
  self.target = "target"

@wob.receiver("dataframe","Dataset")
def receive_value(self, value):
  self.df = value

@wob.receiver("string","Target Column",control=Textbox(placeholder="target"))
def receive_target(self, target):
  self.target = target

@wob.receiver("plotly","plotly",control=Plotly(),hidden=True)
def get_plotly(self,plotly_data):
  pass
 

@wob.execute()
def execute(self):
  ecx = miranda.get_execution_context()
  sc = ecx.get_security_context()
  wob = ecx.get_current_wob()

  fig = px.histogram(self.df,x=f"{self.target}", color=f"{self.target}", color_discrete_sequence=["grey", "cyan"])

  # magic to update UI
  miranda.update_api(sc, wob, "RECEIVER", "plotly", "plotly", value=fig.to_json(), control=Plotly().to_dict(), hidden=True, connectable=False)
  payload = json.dumps({ "action": "update[VIEW]", "data": { "id": wob.id, "metadata_id" : wob.metadata_id } })
  miranda.notify_gui(sc, payload)