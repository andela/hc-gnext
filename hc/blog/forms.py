from django import forms
from django.template.defaultfilters import slugify
from .models import Category


class CategoryForm(forms.ModelForm):
    """
    Create form from Category model.
    """

    class Meta:
        model = Category
        fields = ('name', )

    def save(self, commit=True):
        """
        Override default save method in order to create slug value.

        """
        obj = super(CategoryForm, self).save(commit=False)
        print(obj.name)
        slug = slugify(self.cleaned_data.get('name', ''))
        obj.slug = slug
        obj.save()
        return obj
