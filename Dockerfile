# 使用Python 3.11官方镜像作为基础镜像
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件（如果有requirements.txt的话先复制）
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# 安装Python依赖
RUN pip install --no-cache-dir aiogram

# 复制应用代码
COPY bot.py .
COPY groups.json .
COPY ledger.json .

# 创建非root用户
RUN useradd --create-home --shell /bin/bash appuser && \
    chown -R appuser:appuser /app
USER appuser

# 暴露端口（如果需要的话，Telegram Bot通常不需要）
# EXPOSE 8000

# 启动命令
CMD ["python", "bot.py"]