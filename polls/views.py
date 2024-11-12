from django.db.models import F
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .models import Choice, Question

def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    context = {
        "latest_question_list": latest_question_list,
    }
    # return HttpResponse(template.render(context, request))
    return render(request, "polls/index.html", context)
    # Carrega o template polls/index.html e passa um contexto

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/detail.html", {"question": question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/results.html", {"question": question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Exibe novamente o form
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "Você não fez uma escolha.",
            },
            )
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()

        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))