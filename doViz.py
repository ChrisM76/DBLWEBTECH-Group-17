import pandas as pd
import plotly.express as px
from bokeh.models import (BasicTicker, ColorBar, ColumnDataSource,
                              LinearColorMapper, PrintfTickFormatter,
                              Label, ImageURL, RadioGroup, Button, Select,
                              Arrow, NormalHead, LabelSet)

class doViz:
    def __init__(self, generateNew=True):
        '''
        :param generateNew: true/false  regeneration takes a lot of resources, since this page is mainly stsic (does not react to new data, the static page can be used instead of generating it every time this will save cost and money :))
        '''
        self.generateNew = generateNew
        if generateNew:
            self.file_enron = './enron-v1.csv'
            self.enron_data = pd.read_csv(self.file_enron)
            self.enron_data_sorted_by_sentiment = object
            self.colorData()

    def colorData(self):
        ''''sort data'''

        sentiment_overview = self.enron_data['sentiment'].sort_values()
        self.enron_data_sorted_by_sentiment = self.enron_data.sort_values('sentiment')
        mapper = LinearColorMapper(palette="Viridis256", low=sentiment_overview.min(), high=sentiment_overview.max())

        self.enron_data_sorted_by_sentiment['COLOR'] = '.'
        for i in range(len(self.enron_data_sorted_by_sentiment)):
            val = self.enron_data_sorted_by_sentiment.at[i, 'sentiment']
            if val > 0:
                self.enron_data_sorted_by_sentiment.at[i, 'COLOR'] = 'green'
                # print('1')
            if val < 0:
                self.enron_data_sorted_by_sentiment.at[i, 'COLOR'] = 'red'
                # print('2')
            if val == 0:
                self.enron_data_sorted_by_sentiment.at[i, 'COLOR'] = 'black'
                # print('3')
        return self.enron_data_sorted_by_sentiment

    def first(self):
        ''''first plot??'''
        first = px.scatter(x=self.enron_data['date'], y=[self.enron_data['fromJobtitle']])
        # first.write_html('index.html', full_html=False, include_plotlyjs='cdn')
        html = first.to_html()
        return html

    def doColoredGraph(self):
        ''''colored graph'''
        self.enron_data_sorted_by_sentiment[self.enron_data_sorted_by_sentiment['sentiment'] == 0]# ==> ???? used for??
        colored_graph = px.scatter(x=self.enron_data_sorted_by_sentiment['date'],
                                   y=self.enron_data_sorted_by_sentiment['fromJobtitle'],
                                   color=self.enron_data_sorted_by_sentiment['COLOR'])
        # colored_graph.show()
        # colored_graph.write_html('index.html', full_html=False, include_plotlyjs='cdn')
        html = colored_graph.to_html()
        return html

    def doDirectorSentimentOverTime(self):
        '''do director sentiment over time'''
        director = self.enron_data_sorted_by_sentiment[self.enron_data_sorted_by_sentiment['fromJobtitle'] == 'Director']
        director_sentiment_over_time = px.scatter(x=director['date'],
                                                  y=director['sentiment'],
                                                  color=director['COLOR'])
        # director_sentiment_over_time.show()
        # director_sentiment_over_time.write_html('index.html', full_html=False, include_plotlyjs='cdn')
        html = director_sentiment_over_time.to_html()
        return html

    def doDianaSentimentOverTime(self):
        '''do diana sentiment over time'''
        director = self.enron_data_sorted_by_sentiment[self.enron_data_sorted_by_sentiment['fromJobtitle'] == 'Director']

        diana = self.enron_data_sorted_by_sentiment[self.enron_data_sorted_by_sentiment['fromEmail'] == 'diana.scholtes@enron.com']
        diana_sentiment_over_time = px.scatter(x=director['date'],
                                               y=director['sentiment'],
                                               color=director['COLOR'])
        # diana_sentiment_over_time.show()
        # diana_sentiment_over_time.write_html('index.html', full_html=False, include_plotlyjs='cdn')
        html = diana_sentiment_over_time.to_html()
        return html

if __name__ == '__main__':
    test = doViz()
    test.doDianaSentimentOverTime()
