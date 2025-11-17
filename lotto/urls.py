from django.urls import path
from django.contrib import admin
from .views import home
from . import views

urlpatterns = [
    path("", views.index, name="index"),

    # 메인 화면
    path('', home, name='home'),

    # 사용자
    path("buy/", views.buy, name="buy"),
    path("buy/success/<int:purchase_id>/", views.buy_success, name="buy_success"),
    path("my-results/", views.my_results, name="my_results"),

    # 관리자(관리자 페이지와 충돌 방지 -> lotto-admin 사용)
    path("lotto-admin/draw/", views.admin_draw, name="admin_draw"),
    path("lotto-admin/draw/list/", views.admin_draw_list, name="admin_draw_list"),
    path("lotto-admin/winners/<int:draw_number>/", views.admin_winners, name="admin_winners"),
    path("lotto-admin/sales/", views.admin_sales, name="admin_sales"),
]
