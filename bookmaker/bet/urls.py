from django.conf.urls import patterns, include, url

outcome_patterns = patterns('bookmaker.bet.outcome_views',
        url(r'^create/$', 'outcome_create',
            name='outcome-create'),
        url(r'^(?P<outcome_pk>\d+)/$', 'outcome_edit',
            name='outcome-edit'),
        url(r'^(?P<outcome_pk>\d+)/delete/$', 'outcome_delete',
            name='outcome-delete'),
        url(r'^(?P<outcome_pk>\d+)/bet/$', 'outcome_bet',
            name='outcome-bet'),
)

question_patterns = patterns('bookmaker.bet.question_views',
        url(r'^$', 'question_list', name='question-list'),
        url(r'^create/$', 'question_create', name='question-create'),
        url(r'^(?P<question_pk>\d+)/$', 'question_edit',
            name='question-edit'),
        url(r'^(?P<question_pk>\d+)/publish/$', 'question_publish',
            name='question-publish'),
        url(r'^(?P<question_pk>\d+)/delete/$', 'question_delete',
            name='question-delete'),
        url(r'^(?P<question_pk>\d+)/open/$', 'question_open',
            name='question-open'),
        (r'^(?P<question_pk>\d+)/outcome/', include(outcome_patterns)),
)

bet_patterns = patterns('bookmaker.bet.bet_views',
        url(r'^$', 'bet_list', name='bet-list'),
        url(r'^(?P<bet_pk>\d+)/$', 'bet_edit', name='bet-edit'),
        url(r'^(?P<bet_pk>\d+)/delete/$', 'bet_delete', name='bet-delete'),
)

urlpatterns = patterns('bookmaker.bet.views',
    # Examples:
    url(r'^$', 'homepage', name='homepage'),
    (r'^question/', include(question_patterns)),
    (r'^bet/', include(bet_patterns)),
)
