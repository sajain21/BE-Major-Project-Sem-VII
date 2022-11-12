from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import plotly.graph_objects as go
import nltk
from nltk.corpus import stopwords
import os

nltk.download('stopwords')

set(stopwords.words('english'))


def gauge_plot(compound, i):
    i = str(i)
    fig = go.Figure(go.Indicator(
        value=compound,
        mode="gauge+number",
        title={'text': "Sentiment Gauge"},
        gauge={'axis': {'range': [-1, 1]},
               'bar': {'color': "lightgray"},
               'steps': [
             {'range': [-1, 0], 'color': "red"},
             {'range': [0, 1], 'color': "green"}],
            'threshold': {'line': {'color': "black", 'width': 6}, 'thickness': 0.75, 'value': compound}}))

    fig.write_image('static/IMG/gauge' + i + '.png')


def pie_plot(pos, neu, neg):
    labels = ["Positive", "Neutral", "Negative"]
    values = [pos, neu, neg]

    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
    fig.write_image('static/IMG/pie.png')


gauge = 'static/IMG/gauge99.png'


app = Flask(__name__)

IMG_FOLDER = os.path.join('static', 'IMG')

app.config['UPLOAD_FOLDER'] = IMG_FOLDER


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def predict_text():
    stop_words = stopwords.words('english')

    # convert to lowercase
    text1 = request.form['message'].lower()

    text_final = ''.join(c for c in text1 if not c.isdigit())

    processed_doc1 = ' '.join(
        [word for word in text_final.split() if word not in stop_words])

    sa = SentimentIntensityAnalyzer()
    dd = sa.polarity_scores(text=processed_doc1)
    print(dd)

    pie_plot(dd['pos'], dd['neu'], dd['neg'])

    gauge_plot(dd['compound'], 1)

    pie = os.path.join(app.config['UPLOAD_FOLDER'], 'pie.png')
    gauge = os.path.join(app.config['UPLOAD_FOLDER'], 'gauge1.png')

    return render_template('predict.html', final=dd['compound'], text1=text_final, pie_plot=pie, gauge_plot=gauge)


@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        f.save(secure_filename(f.filename))
        df = pd.read_csv(f.filename)
        sid = SentimentIntensityAnalyzer()
        sid.polarity_scores(df.iloc[0]['text'])
        df['scores'] = df['text'].apply(
            lambda review: sid.polarity_scores(review))

        y = 0
        for i in range(len(df)):
            y = y + df['scores'][i]['compound']
        y = y / (len(df))
        gauge_plot(y, len(df))

        pos_tweet = 0
        neg_tweet = 0
        neu_tweet = 0
        for i in range(len(df)):
            if df['scores'][i]['compound'] > 0.05:
                pos_tweet += 1
            elif df['scores'][i]['compound'] < 0.05:
                neg_tweet += 1
            else:
                neu_tweet += 1
        return render_template('uploader.html', gauge_plot1=gauge, pos=pos_tweet, neg=neg_tweet, neu=neu_tweet)


if __name__ == '__main__':
    app.run(debug=True)
