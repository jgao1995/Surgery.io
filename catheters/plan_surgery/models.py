from __future__ import unicode_literals

from django.db import models
from jsonfield import JSONField

# Create your models here.


# Create your models here.

class Device(models.Model):
    manufacturer = models.CharField(max_length=500)
    brand_name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    product_type = models.CharField(max_length=200)

    dimensions = JSONField()


# def add_device():
    # ''' take in all that stuff ^
    # return true/false if it works out'''
    # return False

    # question_text = models.CharField(max_length=200)
    # pub_date = models.DateTimeField('date published')


# class Choice(models.Model):
#     question = models.ForeignKey(Question, on_delete=models.CASCADE)
#     choice_text = models.CharField(max_length=200)
#     votes = models.IntegerField(default=0)