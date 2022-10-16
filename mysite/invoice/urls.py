from django.urls import path

from . import views

from django.conf import settings

from django.conf.urls.static import static


urlpatterns = [

    path('create_event/', views.create_event, name='create_event'),

    path('create_invoice/', views.create_invoice, name='create_invoice'),
    path('create_invoice/<int:Event_ID>/', views.create_invoice_with_group, name='create_invoice_with_group'),


    path('add_purchase/', views.add_purchase, name='add_purchase'),
    path('add_purchase/<int:Event_ID>/', views.add_purchase_with_group, name='add_purchase_with_group'),
    path('add_purchase_pic/<int:Event_ID>/', views.add_purchase_pic, name='add_purchase_pic'),
    

    path('total_transactions/', views.total_transactions, name='total_transactions'),
    path('total_transactions/<int:Event_ID>/', views.total_transactions_with_group, name='total_transactions_with_group'),

]


if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
