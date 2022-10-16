from django.shortcuts import render, HttpResponse, redirect
from django.template import loader
from django.urls import reverse
from django.http import HttpResponseRedirect

from .forms import ContactForm, EventIDForm, SetUpIDForm, Input_Picture, Input_Number, EventIDFormPicture


def create_event(request):
    
    if request.method == "POST":
        
        #query sql and make a new group id


        form = SetUpIDForm(request.POST)
        if form.is_valid():
            random_event_number = 1
            lst_nm = form.cleaned_data['list_of_names']
            # split list of names by string then
            # query sql with group id and add names

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



def create_invoice_with_group(request, Event_ID):

    template = loader.get_template('throwaway.html')  
    context = {
    }
    # query the sql and then do the algorithm and return the invoice

    return HttpResponse(template.render(context, request)) 


def add_purchase(request):

    if request.method == "POST":
        random_event_number = 1
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
        random_event_number = 1
        form = Input_Number(request.POST)
        if form.is_valid():
            money_inputted = form.cleaned_data['amount_id']
            people_added = form.cleaned_data['list_of_users']
            user = form.cleaned_data['user']
            #query the sql with event ID and then add the other data to the database


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

    # query with event id and put it in 

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



            return redirect(url)
            #return render(request, 'index.html', {'form': form, 'img_obj': img_obj})
        return render(request, 'upload_picture.html', {'form': form})
    else:
        form = Input_Picture()
        return render(request, 'upload_picture.html', {'form': form})

