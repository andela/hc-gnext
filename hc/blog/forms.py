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

    def clean_name(self):
        """
        Check if category with the same name exists to avoid duplication.
        """

        name = self.cleaned_data.get('name', '')
        exists = Category.objects.filter(name=name)
        if exists:
            raise forms.ValidationError('')

        return name

    def save(self, commit=True):
        """
        Override default save method in order to create slug value.

        """
        obj = super(CategoryForm, self).save(commit=False)
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

        if 'create' in kwargs:
            self.create = kwargs.pop('create', False)

        if 'update' in kwargs:
            self.update = kwargs.pop('update', False)

        super(PostForm, self).__init__(*args, **kwargs)

        place_holders = {
            'title': 'Post Title',
            'categories': 'Choose Post Category',
            'content': 'Post Content'}

        for field_name, field_obj in self.fields.items():
            if field_name == 'categories':
                pass

            else:
                field_obj.widget.attrs.update({'class': 'form-control'})
                field_obj.widget.attrs.update({'placeholder': place_holders.get(field_name, '')})

    def clean_title(self):
        """
        Check if post with the same title exists to avoid duplication.
        """

        title = self.cleaned_data.get('title', '')

        if hasattr(self, 'create') and self.create:
            exists = Post.objects.filter(title=title)
            if exists:
                msg = 'There exists a post with that title, choose a different title'
                raise forms.ValidationError(msg)

        return title

    def save(self, commit=True):
        obj = super(PostForm, self).save(commit=False)
        obj.slug = slugify(self.cleaned_data.get('title', ''))
        obj.created_by = self.request.user
        obj.save()
        obj.categories = self.cleaned_data.get('categories', '')
        obj.save()
        return obj
