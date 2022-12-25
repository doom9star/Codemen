from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from .models import Image, Question
from django.core.exceptions import ObjectDoesNotExist, ValidationError

User = get_user_model()

class SignUpForm(UserCreationForm):
	class Meta:
		model = User
		fields = ('username', 'password1', 'password2')

class LoginForm(forms.Form):
	username = forms.CharField(max_length=30)
	password = forms.CharField(min_length=8, max_length=20, widget=forms.PasswordInput())

	def is_valid(self):
		valid = super(LoginForm, self).is_valid()
		if not valid: return valid
		user = None
		try:
			user = User.objects.get(username=self.cleaned_data.get('username'))
		except ObjectDoesNotExist:
			pass
		if user:
			if not check_password(self.cleaned_data.get('password'), user.password):
				return False
		else: return False
		return True

class QuestionForm(forms.ModelForm):
	class Meta:
		model = Question
		fields = ('title', 'description')