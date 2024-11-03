from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.html import escape
from django.utils.safestring import mark_safe

from django.utils import timezone


class User(AbstractUser):
    is_moderator = models.BooleanField(default=False)
    is_respondent = models.BooleanField(default=False)


class Subject(models.Model):
    name = models.CharField('Название категории', max_length=30)
    color = models.CharField(max_length=7, default='#007bff')

    def __str__(self):
        return self.name

    def get_html_badge(self):
        name = escape(self.name)
        color = escape(self.color)
        html = f'<span class="badge badge-primary" style="background-color: {color}">{name}</span>'
        return mark_safe(html)


class Quiz(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quizzes')
    name = models.CharField('Название опроса', max_length=255)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='quizzes')

    start_date = models.DateField('Дата начала опроса', default=timezone.now)
    end_date = models.DateField('Дата окончания вопроса', default=timezone.now)
    is_active = models.BooleanField('Статус опроса', default=True)

    def __str__(self):
        return self.name


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.CharField('Вопросы', max_length=255)

    def __str__(self):
        return self.text


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.CharField('Ответы', max_length=255)
    is_correct = models.BooleanField('Правильны ответ', default=False)

    def __str__(self):
        return self.text


class Respondent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    quizzes = models.ManyToManyField(Quiz, through='TakenQuiz')
    category = models.ManyToManyField(Subject, related_name='category_respondents')

    def get_unanswered_questions(self, quiz):
        answered_questions = self.quiz_answers \
            .filter(answer__question__quiz=quiz) \
            .values_list('answer__question__pk', flat=True)
        questions = quiz.questions.exclude(pk__in=answered_questions).order_by('text')
        return questions

    def __str__(self):
        return self.user.username


class TakenQuiz(models.Model):
    respondent = models.ForeignKey(Respondent, on_delete=models.CASCADE, related_name='taken_quizzes')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='taken_quizzes')
    score = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)


class RespondentAnswer(models.Model):
    respondent = models.ForeignKey(Respondent, on_delete=models.CASCADE, related_name='quiz_answers')
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='+')
