from django.contrib import admin
from .models import FAQ
from ckeditor.widgets import CKEditorWidget
from django import forms


class FAQAdminForm(forms.ModelForm):
    class Meta:
        model = FAQ
        fields = '__all__'
        widgets = {
            'answer': CKEditorWidget(),
        }


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    form = FAQAdminForm
    list_display = ('question', 'get_translated_question')
    search_fields = ('question', 'answer')

    def get_translated_question(self, obj):
        return obj.get_translated_question('hi')  # Example for Hindi
    get_translated_question.short_description = 'Translated Question (Hindi)'
