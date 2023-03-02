from django import forms
from .models import Topic, Course, Material
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class MaterialForm(forms.Form):
    name = forms.CharField(max_length=255, label='Name', required=True)
    description = forms.CharField(label='Description', required=True)
    file = forms.FileField(label='File', required=True)
    course = forms.ModelChoiceField(queryset=Course.objects.all(), label='Course', required=False)
    topic = forms.ModelChoiceField(queryset=Topic.objects.all(), label='Topic', required=False)
    new_topic_name = forms.CharField(max_length=255, label='Tag a Topic', required=False)
    new_course_name = forms.CharField(max_length=255, label='New Course Name', required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['course'].empty_label = 'Select a course (optional)'
        self.fields['topic'].empty_label = 'Select a topic to tag(optional)'

    def clean(self):
        cleaned_data = super().clean()
        topic = cleaned_data.get('topic')
        new_topic_name = cleaned_data.get('new_topic_name')
        course = cleaned_data.get('course')
        new_course_name = cleaned_data.get('new_course_name')

        # Check that either a topic is selected or a new topic name is provided
        if not topic and not new_topic_name:
            raise forms.ValidationError('Either select a topic or enter a new topic name.')

        # Check that either a course is selected or a new course name is provided
        if not course and not new_course_name:
            raise forms.ValidationError('Either select a course or enter a new course name.')

        return cleaned_data

    def save(self):
        name = self.cleaned_data['name']
        file = self.cleaned_data['file']
        topic = self.cleaned_data['topic']
        description = self.cleaned_data['description']
        new_topic_name = self.cleaned_data['new_topic_name']
        course = self.cleaned_data['course']
        new_course_name = self.cleaned_data['new_course_name']

        if not topic:
            # If a new topic name is provided, create a new Topic object
            if new_topic_name:
                topic = Topic.objects.create(name=new_topic_name, course=course)
            else:
                raise forms.ValidationError('Either select a topic or enter a new topic name.')
        if not course:
            # If a new course name is provided, create a new Course object
            if new_course_name:
                course = Course.objects.create(name=new_course_name)
            else:
                raise forms.ValidationError('Either select a course or enter a new course name.')

        # Create a new Material object with the provided information
        material = Material.objects.create(name=name, file=file, course=course, topic=topic, description=description)
        return material


class MaterialUpdateForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance', None)
        super().__init__(*args, **kwargs)

        if instance:
            self.fields['topic'].initial = instance.topic
            self.fields['course'].initial = instance.course


class UserLoginForm(forms.Form):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password', 'id': 'password-field'}))


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email'}))
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'username'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password', 'id': 'password-field'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password', 'id': 'password-field'}))
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
