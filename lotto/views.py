from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.db.models import Count
from django.contrib import messages
from .models import LottoPurchase, LottoDraw, Winner

from .services import (
    auto_purchase, 
    manual_purchase, 
    draw_lotto, 
    check_winners
)
from .models import LottoPurchase, LottoDraw, Winner

def home(request):
    return render(request, "base.html")

# 홈페이지
def index(request):
    draws = LottoDraw.objects.order_by('-draw_number')
    return render(request, "index.html", {"draws": draws})


@login_required
def buy(request):
    latest = LottoDraw.objects.order_by('-draw_number').first()
    next_draw_number = latest.draw_number + 1 if latest else 1

    if request.method == "POST":
        user = request.user        # user_name 대신 로그인 유저
        mode = request.POST.get("mode")
        draw_number = next_draw_number

        # 자동 구매
        if mode == "auto":
            purchase = auto_purchase(user, draw_number)
            return redirect("buy_success", purchase_id=purchase.id)

        # 수동 구매
        numbers_raw = request.POST.get("numbers", "")
        try:
            if not numbers_raw.strip():
                messages.error(request, "수동 번호를 입력해주세요.")
                return render(request, "buy.html", {"next_draw_number": next_draw_number})

            nums = numbers_raw.replace(" ", "").split(",")

            if len(nums) != 6:
                messages.error(request, "숫자는 쉼표로 구분된 6개여야 합니다.")
                return render(request, "buy.html", {"next_draw_number": next_draw_number})

            nums_int = []
            for n in nums:
                val = int(n)
                if not (1 <= val <= 45):
                    messages.error(request, "각 숫자는 1~45 사이여야 합니다.")
                    return render(request, "buy.html", {"next_draw_number": next_draw_number})
                nums_int.append(val)

            if len(set(nums_int)) != 6:
                messages.error(request, "중복된 숫자가 있습니다.")
                return render(request, "buy.html", {"next_draw_number": next_draw_number})

            purchase = manual_purchase(user, nums_int, draw_number)
            return redirect("buy_success", purchase_id=purchase.id)

        except ValueError:
            messages.error(request, "숫자만 입력해야 합니다. 예: 1,5,10,22,33,40")
            return render(request, "buy.html", {"next_draw_number": next_draw_number})

    return render(request, "buy.html", {"next_draw_number": next_draw_number})



# 구매 성공 페이지
def buy_success(request, purchase_id):
    p = LottoPurchase.objects.get(id=purchase_id)
    return render(request, "buy_success.html", {"purchase": p})



# 관리자: 회차 추첨
@staff_member_required
def admin_draw(request):
    # 최신 회차 찾기
    latest = LottoDraw.objects.order_by('-draw_number').first()

    if latest:
        next_draw_number = latest.draw_number + 1
    else:
        next_draw_number = 1

    if request.method == "POST":
        draw = draw_lotto(next_draw_number)
        return redirect("admin_draw_list")

    return render(request, "admin_draw.html", {"next_draw_number": next_draw_number})



# 관리자: 추첨 리스트
@staff_member_required
def admin_draw_list(request):
    draws = LottoDraw.objects.order_by('-draw_number')
    return render(request, "admin_draw_list.html", {"draws": draws})


# 관리자: 당첨 확인
@staff_member_required
def admin_winners(request, draw_number):
    results = check_winners(draw_number)
    return render(request, "admin_winners.html", {"results": results})



def signup_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()        # Django가 자동으로 암호화해 저장
            login(request, user)      # 자동 로그인
            return redirect("home")   # 홈으로 이동 (또는 index)
    else:
        form = UserCreationForm()

    return render(request, "registration/signup.html", {"form": form})


@login_required
def my_results(request):
    user = request.user

    # 1. 사용자 구매 내역 전체 조회
    my_purchases = LottoPurchase.objects.filter(user=user).order_by("-draw_number")

    results = []

    for p in my_purchases:
        # 2. 해당 회차에 대해 추첨이 되었는지 확인
        draw = LottoDraw.objects.filter(draw_number=p.draw_number).first()

        # 3. 아직 추첨 안된 경우 → "대기중"
        if draw is None:
            results.append({
                "purchase": p,
                "status": "pending",  # 대기중
                "rank": None,
                "match": None,
                "bonus": None
            })
            continue

        # 4. 추첨된 경우 당첨 여부 계산
        winning = list(map(int, draw.winning_numbers.split(',')))
        bonus = draw.bonus_number
        nums = list(map(int, p.numbers.split(',')))

        match_count = len(set(nums) & set(winning))
        bonus_match = bonus in nums

        rank = None
        if match_count == 6:
            rank = 1
        elif match_count == 5 and bonus_match:
            rank = 2
        elif match_count == 5:
            rank = 3
        elif match_count == 4:
            rank = 4
        elif match_count == 3:
            rank = 5

        results.append({
            "purchase": p,
            "status": "done",   # 추첨 완료
            "rank": rank,
            "match": match_count,
            "bonus": bonus_match
        })

    return render(request, "my_results.html", {"results": results})

# 관리자: 실적 확인
@staff_member_required
def admin_sales(request):

    all_draws = LottoDraw.objects.order_by('-draw_number')
    sales_data = []

    for draw in all_draws:
        draw_no = draw.draw_number

        purchase_count = LottoPurchase.objects.filter(draw_number=draw_no).count()
        sales_amount = purchase_count * 5000

        winner_count = Winner.objects.filter(purchase__draw_number=draw_no).count()

        sales_data.append({
            "draw_number": draw_no,
            "purchase_count": purchase_count,
            "sales_amount": sales_amount,
            "winner_count": winner_count,
        })

    return render(request, "admin_sales.html", {"sales_data": sales_data})