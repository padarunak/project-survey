from django.urls import include, path

from .views import account, moderators, respondents

urlpatterns = [
    path('', account.home, name='home'),

    path('respondents/', include(([
        path('', respondents.QuizListView.as_view(), name='quiz_list'),
        path('category/', respondents.RespondentCategoryView.as_view(), name='category_respondents'),
        path('taken/', respondents.TakenQuizListView.as_view(), name='taken_quiz_list'),
        path('quiz/<int:pk>/', respondents.take_quiz, name='take_quiz'),
    ], 'account'), namespace='respondents')),

    path('moderators/', include(([
        path('', moderators.QuizListView.as_view(), name='quiz_change_list'),
        path('quiz/add/', moderators.QuizCreateView.as_view(), name='quiz_add'),
        path('quiz/<int:pk>/', moderators.QuizUpdateView.as_view(), name='quiz_change'),
        path('quiz/<int:pk>/delete/', moderators.QuizDeleteView.as_view(), name='quiz_delete'),
        path('quiz/<int:pk>/results/', moderators.QuizResultsView.as_view(), name='quiz_results'),
        path('quiz/<int:pk>/question/add/', moderators.question_add, name='question_add'),
        path('quiz/<int:quiz_pk>/question/<int:question_pk>/', moderators.question_change, name='question_change'),
        path('quiz/<int:quiz_pk>/question/<int:question_pk>/delete/', moderators.QuestionDeleteView.as_view(), name='question_delete'),
    ], 'account'), namespace='moderators')),
]
