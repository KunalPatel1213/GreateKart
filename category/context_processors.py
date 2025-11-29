from .models import Category

def menu_links(request):
    links = Category.objects.all()   # ✅ assign queryset to links
    return dict(links=links)         # ✅ return dictionary