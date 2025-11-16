import random
import uuid
from .models import LottoPurchase, LottoDraw, Winner


# 1) 자동 번호 생성
def generate_auto_numbers():
    numbers = sorted(random.sample(range(1, 46), 6))
    return numbers


# 2) 번호 저장 공통 함수
def save_purchase(user, numbers, draw_number):
    numbers_str = ",".join(map(str, numbers))
    
    purchase = LottoPurchase.objects.create(
        user=user,                   # user_name → user 객체
        numbers=numbers_str,
        draw_number=draw_number,
        unique_code=uuid.uuid4().hex[:8].upper()
    )
    return purchase


# 3) 수동 구매
def manual_purchase(user, number_list, draw_number):
    number_list = list(map(int, number_list))
    number_list.sort()
    return save_purchase(user, number_list, draw_number)


# 4) 자동 구매
def auto_purchase(user, draw_number):
    auto_nums = generate_auto_numbers()
    return save_purchase(user, auto_nums, draw_number)


# 5) 회차 추첨 로직 (변경 없음)
def draw_lotto(draw_number):
    winning_numbers = sorted(random.sample(range(1, 46), 6))
    bonus = random.choice([n for n in range(1, 46) if n not in winning_numbers])
    
    draw = LottoDraw.objects.create(
        draw_number=draw_number,
        winning_numbers=",".join(map(str, winning_numbers)),
        bonus_number=bonus,
    )
    
    return draw


# 6) 당첨 확인 로직 (user_name → user.username 변경)
def check_winners(draw_number):
    draw = LottoDraw.objects.get(draw_number=draw_number)
    
    winning_nums = list(map(int, draw.winning_numbers.split(",")))
    bonus = draw.bonus_number
    
    purchases = LottoPurchase.objects.filter(draw_number=draw_number)
    
    result = []

    for p in purchases:
        nums = list(map(int, p.numbers.split(",")))
        
        match = len(set(nums) & set(winning_nums))
        bonus_match = bonus in nums
        
        # 등수 판정
        if match == 6:
            rank = 1
            prize = 2000000000
        elif match == 5 and bonus_match:
            rank = 2
            prize = 50000000
        elif match == 5:
            rank = 3
            prize = 1500000
        elif match == 4:
            rank = 4
            prize = 50000
        elif match == 3:
            rank = 5
            prize = 5000
        else:
            rank = None
            prize = 0
        
        # Winner 저장
        if rank:
            Winner.objects.create(
                purchase=p,
                rank=rank,
                prize_amount=prize
            )

        result.append({
            "user": p.user.username,        
            "numbers": nums,
            "match": match,
            "bonus": bonus_match,
            "rank": rank,
            "prize": prize,
            "unique_code": p.unique_code,
            "draw_number": p.draw_number,
        })

    return result
