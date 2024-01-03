from django import forms
from .models import EventModel

class EventForm(forms.Form):
    name = forms.CharField(max_length=50)
    description = forms.CharField(max_length=2000)
    time = forms.DateTimeField(widget = forms.TextInput(attrs={'type': 'time'}))
    address =forms.CharField(max_length=1000)
    topic = forms.CharField(max_length=50)
    image = forms.ImageField()
    
    def save(self):
        EventModel.objects.create(
            name = self.cleaned_data['name'],
            description = self.cleaned_data['description'],
            address = self.cleaned_data['address'],
            time = self.cleaned_data['time'],
            topic = self.cleaned_data['topic'],
            image = self.cleaned_data['image'],
        )
class EventFormModel(forms.ModelForm):
    time = forms.TimeField(widget=forms.TextInput(attrs={'type': 'time'}))
    date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))
    deadlinedate = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))
    deadlinetime = forms.TimeField(widget=forms.TextInput(attrs={'type': 'time'}))
    
    class Meta():
        model = EventModel
        fields = '__all__'
        widgets = {'user':forms.HiddenInput()}
