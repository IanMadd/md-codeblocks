# Configuration Examples

This file contains various configuration examples.

## Docker Configuration

Here's a Dockerfile:

```
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "app.py"]
```

## YAML Configuration

Some YAML configuration:

```
version: '3.8'
services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DEBUG=1
    volumes:
      - .:/app
```

## Regular Text

This is just regular markdown text that should not be affected.

No code blocks here, just normal paragraphs and text.

## SQL Example

A database query:

```
SELECT 
    u.id,
    u.name,
    u.email,
    COUNT(o.id) as order_count
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE u.active = 1
GROUP BY u.id, u.name, u.email
ORDER BY order_count DESC;
```

That's all for this file.