from django import forms
from Users.models import BaseUser
from .models import Review


class AddMoneyForm(forms.ModelForm):
    class Meta:
        model = BaseUser
        fields = ["balance"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["balance"].label = "Amount to Add"


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["rating", "audit"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["audit"].label = "Leave Your Review"
