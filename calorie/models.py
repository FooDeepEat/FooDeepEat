from django.db import models
from user.models import Account


class Food(models.Model):
    name = models.CharField(max_length=20, null=True, blank=True, default=None)
    weight = models.IntegerField(null=True, blank=True, default=None)
    energy = models.IntegerField(null=True, blank=True, default=None)
    carbohydrate = models.IntegerField(null=True, blank=True, default=None)
    protein = models.IntegerField(null=True, blank=True, default=None)
    fat = models.IntegerField(null=True, blank=True, default=None)

    def __str__(self):
        return f"음식:{self.name} 탄수화물:{self.carbohydrate} 단백질:{self.protein} 지방:{self.fat}"


class FoodImage(models.Model):
    name = models.ForeignKey(Food, on_delete=models.CASCADE, related_name='images')
    food_img = models.ImageField(null=True, blank=True, default=None, upload_to="food/")

    def __str__(self):
        return f"음식:{self.name} 이미지:{self.food_img}"


class UserFood(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='users')
    name = models.ForeignKey(Food, on_delete=models.CASCADE, related_name='foods')
    weight = models.IntegerField(null=True, blank=True, default=None)
    carbohydrate = models.IntegerField(null=True, blank=True, default=None)
    protein = models.IntegerField(null=True, blank=True, default=None)
    fat = models.IntegerField(null=True, blank=True, default=None)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"유저:{self.user} 음식:{self.name} 탄수화물:{self.carbohydrate} 단백질:{self.protein} 지방:{self.fat} 날짜:{self.date}"


class UserMemo(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='memos')
    description = models.TextField(blank=True, null=True)
    date = models.DateField()

    class Meta:
        unique_together = ('user', 'date')

    def __str__(self):
        return f"유저:{self.user.username} 메모:{self.description} 날짜:{self.date}"
