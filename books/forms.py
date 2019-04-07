from django import forms

from .models import Book, Page


class PageCreateForm(forms.Form):
    total_number = forms.IntegerField(required=True)
    comment = forms.CharField(widget=forms.Textarea, required=True)
    book_id = forms.IntegerField(required=True)

    def clean(self):
        book_id = self.data['book_id']
        total_number = int(self.data['total_number'])

        if total_number < 1:
            raise forms.ValidationError('Invalid page number')

        book = Book.objects.get(pk=book_id)
        if not book:
            raise forms.ValidationError('Invalid book id')

        page = Page.objects.filter(book_id=book_id).last()
        if not page:
            number = total_number
            page_total_number = 0
        else:
            number = total_number - page.total_number
            page_total_number = page.total_number

        if page_total_number >= total_number:
            raise forms.ValidationError('Invalid page number')
        if book.page_number < total_number:
            raise forms.ValidationError('Invalid page number')

        self.cleaned_data['number'] = number
        self.cleaned_data['book'] = book
        return super().clean()
