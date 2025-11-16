from django.contrib import admin
from .models import LottoPurchase, LottoDraw, Winner


@admin.register(LottoPurchase)
class LottoPurchaseAdmin(admin.ModelAdmin):
    list_display = ("user", "numbers", "draw_number", "created_at")
    list_filter = ("draw_number", "created_at")
    search_fields = ("user__username", "numbers")


@admin.register(LottoDraw)
class LottoDrawAdmin(admin.ModelAdmin):
    list_display = ("draw_number", "winning_numbers", "bonus_number", "created_at")
    search_fields = ("draw_number",)


@admin.register(Winner)
class WinnerAdmin(admin.ModelAdmin):
    list_display = ("purchase", "rank", "prize_amount")
    list_filter = ("rank",)
    search_fields = ("purchase__user__username",)
