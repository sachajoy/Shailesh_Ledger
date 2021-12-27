from django import forms
from django.forms.models import ModelForm
from . import models


class ClientForm(ModelForm):
    class Meta:
        model = models.Client
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, val in self.fields.items():
            self.fields[key].widget.attrs.update(
                {'class': 'form-control form-control-user'}
            )

class FirmForm(ModelForm):
    class Meta:
        model = models.Firm
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, val in self.fields.items():
            self.fields[key].widget.attrs.update(
                {'class': 'form-control form-control-user'}
            )


class DateInput(forms.DateInput):
    input_type = 'date'


class TrancationForm(ModelForm):
    remarks = forms.CharField(required=False)

    class Meta:
        model = models.Trancation
        fields = ('booking_date', 'passenger_list',
                  'date', 'remarks', 'sector',
                  'amount', 'firm')
        widgets = {
            'date': forms.TextInput(
                attrs={'placeholder': 'Date', 'required': 'False'}),
            'remarks': forms.TextInput(
                attrs={'placeholder': 'Remarks', 'required': 'false'}),
            'sector': forms.TextInput(attrs={'placeholder': 'Sector'}),
            'amount': forms.NumberInput(attrs={'placeholder': 'Amount'}),
            'booking_date': DateInput(),
            'passenger_list': forms.TextInput(
                attrs={'placeholder': 'Passenger List'}),
            'firm': forms.Select(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, val in self.fields.items():
            self.fields[key].widget.attrs.update(
                {'class': 'form-control form-control-user'}
            )


class FromToForm(forms.Form):
    from_date = forms.DateField(widget=DateInput())
    to_date = forms.DateField(widget=DateInput())
    # test = forms.CharField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, val in self.fields.items():
            self.fields[key].widget.attrs.update(
                {'class': 'form-control form-control-user'}
            )


class DateSelectorForm(ModelForm):

    class Meta:
        model = models.DateSelector
        fields = ('start_date', 'end_date')
        widgets = {
            'start_date': DateInput(),
            'end_date': DateInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, val in self.fields.items():
            self.fields[key].widget.attrs.update(
                {'class': 'form-control form-control-user'}
            )


