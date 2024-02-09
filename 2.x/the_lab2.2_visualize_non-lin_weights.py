from mirmod.workflow_object import WOB
wob = WOB(name="the_lab2.2_visualize_non-lin_weights")
prefab_description = """
"""
prefab_labels=["The Lab"]
# ------------------- Code block -------------------
from mirmod import miranda
from mirmod.controls import Plotly
import plotly.graph_objects as go
import plotly.figure_factory as ff
import plotly.express as px
import json
import pandas as pd
import numpy as np

from sklearn.svm import SVR
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.inspection import permutation_importance

def generate_non_linear_reg_model_weights(model,x_val, y_val):
    if type(model) == RandomForestRegressor:
        sorted_idx = model.feature_importances_.argsort()
        df_coef = pd.DataFrame({"Feature Weight": model.feature_importances_[sorted_idx], "Classes": model.feature_names_in_[sorted_idx]})
        model_name = "Random Forest"
    elif type(model) == GradientBoostingRegressor:
        sorted_idx = model.feature_importances_.argsort()
        df_coef = pd.DataFrame({"Feature Weight": model.feature_importances_[sorted_idx], "Classes": model.feature_names_in_[sorted_idx]})
        model_name = "Gradient Boosting"
    elif type(model) == SVR:
        perm_imp = permutation_importance(model, x_val, y_val, n_repeats=100)
        feature_names = x_val.columns
        feature_names = np.array(feature_names)
        sorted_idx = perm_imp.importances_mean.argsort()
        df_coef = pd.DataFrame({"Feature Weight": perm_imp.importances_mean[sorted_idx], "Classes": feature_names[sorted_idx]})
        model_name = "SVM (Sigmoid)"

    fig = px.bar(df_coef, x="Classes", y=df_coef["Feature Weight"], title="Wide-Form Input", height=1000)
    fig.update_layout(
        title=None,
        font=dict(
            family="Courier New, monospace",
            size=20,
            color="RebeccaPurple"
        ))
    return fig

@wob.init()
def init(self):
  self.model = None
  self.x_val = None
  self.y_val = None

@wob.receiver("modelcard","Trained Non-Linear Model")
def receive_model(self, model):
  self.model = model

@wob.receiver("dataframe","x_val")
def receive_x_val(self, x_val):
  self.x_val = x_val

@wob.receiver("dataframe","y_val")
def receive_y_val(self, y_val):
  self.y_val = y_val


@wob.receiver("plotly","plotly",control=Plotly(),hidden=True)
def get_plotly(self,plotly_data):
  pass

@wob.execute()
def execute(self):
  ecx = miranda.get_execution_context()
  sc = ecx.get_security_context()
  wob = ecx.get_current_wob()

  fig = generate_non_linear_reg_model_weights(self.model, self.x_val, self.y_val)

  # magic to update UI
  miranda.update_api(sc, wob, "RECEIVER", "plotly", "plotly", value=fig.to_json(), control=Plotly().to_dict(), hidden=True, connectable=False)
  payload = json.dumps({ "action": "update[VIEW]", "data": { "id": wob.id, "metadata_id" : wob.metadata_id } })
  miranda.notify_gui(sc, payload)