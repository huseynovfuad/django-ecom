from django import forms
from .models import Product, Category
from .validators import name_validator


class ProductForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    # name2 = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))

    class Meta:
        model = Product
        exclude = ("user", )

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control", "data-id": "intiqam"})
            self.fields[field].required = True

        self.fields["description"].widget.attrs.update({
            "cols": "100", "rows": "6", "placeholder": "Message"
        })

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if name == "Fuad":
            raise forms.ValidationError("Bu ad olmaz")
        return name

    # def clean(self):
    #     cleaned_data = self.cleaned_data
    #     name = cleaned_data.get("name")
    #     print(name, "Formun umumi cleani")
    #     # if name == "Fuad":
    #     #     raise forms.ValidationError({"Bu ad olmaz"})
    #
    #     price = cleaned_data.get("price")
    #     tax = cleaned_data.get("tax")
    #     discount = cleaned_data.get("discount")
    #     total_price = price + tax - discount
    #     if total_price < 100:
    #         raise forms.ValidationError({"Total Qiymet 100den asagi ola bilmez"})
    #     return cleaned_data


    # def save(self):
    #     cleaned_data = self.cleaned_data
    #     sizes = cleaned_data.pop("sizes")
    #     product = Product.objects.create(
    #         **cleaned_data
    #     )
    #     product.sizes.set(sizes)
    #     return product


# class ProductForm(forms.Form):
#     name = forms.CharField()
#     content = forms.CharField(widget=forms.Textarea())
#     category = forms.ModelChoiceField(queryset=Category.objects.all())