1. 프로젝트 다운로드
- 방법 A) GitHub에서 클론
- 방법 B) ZIP 다운로드




2. 프로젝트 디렉토리로 이동
- cd 2-Lotto--master




3. Docker 이미지 빌드
- docker build -t lotto_web_image .




4. docker-compose로 실행
- docker-compose up --build
- 접속 주소 -> http://localhost:8000




5. 관리자(Admin) 계정 정보
- 서버가 정상 실행되면 아래 관리자 계정으로 로그인 가능합니다:
> ID: RootManager
> Password: manager0515!!




6. 서비스 기능 요약

로또 구매 (수동/자동)

회차별 추첨 (관리자)

당첨 결과 확인

회차별 판매 실적 (관리자)
 

