from .models import Category

def store(request):
  return {
    "categories": Category.objects.prefetch_related("parent").all(),
  }