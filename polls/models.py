import datetime

from django.db import models
from django.utils import timezone
from django.contrib import admin

# Modelos de pergunta e resposta
# As classes herdam django.db.models.Model

class Question(models.Model):
    # Colunas
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")
    def __str__(self): # retorna representação em string
        return self.question_text
    @admin.display(
        boolean=True,
        ordering="pub_date",
        description="Published recently?",
    )
    def was_published_recently(self):
        now = timezone.now()
        # ontem <= data <= hoje
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

class Choice(models.Model):
    # Colunas
    question = models.ForeignKey(Question, on_delete=models.CASCADE) # Question ->1+ choice, choice ->1 question
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text
