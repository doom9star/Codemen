from django.shortcuts import render, redirect
from .models import Question, Answer, Reply
from django.contrib.auth import login, logout, authenticate
from .forms import SignUpForm, LoginForm, QuestionForm
from django.views.generic import (
    TemplateView,
    ListView,
    CreateView,
    View,
    DeleteView,
    DetailView,
    UpdateView,
)
from django.urls import reverse
from django.http import JsonResponse
from django.db.models import Q
import json
from .mixins import RedirectIfLoggedInMixin, RedirectIfNotLoggedInMixin
from django.core.serializers import serialize
from django.contrib.auth import get_user_model
from django.db.models import Count
from django.contrib import messages
import time

User = get_user_model()


class IndexView(RedirectIfLoggedInMixin, TemplateView):
    template_name = "website/index_page.html"

    def get(self, req):
        if self.request.user.is_authenticated:
            return redirect("home")
        return render(req, self.template_name)


class HomeView(ListView):
    template_name = "website/home_page.html"
    model = Question
    context_object_name = "questions"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context["my_questions"] = Question.objects.filter(user=self.request.user)[
                :5
            ]
            context["other_questions"] = Question.objects.filter(
                ~Q(user=self.request.user)
            )
            context["more_questions"] = len(context["other_questions"]) > 5
            context["other_questions"] = context["other_questions"][:5]
        else:
            context["questions"] = Question.objects.all()
            context["more_questions"] = context["questions"].count() > 5
            context["questions"] = context["questions"][:5]
        return context


class GetMoreQuestions(View):
    def get(self, req, cursor):
        responseData = {}
        if req.user.is_authenticated:
            temp_lst = Question.objects.filter(~Q(user=req.user))[cursor:]
        else:
            temp_lst = Question.objects.all()[cursor:]
        responseData["more_questions"] = len(temp_lst) > 5
        responseData["questions"] = serialize("json", temp_lst[:5])
        return JsonResponse(responseData, safe=False)


class SignupView(RedirectIfLoggedInMixin, CreateView):
    template_name = "website/signup_page.html"
    form_class = SignUpForm

    def form_valid(self, form):
        response = super().form_valid(form)
        user = authenticate(
            username=form.cleaned_data.get("username"),
            password=form.cleaned_data.get("password1"),
        )
        login(self.request, user)
        return response

    def get_success_url(self):
        return reverse("home")


class LoginView(RedirectIfLoggedInMixin, View):
    def get(self, req):
        return render(req, "website/login_page.html", {"form": LoginForm()})

    def post(self, req):
        form = LoginForm(req.POST or None)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data.get("username"),
                password=form.cleaned_data.get("password"),
            )
            if user:
                login(req, user)
                return redirect("home")
        messages.error(req, "Username/Password might be wrong, Try again!")
        return render(req, "website/login_page.html", {"form": form})


class LogoutView(RedirectIfNotLoggedInMixin, View):
    def get(self, req):
        logout(req)
        return redirect("index")


class CreateQuestionView(RedirectIfNotLoggedInMixin, View):
    def get(self, *args, **kwargs):
        qForm = QuestionForm()
        return render(self.request, "website/create-question.html", {"qForm": qForm})

    def post(self, *args, **kwargs):
        q = Question(
            user=self.request.user,
            title=self.request.POST.get("title"),
            description=self.request.POST.get("description"),
        )
        q.save()
        return JsonResponse(None, safe=False)


class DetailQuestionView(DetailView):
    model = Question
    template_name = "website/detail-question.html"
    context_object_name = "question"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        answers = Question.objects.get(pk=self.kwargs["pk"]).get_answers()
        order = self.kwargs["order"]
        if order == "upvotes":
            answers = answers.annotate(upvotes=Count("upvoters")).order_by("-upvotes")
        elif order == "popular":
            answers = answers.annotate(
                totalvotes=Count("upvoters") + Count("downvoters")
            ).order_by("-totalvotes")
        for answer in answers:
            answer.vote_status = -1
            if answer.upvoters.filter(username=self.request.user.username).exists():
                answer.vote_status = 1
            elif answer.downvoters.filter(username=self.request.user.username).exists():
                answer.vote_status = 0
            answer.replies = Reply.objects.filter(answer=answer)
        context["answers"] = answers
        return context


class DeleteQuestionView(RedirectIfNotLoggedInMixin, DeleteView):
    model = Question
    template_name = "website/delete-question-confirm.html"
    context_object_name = "question"

    def get_success_url(self):
        return reverse("home")


class UpdateQuestionView(RedirectIfNotLoggedInMixin, UpdateView):
    model = Question
    fields = ["title", "description"]
    template_name = "website/update-question.html"

    def post(self, request, pk, *args, **kwargs):
        question = self.get_object()
        question.title = self.request.POST.get("title")
        question.description = self.request.POST.get("description")
        question.save()
        return JsonResponse(None, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["question"] = self.get_object()
        return context


class QuestionAnswerView(RedirectIfNotLoggedInMixin, View):
    def post(self, req, pk):
        Answer.objects.create(
            question=Question.objects.get(pk=pk),
            answer=req.POST.get("answer"),
            answerer=req.user,
        ).save()
        return redirect(reverse("detail-question", args=[pk, "recent"]))


class QuestionAnswerEditView(RedirectIfNotLoggedInMixin, UpdateView):
    model = Answer
    fields = ["answer"]
    template_name = "website/answer-edit.html"

    def get_success_url(self):
        return reverse(
            "detail-question", args=[self.get_object().question.id, "recent"]
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["question"] = self.get_object().question
        return context


class QuestionAnswerReplyView(RedirectIfNotLoggedInMixin, View):
    def post(self, req, qid, aid):
        reply = Reply.objects.create(
            answer=Answer.objects.get(pk=aid),
            replier=req.user,
            reply=req.POST.get("reply"),
        )
        reply.save()
        return redirect(reverse("detail-question", args=[qid, "recent"]))


class QuestionAnswerDeleteView(RedirectIfNotLoggedInMixin, View):
    def get(self, req, pk):
        answer = Answer.objects.get(pk=pk)
        qid = answer.question.id
        answer.delete()
        return redirect(reverse("detail-question", args=[qid, "recent"]))


class QuestionAnswerVote(RedirectIfNotLoggedInMixin, View):
    def post(self, _, aid, voteType):
        answer = Answer.objects.get(pk=aid)
        if voteType == "UPVOTE":
            if not answer.upvoters.filter(username=self.request.user.username).exists():
                answer.downvoters.remove(self.request.user)
                answer.upvoters.add(self.request.user)
        else:
            if not answer.downvoters.filter(
                username=self.request.user.username
            ).exists():
                answer.upvoters.remove(self.request.user)
                answer.downvoters.add(self.request.user)
        answer.save()
        return JsonResponse(None, safe=False)


class EditProfileImageView(RedirectIfNotLoggedInMixin, View):
    def post(self, req):
        image = json.loads(req.body.decode("utf-8"))["image"]
        user = User.objects.get(username=req.user.username)
        user.image = image
        user.save()
        return JsonResponse(None, safe=False)


# class AssignBadgeView(RedirectIfNotLoggedInMixin, View):
#     def post(self, req, qid, aid, btype):
#         q = Question.objects.get(pk=qid)
#         a = Answer.objects.get(pk=aid)
#         if btype == 1:
#             q.golden_answer = a
#         elif btype == 2:
#             q.silver_answer = a
#         elif btype == 3:
#             q.bronze_answer = a

#         q.save()
#         return JsonResponse(None, safe=False)
