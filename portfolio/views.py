from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import *
from .forms import *
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.db.models import Sum
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CustomerSerializer
from django.core.mail import EmailMessage
from django.template.loader import get_template
from io import BytesIO
from io import StringIO  ## for Python 3
from django.core.mail import send_mail
from django.core.mail import EmailMessage

from efs import settings
from xhtml2pdf import pisa
from django.http import HttpResponse
from django.views.generic import View
from .utils import render_to_pdf
now = timezone.now()
def home(request):
   return render(request, 'portfolio/home.html',
                 {'portfolio': home})

now = timezone.now()
def home(request):
   return render(request, 'portfolio/home.html',
                 {'portfolio': home})

@login_required
def customer_list(request):

    #send_mail('Example Subject', 'Example message', 'jdyesh@gmail.com', ['yesh080690@gmail.com'])
    customer = Customer.objects.filter(created_date__lte=timezone.now())
    return render(request, 'portfolio/customer_list.html',
                 {'customers': customer})

@login_required
def customer_new(request):
   if request.method == "POST":
       form = CustomerForm(request.POST)
       if form.is_valid():
           customer = form.save(commit=False)
           customer.save()
           customer = Customer.objects.filter(created_date__lte=timezone.now())
           return render(request, 'portfolio/customer_list.html',
                         {'customers': customer})
   else:
       form = CustomerForm()
       # print("Else")
   return render(request, 'portfolio/customer_new.html', {'form': form})



@login_required
def customer_edit(request, pk):
   customer = get_object_or_404(Customer, pk=pk)
   if request.method == "POST":
       # update
       form = CustomerForm(request.POST, instance=customer)
       if form.is_valid():
           customer = form.save(commit=False)
           customer.updated_date = timezone.now()
           customer.save()
           customer = Customer.objects.filter(created_date__lte=timezone.now())
           return render(request, 'portfolio/customer_list.html',
                         {'customers': customer})
   else:
        # edit
       form = CustomerForm(instance=customer)
   return render(request, 'portfolio/customer_edit.html', {'form': form})

@login_required
def customer_delete(request, pk):
   customer = get_object_or_404(Customer, pk=pk)
   customer.delete()
   return redirect('portfolio:customer_list')


@login_required
def stock_list(request):
   stocks = Stock.objects.filter(purchase_date__lte=timezone.now())
   return render(request, 'portfolio/stock_list.html', {'stocks': stocks})

@login_required
def stock_new(request):
   if request.method == "POST":
       form = StockForm(request.POST)
       if form.is_valid():
           stock = form.save(commit=False)
           stock.created_date = timezone.now()
           stock.save()
           stocks = Stock.objects.filter(purchase_date__lte=timezone.now())
           return render(request, 'portfolio/stock_list.html',
                         {'stocks': stocks})
   else:
       form = StockForm()
       # print("Else")
   return render(request, 'portfolio/stock_new.html', {'form': form})


@login_required
def stock_edit(request, pk):
   stock = get_object_or_404(Stock, pk=pk)
   if request.method == "POST":
       form = StockForm(request.POST, instance=stock)
       if form.is_valid():
           stock = form.save()
           # stock.customer = stock.id
           stock.updated_date = timezone.now()
           stock.save()
           stocks = Stock.objects.filter(purchase_date__lte=timezone.now())
           return render(request, 'portfolio/stock_list.html', {'stocks': stocks})
   else:
       # print("else")
       form = StockForm(instance=stock)
   return render(request, 'portfolio/stock_edit.html', {'form': form})


@login_required
def stock_delete(request, pk):
   stock = get_object_or_404(Stock, pk=pk)
   stock.delete()
   return redirect('portfolio:stock_list')



@login_required
def investment_list(request):
   investment = Investment.objects.filter(acquired_date__lte=timezone.now())
   return render(request, 'portfolio/investment_list.html', {'investment': investment})

@login_required
def investment_new(request):
   if request.method == "POST":
       form = InvestmentForm(request.POST)
       if form.is_valid():
           investment = form.save(commit=False)
           investment.recent_date_date = timezone.now()
           investment.save()
           investment = Investment.objects.filter()
           return render(request, 'portfolio/investment_list.html',
                         {'investment': investment})
   else:
       form = InvestmentForm()
       # print("Else")
   return render(request, 'portfolio/investment_new.html', {'form': form})


