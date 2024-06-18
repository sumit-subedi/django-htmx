from django import forms
from .models import Task, Remainder

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['date', 'time', 'task']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
            'task': forms.TextInput(attrs={'maxlength': 100}),
        }

class RemainderForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['added'].widget = forms.HiddenInput()
        self.fields['added'].required = True
        self.fields['set_time'].required = True
        self.fields['text'].required = True
        self.fields['mail'].required = True
        
  
    class Meta:
        model = Remainder
        fields = ['added', 'set_time', 'text', 'mail']
        labels = {
            'set_time': 'Remainder Time',
            'text': 'Remainder',
        }
        widgets = {
            'added': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'set_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'text': forms.Textarea(attrs={'rows': 3}),
            'mail': forms.EmailInput(),
        }
