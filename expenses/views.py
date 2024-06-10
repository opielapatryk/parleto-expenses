from django.views.generic.list import ListView
from django.db import models
from .forms import ExpenseSearchForm
from .models import Expense, Category
from .reports import summary_per_category


class ExpenseListView(ListView):
    model = Expense
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()

        form = ExpenseSearchForm(self.request.GET)
        if form.is_valid():
            name = form.cleaned_data.get('name', '').strip()
            date_from = form.cleaned_data.get('date_from')
            date_to = form.cleaned_data.get('date_to')
            categories = form.cleaned_data.get('categories')
            sort_by = form.cleaned_data.get('sort_by')

            if name:
                queryset = queryset.filter(name__icontains=name)
            if date_from:
                queryset = queryset.filter(date__gte=date_from)
            if date_to:
                queryset = queryset.filter(date__lte=date_to)
            if categories:
                queryset = queryset.filter(category__in=categories)
            if sort_by:
                queryset = queryset.order_by(sort_by)

        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = object_list if object_list is not None else self.object_list

        form = ExpenseSearchForm(self.request.GET)

        total_amount_spent = round(queryset.aggregate(total_amount_spent=models.Sum('amount'))['total_amount_spent'] or 0, 2)

        summary_per_year_month = queryset.annotate(
            year_month=models.functions.Concat(models.functions.ExtractYear('date'), models.Value('-'), models.functions.ExtractMonth('date'),output_field=models.CharField())
        ).values('year_month').annotate(
            total_amount=models.Sum('amount')
        ).order_by('year_month')

        return super().get_context_data(
            form=form,
            object_list=queryset,
            summary_per_category=summary_per_category(queryset),
            total_amount_spent=total_amount_spent,
            summary_per_year_month=summary_per_year_month,
            **kwargs)

class CategoryListView(ListView):
    model = Category
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()

        queryset = queryset.annotate(expense_count=models.Count('expense'))
        return queryset