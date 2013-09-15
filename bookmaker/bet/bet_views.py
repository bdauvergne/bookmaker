from django.views.generic.edit import DeleteView, UpdateView
from django.http import Http404

from . import models
from . import outcome_forms
from . import views


def bet_list(request):
    pass

class BetEditView(views.UserObjectsMixin, UpdateView):
    pk_url_kwarg = 'bet_pk'
    model = models.Bet
    form_class = outcome_forms.BetForm

bet_edit = BetEditView.as_view()

class BetDeleteView(DeleteView):
    model = models.Bet
    success_url = '/'
    pk_url_kwarg = 'bet_pk'

bet_delete = BetDeleteView.as_view()
