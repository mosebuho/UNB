from django import forms
from .models import Military


class MilitaryModelForm(forms.ModelForm):
    class Meta:
        model = Military
        fields = ["category", "title", "content"]
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "제목을 입력해주세요."}),
        }
