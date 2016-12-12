from django.contrib import admin
from bookmarkz_app.models import Tag, Bookmark, Link

admin.site.register(Bookmark)
admin.site.register(Link)
admin.site.register(Tag)