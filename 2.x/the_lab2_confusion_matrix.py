from mirmod.workflow_object import WOB
wob = WOB(name="the_lab2_confusion_matrix")
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
import json

def generate_confusion_matrix(y_true,y_pred, labels, title=None):
    z = confusion_matrix(y_true, y_pred)

    z = z[::-1]
    x = labels
    y = labels[::-1].copy()

    # change each element of z to type string for annotations
    z_text = [[str(y) for y in x] for x in z]

    # set up figure 
    fig = ff.create_annotated_heatmap(z, 
                                    x=x, 
                                    y=y, 
                                    annotation_text=z_text, 
                                    colorscale="tempo",
                                    reversescale=False)
    
    # add custom xaxis title
    fig.add_annotation(dict(font=dict(color="black",size=25),
                            x=0.5,
                            y=-0.15,
                            showarrow=False,
                            text="Predicted value",
                            xref="paper",
                            yref="paper"))
    
    # add custom yaxis title
    fig.add_annotation(dict(font=dict(color="black",size=25),
                            x=-0.25,
                            y=0.5,
                            showarrow=False,
                            text="Real value",
                            textangle=-90,
                            xref="paper",
                            yref="paper"))
    
    # adjust margins to make room for yaxis title
    fig.update_layout(
            title_font = dict(color="grey"),
            title_yanchor="auto",
            font=dict(
            family="Times New Roman",
            size=15,
            color="black"
        ), margin=dict(b=100))
    # add colorbar
    fig['data'][0]['showscale'] = True
    
    return fig


@wob.init()
def init(self):
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

@wob.transmitter("modelcard", "output")
def transmit_value(self):
  return self.value

@wob.receiver("plotly","plotly",control=Plotly(),hidden=True)
def get_plotly(self,plotly_data):
  pass

@wob.execute()
def execute(self):
  ecx = miranda.get_execution_context()
  sc = ecx.get_security_context()
  wob = ecx.get_current_wob()

  fig = generate_confusion_matrix(y_true=self.y_true, y_pred=self.y_pred, labels=self.model.classes_.tolist(), title="")

  # magic to update UI
  miranda.update_api(sc, wob, "RECEIVER", "plotly", "plotly", value=fig.to_json(), control=Plotly().to_dict(), hidden=True, connectable=False)
  payload = json.dumps({ "action": "update[VIEW]", "data": { "id": wob.id, "metadata_id" : wob.metadata_id } })
  miranda.notify_gui(sc, payload)