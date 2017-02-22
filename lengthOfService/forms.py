from django import forms


class UploadSeedFileForm(forms.Form):
    file = forms.FileField(
        widget=forms.FileInput(attrs={'rows': 30, 'cols': 100, 'placeholder': 'Drop your .csv file here'}),
        label='CSV File Upload')


class GenerateSeedFileForm(forms.Form):
    start_date = forms.DateField()
    end_date = forms.DateField()
    no_of_records = forms.IntegerField()