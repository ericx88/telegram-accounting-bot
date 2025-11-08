# 使用Python官方镜像
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV PYTHONUNBUFFERED=1

# 复制依赖文件
COPY requirements.txt .

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY bot.py .

# 创建数据目录
RUN mkdir -p /tmp

# 启动命令
CMD ["python", "bot.py"]