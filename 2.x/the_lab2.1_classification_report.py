from mirmod.workflow_object import WOB
wob = WOB(name="the_lab2.1_classification_report")
prefab_description = """
"""
prefab_labels=["The Lab"]
# ------------------- Code block -------------------
from mirmod import miranda
from mirmod.controls import Plotly
import pandas as pd
from sklearn.metrics import classification_report
import plotly.graph_objects as go
import plotly.figure_factory as ff
import plotly.express as px
import json

def generate_classification_report(y_true,y_pred, target_names, split):

  # target_names = model.classes_.tolist()
  
  df_results= pd.DataFrame(classification_report(y_true, y_pred, target_names=target_names, output_dict=True)).T
  df_results = df_results[:-3]

  # import plotly.graph_objects as go
  fig = go.Figure(data=[go.Table(
    header=dict(values=list(f"<b>{item}</b>" for item in ["Features","Precision","Recall","F1-score", "Support"]),
                fill_color='paleturquoise',
                font=dict(color='black', size=15),
                align='center'),
    cells=dict(values=[[f"<b>{str(val)}</b>" for val in df_results.index],df_results.precision.round(2), 
                        df_results.recall.round(2), 
                        df_results["f1-score"].round(2), 
                        df_results.support.round(2)],
                fill=dict(color=['grey', 'white']),
                font=dict(color='black', size=20),
                height=30,
                align='left'),
                columnwidth=[1.2,0.5]
                )
  ])

  fig.update_layout(
      font=dict(
      family="Courier New, monospace",
      size=25,
      color="RebeccaPurple"
  ))
  
  return fig


@wob.init()
def init(self):
  self.value = None
  self.y_true = None
  self.y_pred = None
  self.model = None

@wob.receiver("dataframe","y_true")
def receive_y_true(self, y_true):
  self.y_true = y_true

@wob.receiver("dataframe","y_pred")
def receive_y_pred(self, y_pred):
  self.y_pred = y_pred

@wob.receiver("modelcard","Trained Model")
def receive_model(self, model):
  self.model = model

@wob.receiver("plotly","plotly",control=Plotly(),hidden=True)
def get_plotly(self,plotly_data):
  pass

@wob.execute()
def execute(self):
  ecx = miranda.get_execution_context()
  sc = ecx.get_security_context()
  wob = ecx.get_current_wob()

  fig = generate_classification_report(y_true=self.y_true, y_pred=self.y_pred, target_names=self.model.classes_.tolist(), split="")

  # magic to update UI
  miranda.update_api(sc, wob, "RECEIVER", "plotly", "plotly", value=fig.to_json(), control=Plotly().to_dict(), hidden=True, connectable=False)
  payload = json.dumps({ "action": "update[VIEW]", "data": { "id": wob.id, "metadata_id" : wob.metadata_id } })
  miranda.notify_gui(sc, payload)