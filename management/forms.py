from django import forms
from .models import Batch, Deaths, Expenses, Revenue, Customers,UserProfile, ExpenseGroup
from django.utils.translation import gettext_lazy as _
from django.contrib.admin.widgets import AdminDateWidget
class BatchForm(forms.ModelForm):
  class Meta:
    model=Batch
    exclude=['user', 'picture']
    labels = {
            'farm': _('Animal being kept'),
            'purchased': _('Units purchased'),
            'projected_SP': _('Projected Selling Price'),
        }
    widgets= {
      'end_date': AdminDateWidget()

    }


class DeathsForm(forms.ModelForm):
  class Meta:
    model=Deaths
    exclude=['batch']
    labels = {
            'number': _('Number dead'),
        }

class ExpensesForm(forms.ModelForm):
  class Meta:
    model=Expenses
    exclude=['batch']


    labels = {
            'group': _('Expense Category'),
            'amount': _('Amount Spent'),
        }
    help_texts = {
            'group': _('e.g. Food, Health, Utilities, etc'),
            'details': _('e.g. 1kg Isinya starter mash, animal parafin, 1kg makaa etc'),
        }
class ExpenseGroupForm(forms.ModelForm):
  class Meta:
    model=ExpenseGroup
    exclude=['batch']
    labels = {
            'group': _('Expense Category'),
        }
    help_texts = {
            'group': _('e.g. Food, Health, Utilities, etc'),
        }
class RevenueForm(forms.ModelForm):
  class Meta:
    model=Revenue
    exclude=['batch']
    Widgets = { 'customer' : forms.CheckboxSelectMultiple() ,}
    labels = {
            'number': _('Units Sold'),
            'customer': _('Customer sold to'),
        }


class CustomersForm(forms.ModelForm):
  class Meta:
    model=Customers
    fields = ('name', 'number')
    labels = {
            'number': _('Phone Number'),
            'name': _('Customers Name'),
        }


class UserProfileForm(forms.ModelForm):
  class Meta:
    model = UserProfile
    exclude = ['editor']

