from django.test import TestCase
from django.urls import reverse
from .models import Expense, Category
from datetime import date

class ExpenseListViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.category1 = Category.objects.create(name='Category 1')
        cls.category2 = Category.objects.create(name='Category 2')
        
        cls.expense1 = Expense.objects.create(name='Expense 1', amount=10, date=date(2024, 1, 1), category=cls.category1)
        cls.expense2 = Expense.objects.create(name='Expense 2', amount=20, date=date(2024, 2, 1), category=cls.category2)
        cls.expense3 = Expense.objects.create(name='Expense 3', amount=30, date=date(2024, 3, 1), category=cls.category1)

    def test_filter_expenses_by_date_from(self):
        response = self.client.get(reverse('expenses:expense-list'), {'date_from': '2024-02-01'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Expense 2')
        self.assertContains(response, 'Expense 3')
        self.assertNotContains(response, 'Expense 1')

    def test_filter_expenses_by_date_to(self):
        response = self.client.get(reverse('expenses:expense-list'), {'date_to': '2024-02-01'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Expense 1')
        self.assertContains(response, 'Expense 2')
        self.assertNotContains(response, 'Expense 3')

    def test_filter_expenses_by_date_range(self):
        response = self.client.get(reverse('expenses:expense-list'), {'date_from': '2024-01-15', 'date_to': '2024-02-15'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Expense 2')
        self.assertNotContains(response, 'Expense 1')
        self.assertNotContains(response, 'Expense 3')

    def test_filter_expenses_by_name(self):
        response = self.client.get(reverse('expenses:expense-list'), {'name': 'Expense 1'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Expense 1')
        self.assertNotContains(response, 'Expense 2')
        self.assertNotContains(response, 'Expense 3')

    def test_filter_expenses_by_name_and_date(self):
        response = self.client.get(reverse('expenses:expense-list'), {'name': 'Expense', 'date_from': '2024-01-01', 'date_to': '2024-02-01'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Expense 1')
        self.assertContains(response, 'Expense 2')
        self.assertNotContains(response, 'Expense 3')

    def test_filter_expenses_by_multiple_categories(self):
        response = self.client.get(reverse('expenses:expense-list'), {'categories': [self.category1.id, self.category2.id]})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Expense 1')
        self.assertContains(response, 'Expense 2')
        self.assertContains(response, 'Expense 3')

    def test_filter_expenses_by_multiple_categories(self):
        response = self.client.get(reverse('expenses:expense-list'), {'categories': [self.category1.id, self.category2.id]})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Expense 1')
        self.assertContains(response, 'Expense 2')
        self.assertContains(response, 'Expense 3')