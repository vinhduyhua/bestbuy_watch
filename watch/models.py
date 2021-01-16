from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
	pass

class Item(models.Model):
	title = models.TextField()
	status = models.TextField()
	price = models.TextField()
	link = models.TextField(blank=True)
	datetime = models.DateTimeField(auto_now_add=True, blank=True)

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.__price = self.price

	def save(self, *args, **kwargs):
		if self.price and not self.__price:
			self.datetime.now()
		super().save(*args, **kwargs)

	def __str__(self):
		return f"{self.title} | {self.status} | {self.price} | {self.datetime}"

	def serialize(self):
		return {
			"id": self.id,
			"title": self.title,
			"status": self.status,
			"price": self.price,
			"link": self.link,
			"datetime": self.datetime.strftime("%b %d %Y, %I:%M %p"),
		}

class Watchlist(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_watchlist")
	items = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="items_watchlist")
	watched = models.BooleanField(default=True)

	def serialize(self):
		return {
			"id": self.id,
			"item_id": self.items.id,
			"username" : self.user.username,
			"title": self.items.title,
			"status": self.items.status,
			"price": self.items.price,
			"link": self.items.link,
			"datetime": self.items.datetime.strftime("%b %d %Y, %I:%M %p"),
		}

	def __str__(self):
		return f"{self.user.username} | {self.items.title}"