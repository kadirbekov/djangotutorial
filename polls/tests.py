import datetime

from django.test import TestCase
# Create your tests here.
from django.urls import reverse
from django.utils import timezone

from polls.models import Question


class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        time = timezone.now() + datetime.timedelta(days=30)
        self.assertFalse(Question(pub_date=time).was_published_recently());

    def test_was_published_recently__when_2_days_ago(self):
        time = timezone.now() - datetime.timedelta(days=2)
        self.assertFalse(Question(pub_date=time).was_published_recently());

    def test_was_published_recently__when_recent(self):
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)


def create_question(text, days):
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=text, pub_date=time)


class QuestionIndexViewTests(TestCase):

    def test_no_question(self):
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(200, response.status_code)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        create_question("text", -20)
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(200, response.status_code)
        self.assertQuerysetEqual(response.context['latest_question_list'], ['<Question: text>'])

    def test_future_question(self):
        create_question("future question", 10)
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(200, response.status_code)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_and_past_questions(self):
        create_question("past", -20)
        create_question("future", 1)
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(200, response.status_code)
        self.assertQuerysetEqual(response.context['latest_question_list'], ['<Question: past>'])

    def test_two_past_questions(self):
        create_question("past 1", -20)
        create_question("past 2", -10)
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(200, response.status_code)
        self.assertQuerysetEqual(response.context['latest_question_list'], ['<Question: past 2>', '<Question: past 1>'])


class QuestionDetailViewTests(TestCase):

    def test_future_question(self):
        question = create_question("future", 10)
        url = reverse('polls:detail', args=(question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        question = create_question("past", -2)
        url = reverse('polls:detail', args=(question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, question.question_text)