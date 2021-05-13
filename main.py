from flask import Flask
from doViz import doViz
app = Flask(__name__)
doDianaSentimentOverTime = ''
@app.route("/")
def index():
    homePage = '<br> <a href="/doDianaSentimentOverTime"> doDianaSentimentOverTime </a><br><br>' \
               '<br> <a href="/doDirectorSentimentOverTime"> doDirectorSentimentOverTime </a><br><br>' \
               '<br> <a href="/doColoredGraph"> doColoredGraph </a><br><br>' \
               '<br> <a href="/first"> first <a>'

    return homePage

@app.route("/doDianaSentimentOverTime")
def doDianaSentimentOverTime():
    viz = doViz()
    html = viz.doDianaSentimentOverTime()
    return html

@app.route("/doDirectorSentimentOverTime")
def doDirectorSentimentOverTime():
    viz = doViz()
    html = viz.doDianaSentimentOverTime()
    return html

@app.route("/doColoredGraph")
def doColoredGraph():
    viz = doViz()
    html = viz.doColoredGraph()
    return html

@app.route("/first")
def first():
    viz = doViz()
    html = viz.first()
    return html
	

if __name__ == "__main__":
	app.run(host="127.0.0.1", port=8080, debug=True)