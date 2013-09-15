# Create your views here.

from django.views.generic import TemplateView
from django.views.generic.detail import (BaseDetailView,
        SingleObjectTemplateResponseMixin)
from django.db.models import query
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

from . import models

class UserObjectsMixin(object):
    def get_queryset(self):
        qs = super(UserObjectsMixin, self).get_queryset()
        qs = qs.filter(user=self.request.user)
        return qs

class Homepage(TemplateView):
    template_name = 'bet/homepage.html'

    def get_context_data(self, **kwargs):
        ctx = super(Homepage, self).get_context_data(**kwargs)
        ctx['questions'] = models.Question.objects.filter(
                query.Q(status=models.Question.STATUS.open) |
                query.Q(user=self.request.user))[:20]
        ctx['bets'] = models.Bet.objects.filter(user=self.request.user)
        return ctx

homepage = login_required(Homepage.as_view())

class ActionMixin(object):
    """
    A mixin providing the ability to delete objects
    """
    success_url = None
    action_method_name = None

    def act(self, request, *args, **kwargs):
        """
        Calls the delete() method on the fetched object and then
        redirects to the success URL.
        """
        self.object = self.get_object()
        success_url = self.get_success_url()
        if self.action_method_name:
            getattr(self.object, self.action_method_name)()
        else:
            raise ImproperlyConfigured(
                "No action to do. Provide a action_method_name.")
        return redirect(success_url)

    # Add support for browsers which only accept GET and POST for now.
    def post(self, request, *args, **kwargs):
        return self.act(request, *args, **kwargs)

    def get_success_url(self):
        if self.success_url:
            return self.success_url % self.object.__dict__
        else:
            raise ImproperlyConfigured(
                "No URL to redirect to. Provide a success_url.")

    @property
    def template_name_suffix(self):
        return '_%s' % self.action_method_name

class ActionView(ActionMixin, SingleObjectTemplateResponseMixin, BaseDetailView):
    pass
