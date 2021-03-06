from django.contrib import admin
from bookmarkz_app.models import Tag, Bookmark, Link

class BookmarkAdmin(admin.ModelAdmin):
	list_display = ('title', 'link', 'user')
	list_filter = ('user',)
	ordering = ('title',)
	search_fields = ('title', )

admin.site.register(Link)
admin.site.register(Tag)
admin.site.register(Bookmark, BookmarkAdmin)