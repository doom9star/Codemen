from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    image = models.ImageField(upload_to="profile", blank=True, null=True)


class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.title)

    def get_answers(self):
        return Answer.objects.filter(question=self)


class Image(models.Model):
    image = models.TextField()
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.TextField()
    answerer = models.ForeignKey(User, on_delete=models.CASCADE)
    upvoters = models.ManyToManyField(User, related_name="upvoters")
    downvoters = models.ManyToManyField(User, related_name="downvoters")
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created",)

    def __str__(self):
        return str(self.answer)


class Reply(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    replier = models.ForeignKey(User, on_delete=models.CASCADE)
    reply = models.TextField()

    def __str__(self):
        return self.reply
