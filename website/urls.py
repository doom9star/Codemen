from django.urls import path
from .views import (
    IndexView, HomeView, SignupView, LoginView, LogoutView, 
    CreateQuestionView, DetailQuestionView, DeleteQuestionView, 
    UpdateQuestionView, QuestionAnswerView, QuestionAnswerEditView, 
    QuestionAnswerReplyView, QuestionAnswerDeleteView, GetMoreQuestions,
    QuestionAnswerVote, EditProfileImageView)

urlpatterns = [
    path('', IndexView.as_view(), name="index"),
    path('home/', HomeView.as_view(), name="home"),
    path('signup/', SignupView.as_view(), name="signup"),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('create-question/', CreateQuestionView.as_view(), name="create-question"),
    path('detail-question/<int:pk>/<str:order>', DetailQuestionView.as_view(), name="detail-question"),
    path('delete-question/<int:pk>', DeleteQuestionView.as_view(), name="delete-question"),
    path('update-question/<int:pk>', UpdateQuestionView.as_view(), name="update-question"),
    path('answer-question/<int:pk>', QuestionAnswerView.as_view(), name="answer-question"),
    path('answer-question-delete/<int:pk>', QuestionAnswerDeleteView.as_view(), name="answer-delete"),
    path('answer-question-edit/<int:pk>', QuestionAnswerEditView.as_view(), name="answer-question-edit"),
    path('answer-question-reply/<int:qid>/<int:aid>', QuestionAnswerReplyView.as_view(), name="answer-question-reply"),
    path('answer-question-vote/<int:aid>/<str:voteType>', QuestionAnswerVote.as_view(), name="answer-question-vote"),
    # path('assign-badge/<int:qid>/<int:aid>/<int:btype>', AssignBadgeView.as_view(), name="assign-badge"),

    # Data Views
    path('get-more-questions/<int:cursor>', GetMoreQuestions.as_view(), name="get-more-questions"),
    path('edit-profile-image', EditProfileImageView.as_view(), name="edit-profile-image"),
]