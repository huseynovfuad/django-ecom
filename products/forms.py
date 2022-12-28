from django import forms
from .models import Product, Category


class ProductForm(forms.ModelForm):
    # category = forms.RadioSelect(widget=forms.CheckboxInput())

    class Meta:
        model = Product
        exclude = ("user", )

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        print(self.fields)
        for field in self.fields:
            # self.fields[field].widget.attrs.update({"class": "form-control"})
            self.fields[field].required = True

        self.fields["description"].widget.attrs.update({
            "cols": "40", "rows": "4", "placeholder": "Message"
        })