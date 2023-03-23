from django.db import models
from user.models import Account


class Food(models.Model):
    name = models.CharField(max_length=20, null=True, blank=True, default=None)
    weight = models.FloatField(null=True, blank=True, default=None)
    energy = models.FloatField(null=True, blank=True, default=None)
    carbohydrate = models.FloatField(null=True, blank=True, default=None)
    protein = models.FloatField(null=True, blank=True, default=None)
    fat = models.FloatField(null=True, blank=True, default=None)
    sugar = models.FloatField(null=True, blank=True, default=None)
    cholesterol = models.FloatField(null=True, blank=True, default=None)
    calcium = models.FloatField(null=True, blank=True, default=None)
    phosphorus = models.FloatField(null=True, blank=True, default=None)
    sodium = models.FloatField(null=True, blank=True, default=None)
    potassium = models.FloatField(null=True, blank=True, default=None)
    magnesium = models.FloatField(null=True, blank=True, default=None)
    iron = models.FloatField(null=True, blank=True, default=None)
    zinc = models.FloatField(null=True, blank=True, default=None)
    trans_fat = models.FloatField(null=True, blank=True, default=None)
    created_at = models.DateField(auto_now_add=True)


    def __str__(self):
        return f"{self.name}"


class FoodImage(models.Model):
    name = models.ForeignKey(Food, on_delete=models.CASCADE, related_name='images')
    food_img = models.ImageField(null=True, blank=True, default=None, upload_to="food/")
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} {self.food_img} {self.created_at}"


class UserFood(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='user_foods')
    name = models.ForeignKey(Food, on_delete=models.CASCADE, related_name='user_foods')
    weight = models.FloatField(null=True, blank=True, default=None)
    carbohydrate = models.FloatField(null=True, blank=True, default=None)
    protein = models.FloatField(null=True, blank=True, default=None)
    fat = models.FloatField(null=True, blank=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} {self.name}"


class UserFoodImage(models.Model):
    name = models.ForeignKey(UserFood, on_delete=models.CASCADE, related_name='user_food_images')
    food_img = models.ImageField(null=True, blank=True, default=None, upload_to="user_food/")
    created_at = models.DateTimeField(auto_now_add=True)


class UserMemo(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='user_memos')
    description = models.TextField(blank=True, null=True)
    created_at = models.DateField()

    class Meta:
        unique_together = ('user', 'created_at')

    def __str__(self):
        return f"{self.user.username} {self.description} {self.created_at}"
