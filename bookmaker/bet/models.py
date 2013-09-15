import decimal

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _

import model_utils.fields
import model_utils

# Create your models here.
class Question(models.Model):
    STATUS = model_utils.Choices(
            ('unpublished', _('unpublished')),
            ('published', _('published')),
            ('open', _('open')),
            ('finished', _('finished')),
    )

    description = models.TextField(verbose_name=_('bet description'))
    user = models.ForeignKey('auth.User', verbose_name=_('user'))
    created = models.DateTimeField(auto_now_add=True,
            verbose_name=_('created'))
    status = model_utils.fields.StatusField(verbose_name=_('status'))

    @property
    def amount(self):
        qs = models.Bet.objects.filter(outcome__question=self)
        return qs.aggregate(models.Sum('amount'))['amount__sum']

    def clean(self):
        if self.status in (Question.STATUS.finished, Question.STATUS.open):
            raise ValidationError(_('you cannot modify an open or finished question'))

    def publish(self):
        assert self.status == Question.STATUS.unpublished
        self.status = Question.STATUS.published
        self.save()

    def open(self):
        assert self.status == Question.STATUS.published
        self.status = Question.STATUS.open
        self.save()

    @property
    def editable(self):
        return self.status not in (Question.STATUS.open,
                Question.STATUS.finished)

    def __unicode__(self):
        return self.description

    class Meta:
        verbose_name = _('question')
        ordering = ('-created',)

class Outcome(models.Model):
    STATUS = model_utils.Choices(
            ('unknown', _('unknown')),
            ('lost', _('lost')),
            ('win', _('win')),
    )
    question = models.ForeignKey('Question', verbose_name=_('question'))
    description = models.TextField(verbose_name=_('description'))
    user = models.ForeignKey('auth.User', verbose_name=_('user'))
    created = models.DateTimeField(auto_now_add=True,
            verbose_name=_('created'))
    status = model_utils.fields.StatusField()

    def clean(self):
        if self.question.status == Question.STATUS.finished:
            raise ValidationError(_('you cannot add or modify outcome on finished question'))
        if self.status == Outcome.STATUS.lost:
            raise ValidationError(_('you cannot set a lost outcome, only a win'))
        if self.bet_set.exists():
            raise ValidationError(_('This outcome has already bets, you cannot modify it'))

    @property
    def amount(self):
        return self.bet_set.aggregate(models.Sum('amount'))['amount__sum']

    @property
    def odd(self):
        amount = self.amount
        qs = self.question.outcome_set.exclude(pk=self.pk)
        qs = qs.annotate(computed_amount=models.Sum('bet__amount'))
        other_amounts = sum(outcome.computed_amount for outcome in qs)
        return other_amounts / amount

    @property
    def odd_display(self):
        odd = self.odd
        tpl = _('%s vs 1')
        if odd < 1:
            odd = 1 / odd
            tpl =_('1 vs %s')
        return tpl % odd.quantize(exp=decimal.Decimal('0.1'))


    def win(self):
        assert self.status == Outcome.STATUS.unknown
        self.status = Outcome.STATUS.win
        self.status.save()
        qs = self.question.outcome_set.exclude(pk=self.pk)
        qs.update(status=Bet.STATUS.lost)
        self.question.status = Question.STATUS.closed
        self.question.save()

    class Meta:
        verbose_name = _('outcome')
        ordering = ('created',)


    def __unicode__(self):
        return self.description

class Bet(models.Model):
    outcome = models.ForeignKey('Outcome')
    amount = models.DecimalField(verbose_name=_('amount'),
            decimal_places=2, max_digits=6)
    created = models.DateTimeField(auto_now_add=True,
        verbose_name=_('creation date'))
    modified = models.DateTimeField(auto_now=True,
            verbose_name=_('modification date'))
    user = models.ForeignKey('auth.User', verbose_name=_('user'))

    class Meta:
        verbose_name = _('bet')
        ordering = ('-modified',)
        unique_together = ('user', 'outcome')

    def clean(self):
        if self.outcome.question.status == Question.STATUS.finished:
            raise ValidationError(_('you cannot bet on finished questions'))

    def clean_amount(self):
        if self.amount <= 0:
            raise models.ValidationError(_('amount must be positive'))

    @property
    def gain(self):
        return self.amount * self.outcome.odd

    def __unicode__(self):
        return u'%s %s' % (self.amount, self.user)
