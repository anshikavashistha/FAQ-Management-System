from django.db import models
from ckeditor.fields import RichTextField
from django.core.cache import cache
from googletrans import Translator
from django.db.models.signals import post_save, post_delete  # Add this line
from django.dispatch import receiver  # Add this line

# List of supported languages
SUPPORTED_LANGUAGES = ['en', 'hi', 'bn']  # Add more languages as needed


class FAQ(models.Model):
    question = models.TextField()
    answer = RichTextField()

    # Dynamically add language fields
    for lang in SUPPORTED_LANGUAGES:
        if lang != 'en':  # Skip English since it's the default
            locals()[f'question_{lang}'] = models.TextField(
                null=True, blank=True)

    def save(self, *args, **kwargs):
        """Auto-translate and save translations"""
        translator = Translator()
        for lang in SUPPORTED_LANGUAGES:
            if lang != 'en' and not getattr(self, f'question_{lang}'):
                try:
                    translation = translator.translate(
                        self.question, dest=lang)
                    translated_text = translation.text
                    setattr(self, f'question_{lang}', translated_text)
                except Exception:
                    # Fallback to English if translation fails
                    setattr(self, f'question_{lang}', self.question)

        cache.set(f'faq_{self.id}', self, timeout=86400)  # Cache for 1 day
        super().save(*args, **kwargs)

    def get_translated_question(self, lang='en'):
        """Fetch translated question based on language"""
        if lang == 'en' or not hasattr(self, f'question_{lang}'):
            return self.question
        return getattr(self, f'question_{lang}', self.question)

    def __str__(self):
        return self.question


# Add the signal handlers at the bottom of the file
@receiver(post_save, sender=FAQ)
@receiver(post_delete, sender=FAQ)
def invalidate_faq_cache(sender, instance, **kwargs):
    for lang in SUPPORTED_LANGUAGES:
        cache.delete(f'faqs_{lang}')
    cache.delete(f'faq_{instance.id}')
