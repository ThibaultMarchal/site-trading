from django.shortcuts import render, redirect
from AppTrading.models import Titre, Action, Portefeuille
import yfinance as yf
from django.shortcuts import get_object_or_404
from plotly.offline import plot
import plotly.graph_objs as go
from django.contrib.auth.decorators import login_required
import plotly.io as pio
from datetime import datetime, timedelta


# Create your vies here.


@login_required
def add_action(request, titre):
    titre = get_object_or_404(Titre, ticker=titre)
    print(request.user)
    if request.method == 'POST':
        value = request.POST['value']
        type = request.POST['type']
        if type == "buy":
            buys = "buy"
        if type == "sell":
            buys = 'sell'

        prtf = Portefeuille.objects.get(author=request.user)
        if int(value) < int(prtf.value):
            prtf.value = int(prtf.value) - int(value)
            prtf.save()
            action = Action(author=request.user, value=value,
                            portefeuille=prtf, buy=buys, titre_action=titre)
            action.save()
            return redirect('home')

    plot_div = titre.graphe
    context = {
        'titre': titre,
        'plot_div': plot_div,
        'portefeuille': Portefeuille.objects.filter(author=request.user),
    }
    return render(request, 'add_action.html', context)


@login_required
def home(request):
    actions = Action.objects.filter(author=request.user)
    all_change = []
    for action in actions:
        diff = action.variation
        change = action.value-diff
        change = round(change, 2)
        all_change.append([change, action])

    context = {
        'titres': Titre.objects.all(),
        'actions': Action.objects.filter(author=request.user),
        'tert': len(all_change),
        'change': all_change,
        'portefeuille': Portefeuille.objects.filter(author=request.user)

    }
    return render(request, 'home.html', context)


@login_required
def home_titre(request, titre):
    titre = get_object_or_404(Titre, ticker=titre)

    plot_div = titre.graphe

    context = {
        'titre': titre,
        'ticker': titre.ticker,
        'plot_div': plot_div,
        'margin': titre.difference,
        'portefeuille': Portefeuille.objects.filter(author=request.user),
    }
    return render(request, 'titre.html', context=context)


@login_required
def titre(request):
    context = {
        'titres': Titre.objects.all(),
        'actions': Action.objects.filter(author=request.user),
        'portefeuille': Portefeuille.objects.filter(author=request.user),
    }
    return render(request, 'liste_titre.html', context=context)


@login_required
def sell_action(request, id):
    action = Action.objects.get(id=id)
    prtf = Portefeuille.objects.get(author=request.user)
    diff = action.variation
    if action.buy == 'buy':
        prtf.value = prtf.value + diff
    if action.buy == "sell":
        diffe = action.value - diff
        act = action.value + diffe
        prtf.value = prtf.value + act

    prtf.save()
    action.delete()
    return redirect('home')
