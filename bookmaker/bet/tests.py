"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

import decimal

from django.test import TestCase
from django.contrib.auth.models import User

from . import models

class BetTests(TestCase):
    def setUp(self):
        self.john = User.objects.create(username='john.doe')
        self.babe = User.objects.create(username='babe.jensen')
        self.joe = User.objects.create(username='joe')
        self.question = models.Question.objects.create(
                description='what is the color of Henry 4th white horse ?',
                user=self.john)
        self.outcome_1 = models.Outcome.objects.create(question=self.question,
                description='white', user=self.john)
        self.outcome_2 = models.Outcome.objects.create(question=self.question, 
                description='Obi Wan Kenobi', user=self.babe)
        self.bet_1 = models.Bet.objects.create(outcome=self.outcome_1,
                amount='1', user=self.john)
        self.bet_2 = models.Bet.objects.create(outcome=self.outcome_2,
                amount='3', user=self.babe)
        self.bet_3 = models.Bet.objects.create(outcome=self.outcome_1,
                amount='0.5', user=self.joe)

    def test_amount(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(self.outcome_1.amount, decimal.Decimal('1.50'))
        self.assertEqual(self.outcome_2.amount, decimal.Decimal('3'))

    def test_odd(self):
        self.assertEqual(self.outcome_1.odd, decimal.Decimal('2'))
        self.assertEqual(self.outcome_2.odd, decimal.Decimal('0.5'))

    def test_bet_unicity(self):
        from django.db import IntegrityError
        from django.core.exceptions import ValidationError

        with self.assertRaises(IntegrityError):
            models.Bet.objects.create(outcome=self.outcome_1, amount=1, user=self.joe)

        bet = models.Bet(outcome=self.outcome_1, amount=1, user=self.joe)
        with self.assertRaises(ValidationError):
            bet.full_clean()

    def test_closed_question(self):
        from django.core.exceptions import ValidationError

        self.question.status = models.Question.STATUS.closed
        self.question.save()
        outcome = models.Outcome(question=self.question, 
                description='le colonel moutarde', user=self.joe)
        with self.assertRaises(ValidationError):
            outcome.full_clean()
        with self.assertRaises(ValidationError):
            self.bet_1.full_clean()
        bet = models.Bet(outcome=self.outcome_1, user=self.joe, amount=2)
        with self.assertRaises(ValidationError):
            bet.full_clean()

