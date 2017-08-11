from django import forms

from lan_complain.models import Answer, Question


class QuestionForm(forms.ModelForm):

    hostel = forms.ChoiceField(choices=Question.HOSTEL_CHOICES,widget=forms.Select(attrs={'class':'selector'}))

    description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control'}),
        max_length=2000)
    tags = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=255,
        required=False,
        help_text='Use spaces to separate the tags, such as "asp.net mvc5 javascript"')  # noqa: E501

    class Meta:
        model = Question
        fields = ['hostel', 'description', 'tags']


class AnswerForm(forms.ModelForm):
    question = forms.ModelChoiceField(widget=forms.HiddenInput(),
                                      queryset=Question.objects.all())
    description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '4'}),
        max_length=2000)

    class Meta:
        model = Answer
        fields = ['question', 'description']
