from django.db import models
from django.contrib.auth.models import User
import uuid


def generate_unique_code():
    return uuid.uuid4().hex[:12].upper()   # 12자리 고유값

# 로또 구매 DB
class LottoPurchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    numbers = models.CharField(max_length=20)
    draw_number = models.IntegerField(default=0)
    unique_code = models.CharField(max_length=12, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.unique_code:
            self.unique_code = generate_unique_code()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.numbers} ({self.draw_number}회차)"

# 로또 추첨 DB
class LottoDraw(models.Model):
    draw_number = models.IntegerField(unique=True)
    winning_numbers = models.CharField(max_length=20)
    bonus_number = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.draw_number}회차 추첨"

# 당첨자 DB
class Winner(models.Model):
    purchase = models.ForeignKey(LottoPurchase, on_delete=models.CASCADE)
    rank = models.IntegerField()  # 1~5등
    prize_amount = models.IntegerField()

    def __str__(self):
        return f"{self.purchase.user.username} - {self.rank}등"