@login_required
def investment_edit(request, pk):
   investment = get_object_or_404(Investment, pk=pk)
   if request.method == "POST":
       form = InvestmentForm(request.POST, instance=investment)
       if form.is_valid():
           investment = form.save()
           # stock.customer = stock.id
           investment.updated_date = timezone.now()
           investment.save()
           investment = Investment.objects.filter(acquired_date__lte=timezone.now())
           return render(request, 'portfolio/investment_list.html', {'investment': investment})
   else:
       # print("else")
       form = InvestmentForm(instance=investment)
   return render(request, 'portfolio/investment_edit.html', {'form': form})


@login_required
def investment_delete(request, pk):
   investment = get_object_or_404(Investment, pk=pk)
   investment.delete()
   return redirect('portfolio:investment_list')


@login_required
def portfolio(request,pk):
   customer = get_object_or_404(Customer, pk=pk)
   customers = Customer.objects.filter(created_date__lte=timezone.now())
   investments =Investment.objects.filter(customer=pk)
   stocks = Stock.objects.filter(customer=pk)
   mutualfund = MutualFund.objects.filter(customer=pk)
   #sum_recent_value = Investment.objects.filter(customer=pk).aggregate(Sum('recent_value'))
   sum_recent_value = Investment.objects.filter(customer=pk).aggregate(recent_sum=Sum('recent_value'))['recent_sum']
   #sum_acquired_value = Investment.objects.filter(customer=pk).aggregate(Sum('acquired_value'))
   sum_acquired_value = Investment.objects.filter(customer=pk ).aggregate(acquired_sum=Sum('acquired_value'))['acquired_sum']
   sum_acquired_value_mf = MutualFund.objects.filter(customer=pk).aggregate(acquired_sum=Sum('acquired_value'))['acquired_sum']
   sum_recent_value_mf = MutualFund.objects.filter(customer=pk).aggregate(recent_sum=Sum('recent_value'))['recent_sum']

   #overall_investment_results = sum_recent_value-sum_acquired_value
   # Initialize the value of the stocks
   sum_current_stocks_value = 0
   sum_of_initial_stock_value = 0

   # Loop through each stock and add the value to the total
   for stock in stocks:
        sum_current_stocks_value += stock.current_stock_value()
        sum_of_initial_stock_value += stock.initial_stock_value()
   portfolio_initial_investments = float(sum_of_initial_stock_value) + float(sum_acquired_value) + float(
       sum_acquired_value_mf)
   portfolio_current_investments = float(sum_current_stocks_value) + float(sum_recent_value) + float(
       sum_recent_value_mf)

   return render(request, 'portfolio/portfolio.html', {'customers': customers,
                                                       'customer': customer,
                                                       'investments': investments,
                                                       'stocks': stocks,
                                                       'mutualfund':mutualfund,
                                                       'sum_acquired_value': sum_acquired_value,
                                                       'sum_recent_value': sum_recent_value,
                                                        'sum_current_stocks_value': sum_current_stocks_value,
                                                        'sum_of_initial_stock_value': sum_of_initial_stock_value,
                                                       'portfolio_initial_investments': portfolio_initial_investments,
                                                       'portfolio_current_investments': portfolio_current_investments,
                                                       'sum_acquired_value_mf':sum_acquired_value_mf,
                                                       'sum_recent_value_mf':sum_recent_value_mf


                                                       })


# Lists all customers
class CustomerList(APIView):

    def get(self,request):
        customers_json = Customer.objects.all()
        serializer = CustomerSerializer(customers_json, many=True)
        return Response(serializer.data)



@login_required
def mutualfund_list(request):
   mutualfund = MutualFund.objects.filter(acquired_date__lte=timezone.now())
   return render(request, 'portfolio/mutualfund_list.html', {'mutualfund': mutualfund})

