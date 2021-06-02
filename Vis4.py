import plotly.graph_objects as go  # or plotly.express as px

fig = go.Figure()  # or any Plotly Express function e.g. px.bar(...)
# fig.add_trace( ... )
# fig.update_layout( ... )
import json
import pandas as pd

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px

NUMBER_EMAILS_BY_DATE = dict()


def preparedata():
    file_enron = 'enron-v1.csv'
    enron_data = pd.read_csv(file_enron)
    enron_data = enron_data.sort_values(by="date", key=pd.to_datetime)
    dates = [x for x in enron_data['date']]
    number_of_emails_per_date = dict()
    count = 0
    while len(dates) > 0:
        current_date = dates[0]
        # exclude outside the date range
        # if pd.to_datetime(current_date) < pd.to_datetime(start_date) or pd.to_datetime(current_date) > pd.to_datetime(end_date):
        #     dates.pop(0)
        #     continue
        index = 0
        number_of_emails = 0
        while index < len(dates):
            if current_date == dates[index]:
                number_of_emails += 1
                dates.pop(index)
            else:
                index += 1
        number_of_emails_per_date.update({current_date: number_of_emails})
        count += 1
    global NUMBER_EMAILS_BY_DATE
    NUMBER_EMAILS_BY_DATE = number_of_emails_per_date


def generateGraph(start_date, end_date):
    data = dict()

    if len(str(start_date)) + len(str(end_date)) == len(str('1999-01-04')) * 2:
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)
        for date in NUMBER_EMAILS_BY_DATE:
            if pd.to_datetime(date) >= start_date and pd.to_datetime(date) <= end_date:
                data.update({date: NUMBER_EMAILS_BY_DATE[date]})
    else:
        data = NUMBER_EMAILS_BY_DATE

    if len(data) == 0:
        data = NUMBER_EMAILS_BY_DATE
        
    fig = px.line(x=[key for key in data], y=[data[key] for key in data])
    fig.update_layout(
        title="Plot Title",
        xaxis_title="X Axis Title",
        yaxis_title="Y Axis Title",
        legend_title="Legend Title",
        font=dict(
            family="Courier New, monospace",
            size=18,
            color="RebeccaPurple"
        )
    )
    return fig


app = dash.Dash()

app.layout = html.Div([
    dcc.DatePickerRange(
        id='my-date-picker-range',
        min_date_allowed=pd.to_datetime('1999-1-1'),
        max_date_allowed=pd.to_datetime('2003-1-4'),
        initial_visible_month=pd.to_datetime('1999-1-1'),
        end_date=pd.to_datetime('2003-1-4')
    ),
    dcc.Graph(
        id='figure',
        figure=fig,
        style={'width': '100%', 'height': '80vh'}
    )
])


@app.callback(
    dash.dependencies.Output('figure', 'figure'),
    [dash.dependencies.Input('my-date-picker-range', 'start_date'),
     dash.dependencies.Input('my-date-picker-range', 'end_date')])
def update_table(start_date, end_date):
    print('got request')
    print('start_date: ' + str(start_date))
    print('end_date: ' + str(end_date))
    fig = generateGraph(start_date, end_date)
    return fig


if __name__ == '__main__':
    preparedata()
    app.run_server(debug=True)


