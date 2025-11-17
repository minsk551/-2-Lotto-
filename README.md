1. 프로젝트 다운로드
- 방법 A) GitHub에서 클론
- 방법 B) ZIP 다운로드


2. 프로젝트 디렉토리로 이동
- cd 2-Lotto--master


3. docker-compose로 빌드 및 실행
docker-compose up --build


4. Django 초기 설정
- docker exec -it lotto_web_32220623 bash
  (docker ps로 확인 가능)
- python manage.py migrate
- python manage.py createsuperuser


5. 웹사이트 접속 주소
- http://localhost:8000


6. 서비스 기능 요약

수동/자동 로또 구매
회차별 추첨 (관리자)
당첨 결과 확인
회차별 판매 실적 (관리자)
 

