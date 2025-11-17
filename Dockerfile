FROM python:3.12-slim

# 기본 디렉토리
WORKDIR /app

# requirements 먼저 복사 후 설치
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# 전체 프로젝트 복사
COPY . .

# Gunicorn으로 Django 실행
CMD ["gunicorn", "lotto_site.wsgi:application", "--bind", "0.0.0.0:8000"]