@login_required
def mutualfund_new(request):
   if request.method == "POST":
       form = MutualFundForm(request.POST)
       if form.is_valid():
           mutualfund = form.save(commit=False)
           mutualfund.recent_date_date = timezone.now()
           mutualfund.save()
           mutualfund = MutualFund.objects.filter()
           return render(request, 'portfolio/mutualfund_list.html',
                         {'mutualfund': mutualfund})
   else:
       form = MutualFundForm()
       # print("Else")
   return render(request, 'portfolio/mutualfund_new.html', {'form': form})


@login_required
def mutualfund_edit(request, pk):
   mutualfund = get_object_or_404(MutualFund, pk=pk)
   if request.method == "POST":
       form = MutualFundForm(request.POST, instance=mutualfund)
       if form.is_valid():
           mutualfund = form.save()
           # stock.customer = stock.id
           mutualfund.updated_date = timezone.now()
           mutualfund.save()
           mutualfund = MutualFund.objects.filter(acquired_date__lte=timezone.now())
           return render(request, 'portfolio/mutualfund_list.html', {'mutualfund': mutualfund})
   else:
       # print("else")
       form = MutualFundForm(instance=mutualfund)
   return render(request, 'portfolio/mutualfund_edit.html', {'form': form})


@login_required
def mutualfund_delete(request, pk):
   mutualfund = get_object_or_404(MutualFund, pk=pk)
   mutualfund.delete()
   return redirect('portfolio:mutualfund_list')




def download_pdf(request, pk):
 #item = get_object_or_404(object, id=pk)
 customer = get_object_or_404(Customer, pk=pk)
 customers = Customer.objects.filter(created_date__lte=timezone.now())
 investments = Investment.objects.filter(customer=pk)
 stocks = Stock.objects.filter(customer=pk)
 mutualfund = MutualFund.objects.filter(customer=pk)
 # sum_recent_value = Investment.objects.filter(customer=pk).aggregate(Sum('recent_value'))
 sum_recent_value = Investment.objects.filter(customer=pk).aggregate(recent_sum=Sum('recent_value'))['recent_sum']
 # sum_acquired_value = Investment.objects.filter(customer=pk).aggregate(Sum('acquired_value'))
 sum_acquired_value = Investment.objects.filter(customer=pk).aggregate(acquired_sum=Sum('acquired_value'))[
     'acquired_sum']
 sum_acquired_value_mf = MutualFund.objects.filter(customer=pk).aggregate(acquired_sum=Sum('acquired_value'))[
     'acquired_sum']
 sum_recent_value_mf = MutualFund.objects.filter(customer=pk).aggregate(recent_sum=Sum('recent_value'))['recent_sum']

 # overall_investment_results = sum_recent_value-sum_acquired_value
 # Initialize the value of the stocks
 sum_current_stocks_value = 0
 sum_of_initial_stock_value = 0

 # Loop through each stock and add the value to the total
 for stock in stocks:
     sum_current_stocks_value += stock.current_stock_value()
     #sum_current_stocks_value +=100
     sum_of_initial_stock_value += stock.initial_stock_value()
     #sum_of_initial_stock_value +=0
 portfolio_initial_investments = float(sum_of_initial_stock_value) + float(sum_acquired_value) + float(
     sum_acquired_value_mf)
 portfolio_current_investments = float(sum_current_stocks_value) + float(sum_recent_value) + float(
     sum_recent_value_mf)
 investment = Investment.objects.filter(acquired_date__lte=timezone.now())

 context = {'customers': customers,
                                                       'investments': investments,
                                                       'stocks': stocks,
                                                       'customer':customer,
                                                       'mutualfund':mutualfund,
                                                       'sum_acquired_value': sum_acquired_value,
                                                       'sum_recent_value': sum_recent_value,
                                                       'sum_current_stocks_value': sum_current_stocks_value,
                                                       'sum_of_initial_stock_value': sum_of_initial_stock_value,
                                                       'portfolio_initial_investments': portfolio_initial_investments,
                                                       'portfolio_current_investments': portfolio_current_investments,
                                                       'sum_acquired_value_mf':sum_acquired_value_mf,
                                                       'sum_recent_value_mf':sum_recent_value_mf
      }


 template_name = 'portfolio/portfolio_download.html'
 user_email=request.user.email
 pdf = render_to_pdf(user_email,template_name, context)
 return HttpResponse(pdf, content_type='application/pdf')


