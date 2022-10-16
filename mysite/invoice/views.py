from asyncio import events
from django.shortcuts import render, HttpResponse, redirect
from django.template import loader
from django.urls import reverse
from django.http import HttpResponseRedirect
from invoice.models import Transactions, People
from django_pandas.io import read_frame
import pandas as pd
import requests

from .forms import ContactForm, EventIDForm, SetUpIDForm, Input_Picture, Input_Number, EventIDFormPicture


def create_event(request):

    if request.method == "POST":
        form = SetUpIDForm(request.POST)
        if form.is_valid():
            ids = list(Transactions.objects.all().values_list('Event_ID'))
            random_event_number = 1
            if len(ids) != 0:
                random_event_number = sorted(ids)[-1] + 1
            lst_nm = form.cleaned_data['list_of_names']
            lst_nm = lst_nm.split(",")
            for i in lst_nm:
                People.objects.create(Event_ID=random_event_number, Name=i)

            url = '/invoice/total_transactions/'+ str(random_event_number) +'/'
            return redirect(url)
        return render( request, 'new_event_id.html', {'form': form} )
    else:
        form = SetUpIDForm()
        return render( request, 'new_event_id.html', {'form': form})



def create_invoice(request):

    if request.method == "POST":
        random_event_number = 1
        form = EventIDForm(request.POST)
        if form.is_valid():
            lst_nm = form.cleaned_data['event_id']
            url = '/invoice/create_invoice/' + str(lst_nm) + '/'
            return redirect(url)
        return render( request, 'get_event_id.html', {'form': form} )
    else:
        form = EventIDForm()
        return render( request, 'get_event_id.html', {'form': form})

def process(Event_ID):
    qs = Transactions.objects.all()
    transac = read_frame(qs)
    pplQS = People.objects.all()
    ppl = read_frame(pplQS)
    names = pd.Series(ppl[ppl['Event_ID'] == Event_ID]['Name']).to_list()
    transac = transac[transac['Event_ID'] == Event_ID]
    transac['Person_ID'] = transac['Person_ID'].apply(lambda x: names.index(x))
    transac['Owed_By'] = transac['Owed_By'].apply(lambda x: [names.index(i) for i in x.split(',')])
    arr = [0] * len(names)
    def group (row):
        arr[row['Person_ID']] += row['Payment']
        for i in row['Owed_By']:
            arr[i] -= (row['Payment']/len(row['Owed_By']))

    transac = transac.apply(lambda row: group(row), axis=1)
    payments = [[0 for i in arr] for j in arr]
    for i in range(len(arr)):
        if arr[i] < 0:
            for j in range(len(arr)):
                if arr[j] > -1 * arr[i]:
                    payments[i][j] = -1*arr[i]
                    arr[i] = 0
                    arr[j] += arr[i]
                    break;
            if arr[i] != 0:
                for j in range(len(arr)):
                    if arr[j] > 0:
                        if arr[i] + arr[j] > 0:
                            payments[i][j] = -1*arr[i]
                            arr[i] = 0
                            arr[j] += arr[i]
                            break;
                        else:
                            payments[i][j] = arr[j]
                            arr[j] = 0
                            arr[i] += arr[j]

    result = ""

    for i, val in enumerate(payments):
        for j, val2 in enumerate(val):
            if val2 != 0:
                result += str(names[i]) + " Owes " + str(names[j]) + " $" + str(val2) + '\n'
    return result


def create_invoice_with_group(request, Event_ID):

    template = loader.get_template('throwaway.html')
    context = {
    }

    result = process(Event_ID)

    return HttpResponse(template.render(context, request))


def add_purchase(request):

    if request.method == "POST":
        form = EventIDFormPicture(request.POST)
        if form.is_valid():
            lst_nm = form.cleaned_data['event_id']
            is_picture = form.cleaned_data['is_picture']
            if (is_picture == "1"):
                url = '/invoice/add_purchase_pic/' + str(lst_nm) + '/'
                return redirect(url)
            else:
                url = '/invoice/add_purchase/' + str(lst_nm) + '/'
                return redirect(url)
        return render( request, 'get_event_add_purchase.html', {'form': form} )
    else:
        form = EventIDFormPicture()
        return render( request, 'get_event_add_purchase.html', {'form': form})



def add_purchase_with_group(request, Event_ID):

    if request.method == "POST":
        form = Input_Number(request.POST)
        if form.is_valid():
            money_inputted = form.cleaned_data['amount_id']
            people_added = form.cleaned_data['list_of_users']
            user = form.cleaned_data['user']
            Transactions.objects.create(Event_ID=Event_ID, Person_ID=user, Payment=money_inputted, Owed_By=people_added)
            url = '/invoice/total_transactions/' + str(Event_ID) + '/'
            return redirect(url)
        return render( request, 'get_event_id.html', {'form': form} )
    else:
        form = Input_Number()
        return render( request, 'get_event_id.html', {'form': form})


def total_transactions(request):

    if request.method == "POST":
        random_event_number = 1
        form = EventIDForm(request.POST)
        if form.is_valid():
            lst_nm = form.cleaned_data['event_id']
            url = '/invoice/total_transactions/' + str(lst_nm) + '/'
            return redirect(url)
        return render( request, 'get_event_id.html', {'form': form} )
    else:
        form = EventIDForm()
        return render( request, 'get_event_id.html', {'form': form})



def total_transactions_with_group(request, Event_ID):

    return render(request, 'throwaway.html', {'id_event': Event_ID})

'''
def add_purchase_pic(request, Event_ID):
    """Process images uploaded by users"""
    if request.method == 'POST':
        form = Input_Picture(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            img_obj = form.instance
            #  do the cv thing and add to sql
            url = '/invoice/total_transactions/' + str(Event_ID) + '/'


            people_added = form.cleaned_data['list_of_users']
            user = form.cleaned_data['user']
            #query the sql with event ID and then add the other data to the database



            return redirect(url)
            #return render(request, 'index.html', {'form': form, 'img_obj': img_obj})
        return render(request, 'upload_picture.html', {'form': form})
    else:
        form = Input_Picture()
        return render(request, 'upload_picture.html', {'form': form})
'''

def add_purchase_pic(request, Event_ID):
    """Process images uploaded by users"""
    if request.method == 'POST':
        #form = Input_Picture(request.POST, request.FILES)
        form = Input_Picture(request.POST)
        if form.is_valid():
            form.save()
            #img_obj = form.instance
            #  do the cv thing and add to sql
            url = '/invoice/total_transactions/' + str(Event_ID) + '/'

            image = form.cleaned_data['image']
            people_added = form.cleaned_data['list_of_users']
            user = form.cleaned_data['user']
            #query the sql with event ID and then add the other data to the database


            receipt_total = 0
            url = 'https://app.nanonets.com/api/v2/OCR/Model/982478f6-90c5-499e-9b48-eeb6e426799f/LabelFile/?async=false'
            data = {'file': open(image, 'rb')}

            response = requests.post(url, auth=requests.auth.HTTPBasicAuth('CmA1d2TLu4eaJ2vq2QRTVP6TzvMrub0W', ''), files=data)

            objects = response.json()['result'][0]['prediction']
            for obj in objects:
                if obj['label'] == 'Total_Amount':
                    receipt_total = int(obj['ocr_text'])


            return redirect(url)
            #return render(request, 'index.html', {'form': form, 'img_obj': img_obj})
        return render(request, 'upload_picture.html', {'form': form})
    else:
        form = Input_Picture()

        return render(request, 'upload_picture.html', {'form': form})
