from django import forms
from .models import Expense, Category


class ExpenseSearchForm(forms.ModelForm):
    date_from = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    date_to = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))

    SORT_CHOICES = [
        ('category', 'Category (Ascending)'),
        ('-category', 'Category (Descending)'),
        ('date', 'Date (Ascending)'),
        ('-date', 'Date (Descending)'),
    ]

    sort_by = forms.ChoiceField(choices=SORT_CHOICES, required=False)

    class Meta:
        model = Expense
        fields = ('name', 'date_from', 'date_to', 'categories', 'sort_by')

    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].required = False
        self.fields['categories'].required = False
