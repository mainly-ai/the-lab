from mirmod.workflow_object import WOB
wob = WOB(name="the_lab2.2_visualize_lin_weights")
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

def generate_lin_reg_model_weights(model, model_name="Logistic Model"):
    df_coef = pd.DataFrame({"Feature Weight": model.coef_, "Classes": model.feature_names_in_})
    fig = px.bar(df_coef, x="Classes", y=df_coef["Feature Weight"], title="Wide-Form Input", height=1000)
    fig.update_layout(
            font=dict(
            family="Courier New, monospace",
            size=20,
            color="RebeccaPurple"
        ))
    return fig

@wob.init()
def init(self):
  self.model = None

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

  fig = generate_lin_reg_model_weights(self.model,model_name="")

  # magic to update UI
  miranda.update_api(sc, wob, "RECEIVER", "plotly", "plotly", value=fig.to_json(), control=Plotly().to_dict(), hidden=True, connectable=False)
  payload = json.dumps({ "action": "update[VIEW]", "data": { "id": wob.id, "metadata_id" : wob.metadata_id } })
  miranda.notify_gui(sc, payload)