import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question

def create_question(question_text, days):
    time = timezone.now() + datetime.timedelta(days=days) # inimigo do this.?
    return Question.objects.create(question_text=question_text, pub_date=time)

# Voltado para testar as views
class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Nenhuma enquete disponível.")
        self.assertQuerySetEqual(response.context["latest_question_list"], [])

    def test_past_question(self):
        question = create_question(question_text="Pergunta passada", days=-30)
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(
            response.context["latest_question_list"],
            [question],
        )

    def test_future_question(self):
        create_question(question_text="Pergunta futura", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "Nenhuma enquete disponível.")
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [],
        )

    def test_future_and_past_question(self):
        question = create_question(question_text="Pergunta passada", days=-30)
        create_question(question_text="Pergunta futura", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question]
        )

    def test_two_past_questions(self):
        question1 = create_question(question_text="Pergunta passada 1", days=-30)
        question2 = create_question(question_text="Pergunta passada 2", days=-5)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question2, question1],
        )

# Voltado para testar a função was_published_recently()
class QuestionModelTests(TestCase):
    def test_was_published_recently_with_old_question(self):
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)
    def test_was_published_recently_with_recent_question(self):
        time = timezone.now() - datetime.timedelta(days=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), False)
    def test_was_published_recently_with_future_question(self):
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)
