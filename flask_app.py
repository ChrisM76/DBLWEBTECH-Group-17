
# A very simple Flask Hello World app for you to get started with...

from flask import Flask

server = Flask(__name__)

@server.route('/')
def hello_world():
    return 'Hello from Flask!'

####
# Dash app 'filterednetwork.py'
####
import pandas as pd
import numpy as np
import dash
import dash_cytoscape as cyto
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
from random import random
import json


app = dash.Dash(__name__, server = server, routes_pathname_prefix = '/dash/')


file_enron = '/home/thebenjameister/mysite/enron-v1.csv'
enron_data = pd.read_csv(file_enron)
enron_data


enron_string = enron_data[(enron_data['fromJobtitle'] == 'CEO' )& (enron_data['toJobtitle']=='Employee')].astype(str)


emailfromName = enron_string['fromEmail']
emailtoName = enron_string['toEmail']
emailName = np.concatenate((emailfromName,emailtoName))
fromId = enron_string['fromId']
toId = enron_string['toId']
emailId = np.concatenate((fromId, toId))

IdList = []
for i in emailId:
    if i not in IdList:
        IdList.append(i)
NameList = []
for i in emailName:
    if i not in NameList:
        NameList.append(i)

node_data = zip(IdList,NameList)
target_data = zip(fromId,toId)

def removeDuplicates(target_data):
    return list(set([i for i in target_data]))
clean_target_data = removeDuplicates(target_data)

nodes = [{'data':{'id':item[0], 'label':item[1]}, 'position': {'x': (random()*1000), 'y':(random()*1000)}} for item in node_data]
edges = [{'data':{'source':item[0], 'target':item[1]}} for item in clean_target_data]

cyto_data = nodes + edges


graph_roots = ["#" + Id for Id in fromId]
clean_graph_roots = []
for i in graph_roots:
    if i not in clean_graph_roots:
        clean_graph_roots.append(i)
comma_separated_roots = ", ".join(clean_graph_roots)

default_stylesheet = [
    {
        "selector": 'node',
        'style': {
            "opacity": 0.65,'shape': 'rectangle'
        }
    },
    {
        "selector": 'edge',
        'style': {
            "curve-style": "bezier",
            "opacity": 0.65
        }
    },
]

styles = {
    'json-output': {
        'overflow-y': 'scroll',
        'height': 'calc(50% - 25px)',
        'border': 'thin lightgrey solid'
    },
    'tab': {
        'height': 'calc(98vh - 105px)'
    }
}

app.layout = html.Div([
    html.Div(className='eight columns', children=[
        cyto.Cytoscape(
            id='cytoscape',
            layout={'name': 'breadthfirst','roots':comma_separated_roots},
            elements=cyto_data,
            style={
                'height': '95vh',
                'width': '100%'
            }
        ),
                html.P(id='cytoscape-mouseoverNodeData-output'),
    ])
])


@app.callback(Output('tap-node-json-output', 'children'),
              [Input('cytoscape', 'tapNode')])
def display_tap_node(data):
    return json.dumps(data, indent=2)


@app.callback(Output('tap-edge-json-output', 'children'),
              [Input('cytoscape', 'tapEdge')])
def display_tap_edge(data):
    return json.dumps(data, indent=2)


@app.callback(Output('cytoscape', 'stylesheet'),
              [Input('cytoscape', 'tapNode')])
def generate_stylesheet(node):
    follower_color = '#0074D9'
    following_color = '#FF4136'
    node_shape = 'rectangle'
    if not node:
        return default_stylesheet

    stylesheet = [{
        "selector": 'node',
        'style': {
            'opacity': 0.3,
            'shape': node_shape
        }
    }, {
        'selector': 'edge',
        'style': {
            'opacity': 0.2,
            "curve-style": "bezier",
        }
    }, {
        "selector": 'node[id = "{}"]'.format(node['data']['id']),
        "style": {
            'background-color': '#B10DC9',
            "border-color": "purple",
            "border-width": 2,
            "border-opacity": 1,
            "opacity": 1,

            "label": "data(label)",
            "color": "#B10DC9",
            "text-opacity": 1,
            "font-size": 12,
            'z-index': 9999
        }
    }]

    for edge in node['edgesData']:
        if edge['source'] == node['data']['id']:
            stylesheet.append({
                "selector": 'node[id = "{}"]'.format(edge['target']),
                "style": {
                    'background-color': following_color,
                    'opacity': 0.9
                }
            })
            stylesheet.append({
                "selector": 'edge[id= "{}"]'.format(edge['id']),
                "style": {
                    "mid-target-arrow-color": following_color,
                    "mid-target-arrow-shape": "vee",
                    "line-color": following_color,
                    'opacity': 0.9,
                    'z-index': 5000
                }
            })

        if edge['target'] == node['data']['id']:
            stylesheet.append({
                "selector": 'node[id = "{}"]'.format(edge['source']),
                "style": {
                    'background-color': follower_color,
                    'opacity': 0.9,
                    'z-index': 9999
                }
            })

            stylesheet.append({
                "selector": 'edge[id= "{}"]'.format(edge['id']),
                "style": {
                    "mid-target-arrow-color": follower_color,
                    "mid-target-arrow-shape": "vee",
                    "line-color": follower_color,
                    'opacity': 1,
                    'z-index': 5000
                }
            })

    return stylesheet


if __name__ == '__main__':
    app.run_server(debug=False)





