from django.test import TestCase
from django.test import Client
from django.urls import reverse
from tasks.models import Task
import datetime
from datetime import date, timedelta
# Create your tests here.

class TaskTestcase(TestCase):
    def setUp(self):
        Task.objects.create(
            title="Test_task1"
        )
        next_date = date.today() + datetime.timedelta(days=10)
        Task.objects.create(
            title="Test_task2", date=next_date
        )
        self.client = Client()

    def test_default_date(self):
        task = Task.objects.get(title="Test_task1")
        self.assertEqual(date.today(), task.date)

    def test_task_count(self):
        task = Task.objects.all()
        self.assertEqual(2, task.count())

    def test_custom_date(self):
        next_date = date.today() + datetime.timedelta(days=10)
        task = Task.objects.get(title='Test_task2')
        self.assertEqual(next_date, task.date)

    def test_task_order(self):
        tasks = Task.objects.all().order_by('-date')
        self.assertEqual(tasks[0].title, "Test_task2")

    def test_view_home(self):
        response = self.client.get(reverse('homepage'))
        self.assertEqual(response.status_code, 200)

    def test_view_today_task(self):
        response = self.client.get(reverse('today_task'))
        self.assertEqual(response.status_code, 200)
