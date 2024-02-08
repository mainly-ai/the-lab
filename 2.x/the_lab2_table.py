from mirmod.workflow_object import WOB
wob = WOB(name="the_lab2_table")
prefab_description = """
"""
prefab_labels=["The Lab"]
# ------------------- Code block -------------------
from mirmod import miranda
from mirmod.controls import Plotly
from sklearn.metrics import confusion_matrix
import plotly.graph_objects as go
import plotly.figure_factory as ff
import plotly.express as px
import pandas as pd
import json

def generate_statistical_summary(input_df:pd.DataFrame):
    """Generates statistical summary of a Pandas dataframe as a Plotly Figure object"""
    df = input_df.describe().T
    cols = ["Variables", 'Count', 'Mean',"ST-Dev","Min","Median",'Max']
    fig = go.Figure(data=[go.Table(
    header=dict(values=list(f"<b>{item}</b>" for item in cols),
                fill_color='paleturquoise',
                font=dict(color='black', size=15),
                align='center'),
    cells=dict(values=[df.index,
                       df["count"],
                       df["mean"].round(3),
                       df["std"].round(3),
                       df["min"].round(3),
                       df["50%"].round(3),
                       df["max"]],
               fill=dict(color=['grey', 'cyan']),
               font=dict(color='black',
                         family = ["Times New Roman","helvetica"],
                        size=15),
               height=25,
               align='center'))
])

    fig.update_layout(
        font=dict(
        family="Times New Roman",
        size=20,
        color="RebeccaPurple"
    ))

    return fig


@wob.init()
def init(self):
  self.df = None

@wob.receiver("dataframe","Dataset")
def receive_df(self, df):
  self.df = df

@wob.receiver("plotly","plotly",control=Plotly(),hidden=True)
def get_plotly(self,plotly_data):
  pass

@wob.execute()
def execute(self):
  ecx = miranda.get_execution_context()
  sc = ecx.get_security_context()
  wob = ecx.get_current_wob()

  fig = generate_statistical_summary(self.df)

  # magic to update UI
  miranda.update_api(sc, wob, "RECEIVER", "plotly", "plotly", value=fig.to_json(), control=Plotly().to_dict(), hidden=True, connectable=False)
  payload = json.dumps({ "action": "update[VIEW]", "data": { "id": wob.id, "metadata_id" : wob.metadata_id } })
  miranda.notify_gui(sc, payload)