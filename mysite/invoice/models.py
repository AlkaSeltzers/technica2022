from django.db import models


class Transactions(models.Model):
    Event_ID = models.IntegerField(default=0)
    Person_ID = models.IntegerField(default=0)
    Payment = models.IntegerField(default=0)
    Owed_By = models.CharField(max_length=200)


class Image(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images')

    def __str__(self):
        return self.title