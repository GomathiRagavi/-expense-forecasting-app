

# Create your views here.
from django.shortcuts import render, redirect
from .models import Expense
from .forms import ExpenseForm
from prophet import Prophet
import pandas as pd

def home(request):
    form = ExpenseForm()
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    expenses = Expense.objects.all()
    return render(request, 'forecast/home.html', {'form': form, 'expenses': expenses})

def forecast_view(request):
    expenses = Expense.objects.all().values()
    df = pd.DataFrame(expenses)
    if not df.empty:
        df = df.rename(columns={'date': 'ds', 'amount': 'y'})
        model = Prophet()
        model.fit(df[['ds', 'y']])
        future = model.make_future_dataframe(periods=7)
        forecast = model.predict(future)
        forecast_html = forecast[['ds', 'yhat']].tail(7).to_html()
    else:
        forecast_html = "<p>Not enough data to forecast.</p>"
    return render(request, 'forecast/forecast.html', {'forecast': forecast_html})

