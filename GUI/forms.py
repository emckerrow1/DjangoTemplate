from django import forms
from django.contrib.auth.models import User

class ChangePasswordForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())
	password_repeat = forms.CharField(widget=forms.PasswordInput())
	class Meta:
		model = User
		fields = ("password", "password_repeat")
		exclude = ["username", "email","first_name","last_name"]

	def __init__(self, *args, **kwargs):
		super(ChangePasswordForm, self).__init__(*args, **kwargs)					
		for visible in self.visible_fields():
			visible.field.widget.attrs['class'] = 'form-control'

	def save(self, commit=True):
		user = super(ChangePasswordForm, self).save(commit=False)
		if commit:
			user.save()
		return user

	def clean(self):
		cleaned_data = self.cleaned_data
		new_password = cleaned_data.get("password")
		repeat_password = cleaned_data.get("password_repeat")
		if new_password:
			if len(new_password) < 8 or len(new_password) > 75:
				raise ValidationError('Passwords must be between 8 and 75 characters in length.')
		if new_password != repeat_password:
			raise ValidationError('Passwords do not match.')
		return self.cleaned_data