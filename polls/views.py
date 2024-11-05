from django.http import HttpResponse
from django.template import loader

from .models import Question

def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    template = loader.get_template("polls/index.html")
    context = {
        "latest_question_list": latest_question_list,
    }
    return HttpResponse(template.render(context, request))
    # Carrega o template polls/index.html e passa um contexto

def detail(request, question_id):
    return HttpResponse("Detalhando a questão de ID %s." % question_id)

def results(request, question_id):
    response = "Resultados da questão de ID %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("Votando para a questão %s." % question_id)
