from django import forms

from accounts.models import User
from .models import Warehouse


class WarehouseForm(forms.ModelForm):
    class Meta:
        model = Warehouse
        fields = ["name", "city", "manager"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Warehouse name"}),
            "city": forms.TextInput(attrs={"class": "form-control", "placeholder": "City"}),
            "manager": forms.Select(attrs={"class": "form-select"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter managers to only users with role == 2 (Warehouse Manager)
        self.fields['manager'].queryset = User.objects.filter(role=2).order_by('username')
