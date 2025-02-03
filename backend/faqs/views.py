from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.core.cache import cache
from .models import FAQ


@api_view(['GET'])
def get_faqs(request):
    lang = request.GET.get('lang', 'en')
    cache_key = f'faqs_{lang}'
    cached_data = cache.get(cache_key)

    if cached_data:
        return Response(cached_data)

    faqs = FAQ.objects.all()
    data = []
    for faq in faqs:
        data.append({
            "question": faq.get_translated_question(lang),
            "answer": faq.answer
        })

    cache.set(cache_key, data, timeout=86400)  # Cache for 1 day
    return Response(data)
