

from django import forms
from .models import Image

INPUT_METHOD = (
    ("1","Picture Upload"),
    ("2", "Type In Number")

)

class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100
    )
    email = forms.EmailField()

class EventIDForm(forms.Form):
    event_id = forms.IntegerField()


class EventIDFormPicture(forms.Form):
    is_picture = forms.ChoiceField(choices = INPUT_METHOD)
    event_id = forms.IntegerField()



class SetUpIDForm(forms.Form):
    list_of_names = forms.CharField(max_length=30000)
    
    
class Input_Number(forms.Form):
    amount_id = forms.IntegerField()
    list_of_users = forms.CharField(max_length=30000)
    user = forms.CharField(max_length=100)




class Input_Picture(forms.Form):
    list_of_users = forms.CharField(max_length=30000)
    user = forms.CharField(max_length=100)
    image = forms.ImageField()
