from django.views.generic.edit import UpdateView
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404

from . import models
from . import outcome_forms

class QuestionMixin(object):
    def dispatch(self, request, *args, **kwargs):
        self.question = get_object_or_404(models.Question, pk=kwargs['question_pk'])
        return super(QuestionMixin, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super(QuestionMixin, self).get_context_data(**kwargs)
        ctx['question'] = self.question
        return ctx

class OutcomeMixin(object):
    def dispatch(self, request, *args, **kwargs):
        self.outcome = get_object_or_404(models.Outcome,
                question=self.question,
                pk=kwargs['outcome_pk'])
        return super(OutcomeMixin, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super(OutcomeMixin, self).get_context_data(**kwargs)
        ctx['outcome'] = self.outcome
        return ctx

class OutcomeCreateView(QuestionMixin, UpdateView):
    model = models.Outcome
    success_url = '/'
    form_class = outcome_forms.OutcomeCreateForm

    def get_object(self):
        return models.Outcome(question=self.question, user=self.request.user)

outcome_create = OutcomeCreateView.as_view()

def outcome_delete(request):
    pass

def outcome_edit(request):
    pass

class OutcomeBetView(QuestionMixin, OutcomeMixin, UpdateView):
    model = models.Bet
    success_url = '/'
    form_class = outcome_forms.BetForm


    def get_object(self):
        try:
            return models.Bet.objects.get(user=self.request.user,
                    outcome=self.outcome)
        except models.Bet.DoesNotExist:
            return models.Bet(user=self.request.user, outcome=self.outcome)

outcome_bet = OutcomeBetView.as_view()
