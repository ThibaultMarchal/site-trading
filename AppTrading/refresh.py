import schedule
import time
from AppTrading import models
from datetime import datetime, timedelta
import yfinance as yf
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
import plotly.io as pio
from plotly.offline import plot
import plotly.graph_objs as go


def calcul_difference(action):
    ticker = yf.Ticker(f'{action.titre_action.ticker}.PA')
    start = action.creation_date.strftime("%Y-%m-%d")
    now = datetime.now()
    now1 = now.strftime("%Y-%m-%d")
    # Plage de 30 jours incluant la date spécifiée
    start_date = action.creation_date - timedelta(days=1)
    end_date = action.creation_date + timedelta(days=1)
    data = yf.download(f'{action.titre_action.ticker}.PA',
                       start=start_date, end=end_date)
    price_start = data.loc[start]
    price_start1 = float(price_start['Open'])
    # Plage de 30 jours incluant la date spécifiée
    start_date1 = now - timedelta(days=2)
    end_date1 = now + timedelta(days=1)
    data1 = yf.download(f'{action.titre_action.ticker}.PA',
                        start=start_date1, end=end_date1)

    price_end = data1.loc[now1]
    price_end1 = float(price_end['Open'])
    diff = (price_end1/price_start1)
    change = diff*action.value
    return change


def calcul_difference_titre(Titre):
    ticker = yf.Ticker(f'{Titre.ticker}.PA')
    now = datetime.now()
    start = now - timedelta(days=1)
    start1 = start.strftime("%Y-%m-%d")
    now1 = now.strftime("%Y-%m-%d")
    # Plage de 30 jours incluant la date spécifiée
    start_date = start - timedelta(days=2)
    end_date = start + timedelta(days=1)
    data = yf.download(f'{Titre.ticker}.PA',
                       start=start_date, end=end_date)
    price_start = data.loc[start1]
    price_start1 = float(price_start['Open'])
    # Plage de 30 jours incluant la date spécifiée
    start_date1 = now - timedelta(days=2)
    end_date1 = now + timedelta(days=1)
    data1 = yf.download(f'{Titre.ticker}.PA',
                        start=start_date1, end=end_date1)

    price_end = data1.loc[now1]
    price_end1 = float(price_end['Open'])
    diff = (price_end1/price_start1)
    change = diff-1
    change = change*100
    changes = round(change, 2)
    return changes


def create_graphe(titre):
    t = yf.Ticker(f'{titre.ticker}.PA')
    hist = t.history(period='12mo')
    pio.templates.default = "plotly_dark"

    fig = go.Scatter(x=hist.index, y=hist['Open'])
    fig2 = go.Figure(fig)
    fig2.update_layout(
        plot_bgcolor='#1E1E1E',  # Couleur de fond du graphique
        paper_bgcolor='#1E1E1E',  # Couleur de fond du papier
        font_color='#FFFFFF',  # Couleur du texte
    )
    plot_div = plot(fig2, output_type='div')
    return plot_div


def add_info():
    actions = models.Action.objects.all()
    for action in actions:
        try:
            difference = calcul_difference(action)
            action.variation = difference
            action.save()
        except:
            action.variation = 0.0
            print('BUG : ', action.titre_action.ticker)
    print('action')
    titres = models.Titre.objects.all()
    for titre in titres:
        try:
            difference = calcul_difference_titre(titre)
            titre.difference = difference
            titre.save()
        except:
            titre.difference = 0.0
            print('BUG', titre.name)
    print('titre')

    for titre in titres:
        graph = create_graphe(titre)
        titre.graphe = graph
        titre.save()
        print('titre sauvé')


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(add_info, 'interval', seconds=3600)
    scheduler.start()
