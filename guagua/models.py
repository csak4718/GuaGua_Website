from django.db import models

# Create your models here.
class Question(models.Model):
    question_id = models.CharField(max_length=200)
    numA = models.IntegerField(default=0)
    numB = models.IntegerField(default=0)
    choiceA = models.CharField(max_length=200)
    choiceB = models.CharField(max_length=200)        
    title = models.CharField(max_length=200)
    tag = models.CharField(max_length=200)
    createdAt = models.DateTimeField('created at')
    updatedAt = models.DateTimeField('updated at')
        

class Comments(models.Model):
    question = models.ForeignKey(Question)
    msg = models.CharField(max_length=200)
    createdAt = models.DateTimeField('created at')
    updatedAt = models.DateTimeField('updated at')