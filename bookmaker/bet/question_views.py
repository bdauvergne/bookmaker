from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from . import models
from . import question_forms
from . import views

class QuestionViewMixin(object):
    form_class = question_forms.QuestionForm
    pk_url_kwarg = 'question_pk'
    model = models.Question
    success_url = '/'

class QuestionCreateView(QuestionViewMixin, CreateView):
    def get_object(self):
        return models.Question(user=self.request.user)

question_create = QuestionCreateView.as_view()

class QuestionUpdateView(QuestionViewMixin, views.UserObjectsMixin,
        UpdateView):
    pass


question_edit = QuestionUpdateView.as_view()

def question_list(request):
    pass

class QuestionDeleteView(QuestionViewMixin, views.UserObjectsMixin, DeleteView):
    model = models.Question

question_delete = QuestionDeleteView.as_view()

class QuestionPublishView(QuestionViewMixin, views.ActionView):
    action_method_name = 'publish'

question_publish = QuestionPublishView.as_view()

class QuestionOpenView(QuestionViewMixin, views.ActionView):
    action_method_name = 'open'

question_open = QuestionOpenView.as_view()
