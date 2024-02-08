from mirmod.workflow_object import WOB
wob = WOB(name="the_lab2.2_non-linear_model")
prefab_description = """
"""
prefab_labels=["The Lab"]
# ------------------- Code block -------------------
from mirmod import miranda
from mirmod.controls import Plotly
from sklearn.metrics import mean_squared_error
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import json

def get_mse_rmse(model, x_true, y_true):
  """"""
  y_pred = model.predict(x_true)
  mse =mean_squared_error(y_true=y_true, y_pred=y_pred, squared=True)
  rmse =mean_squared_error(y_true=y_true, y_pred=y_pred, squared=False)
  return mse, rmse

def generate_report(models, x_true, y_true):
  """"""
  report_dict = dict()
  for model_name, model in models:
    mse, rmse = get_mse_rmse(model, x_true, y_true)
    report_dict[f"{model_name}"] = {"Mean-Squared Error":mse.round(4), "RMSE":rmse.round(4)}
  return pd.DataFrame(report_dict).T

def generate_regression_model_results(report_df):
    columns = ["Models"] + report_df.columns.to_list()
    # import plotly.graph_objects as go
    fig = go.Figure(data=[go.Table(
      header=dict(values=list(f"<b>{item}</b>" for item in columns),
                  fill_color='paleturquoise',
                  font=dict(color='black', size=15),
                  align='center'),
      cells=dict(values=[report_df.index,
                        report_df["Mean-Squared Error"].round(3), 
                        report_df["RMSE"].round(3)],
                fill=dict(color=['lightgrey', 'white']),
                font=dict(color='black', size=15),
                height=25,
                align='center'))
    ])

    fig.update_layout(
        font=dict(
        family="Courier New, monospace",
        size=20,
        color="RebeccaPurple"
    ))

    return fig

@wob.init()
def init(self):
  self.x = None
  self.y = None

  self.models = []

@wob.receiver('dataframe', 'x')
def receive_x(self, x):
  self.x = x

@wob.receiver('dataframe', 'y')
def receive_x(self, y):
  self.y = y

@wob.receiver("modelcard","Linear Regression")
def receive_model(self, model):
  self.models.append(('Linear Regression', model))
@wob.receiver("modelcard","Lasso Regression")
def receive_model(self, model):
  self.models.append(('Lasso Regression', model))
@wob.receiver("modelcard","Elastic Net")
def receive_model(self, model):
  self.models.append(('Elastic Net', model))
@wob.receiver("modelcard","SVM-Sigmoid")
def receive_model(self, model):
  self.models.append(('SVM-Sigmoid', model))
@wob.receiver("modelcard","Random Forest")
def receive_model(self, model):
  self.models.append(('Random Forest', model))
@wob.receiver("modelcard","Gradient Boosting")
def receive_model(self, model):
  self.models.append(('Gradient Boosting', model))

@wob.receiver('plotly', 'plotly', hidden=True, control=Plotly())
def get_plotly(self):
  pass

@wob.execute()
def execute(self):
  ecx = miranda.get_execution_context()
  sc = ecx.get_security_context()
  wob = ecx.get_current_wob()

  report = generate_report(self.models, self.x, self.y)

  fig = generate_regression_model_results(report)

  # magic to update UI
  miranda.update_api(sc, wob, "RECEIVER", "plotly", "plotly", value=fig.to_json(), control=Plotly().to_dict(), hidden=True, connectable=False)
  payload = json.dumps({ "action": "update[VIEW]", "data": { "id": wob.id, "metadata_id" : wob.metadata_id } })
  miranda.notify_gui(sc, payload)