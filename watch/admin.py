from django.contrib import admin
from .models import User, Item, Watchlist


class ItemAdmin(admin.ModelAdmin):
	list_display = ('title', 'status', 'price', 'datetime')
	list_editable = ('status','price')

class WatchlistAdmin(admin.ModelAdmin):
	list_display = ('user', 'items', 'watched')
	list_editable = ('watched',)

admin.site.register(User)
admin.site.register(Item, ItemAdmin)
admin.site.register(Watchlist, WatchlistAdmin)