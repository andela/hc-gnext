from django import forms
from django.template.defaultfilters import slugify
from .models import Category, Post


class CategoryForm(forms.ModelForm):
    """
    Create form from Category model.
    """

    class Meta:
        model = Category
        fields = ('name',)

    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)

        for field_name, field_obj in self.fields.items():
            if field_name == 'name':
                field_obj.widget.attrs.update({'class': 'form-control'})
                field_obj.widget.attrs.update({'placeholder': 'Post Category'})

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


class PostForm(forms.ModelForm):
    """
    Create form from Post model.
    """

    class Meta:
        model = Post
        fields = ('title', 'categories', 'content')

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')

        super(PostForm, self).__init__(*args, **kwargs)

        place_holders = {
            'title': 'Post Title',
            'categories': 'Choose Post Category',
            'content': 'Post Content'}

        for field_name, field_obj in self.fields.items():
            if field_name == 'categories':
                pass  # do nothing

            else:
                field_obj.widget.attrs.update({'class': 'form-control'})
                field_obj.widget.attrs.update({'placeholder': place_holders.get(field_name, '')})

    def save(self, commit=True):
        obj = super(PostForm, self).save(commit=False)
        obj.slug = slugify(self.cleaned_data.get('title', ''))
        obj.created_by = self.request.user
        obj.save()
        obj.categories = self.cleaned_data.get('categories', '')
        obj.save()
        return obj
