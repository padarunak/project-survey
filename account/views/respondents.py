from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView
from django.views.decorators.csrf import csrf_protect

from ..decorators import respondent_required
from ..forms import RespondentCategoryForm, RespondentSignUpForm, TakeQuizForm
from ..models import Quiz, Respondent, TakenQuiz, User


class RespondentSignUpView(CreateView):
    model = User
    form_class = RespondentSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'respondent'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('respondents:quiz_list')


@method_decorator([login_required, respondent_required], name='dispatch')
class RespondentCategoryView(UpdateView):
    model = Respondent
    form_class = RespondentCategoryForm
    template_name = 'account/respondents/interests_form.html'
    success_url = reverse_lazy('respondents:quiz_list')

    def get_object(self):
        return self.request.user.respondent

    def form_valid(self, form):
        messages.success(self.request, 'Категория успешно обновлена!')
        return super().form_valid(form)


@method_decorator([login_required, respondent_required], name='dispatch')
class QuizListView(ListView):
    model = Quiz
    ordering = ('name', )
    context_object_name = 'quizzes'
    template_name = 'account/respondents/quiz_list.html'

    def get_queryset(self):
        respondent = self.request.user.respondent
        respondent_category = respondent.category.values_list('pk', flat=True)
        taken_quizzes = respondent.quizzes.values_list('pk', flat=True)
        queryset = Quiz.objects.filter(subject__in=respondent_category) \
            .exclude(pk__in=taken_quizzes) \
            .annotate(questions_count=Count('questions')) \
            .filter(questions_count__gt=0)
        return queryset


@method_decorator([login_required, respondent_required], name='dispatch')
class TakenQuizListView(ListView):
    model = TakenQuiz
    context_object_name = 'taken_quizzes'
    template_name = 'account/respondents/taken_quiz_list.html'

    def get_queryset(self):
        queryset = self.request.user.respondent.taken_quizzes \
            .select_related('quiz', 'quiz__subject') \
            .order_by('quiz__name')
        return queryset


@login_required
@respondent_required
def take_quiz(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    respondent = request.user.respondent

    if respondent.quizzes.filter(pk=pk).exists():
        return render(request, 'respondents/taken_quiz.html')

    total_questions = quiz.questions.count()
    unanswered_questions = respondent.get_unanswered_questions(quiz)
    total_unanswered_questions = unanswered_questions.count()
    progress = 100 - round(((total_unanswered_questions - 1) / total_questions) * 100)
    question = unanswered_questions.first()

    if request.method == 'POST':
        form = TakeQuizForm(question=question, data=request.POST)
        if form.is_valid():
            with transaction.atomic():
                respondent_answer = form.save(commit=False)
                respondent_answer.respondent = respondent
                respondent_answer.save()
                if respondent.get_unanswered_questions(quiz).exists():
                    return redirect('respondents:take_quiz', pk)
                else:
                    correct_answers = respondent.quiz_answers.filter(answer__question__quiz=quiz, answer__is_correct=True).count()
                    score = round((correct_answers / total_questions) * 100.0, 2)
                    TakenQuiz.objects.create(respondent=respondent, quiz=quiz, score=score)
                    if score < 50.0:
                        messages.warning(request, f'Удачи в следующий раз! Ваш результат за тест {quiz.name} составил {score}.')
                    else:
                        messages.success(request, f'Поздравляем! Вы успешно прошли тест {quiz.name}! Вы набрали {score} очков.')
                    return redirect('respondents:quiz_list')
    else:
        form = TakeQuizForm(question=question)

    return render(request, 'account/respondents/take_quiz_form.html', {
        'quiz': quiz,
        'question': question,
        'form': form,
        'progress': progress
    })
