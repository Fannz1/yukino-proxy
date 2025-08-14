import os
import requests
from flask import Flask, request, jsonify

# --- Инициализация Flask-приложения ---
app = Flask(__name__)

# --- Получаем API-ключ из переменных окружения для безопасности ---
# Мы не будем хранить ключ прямо в коде. Мы настроим его на хостинге.
GEMINI_API_KEY = os.environ.get("AIzaSyA4JphmE3gGY2EeHeocFc4PQNEmmUPpsWA")

# --- Главный и единственный маршрут нашего API ---
@app.route('/generate', methods=['POST'])
def generate():
    # Проверяем, был ли передан API-ключ при запуске сервера
    if not GEMINI_API_KEY:
        return jsonify({"error": "GEMINI_API_KEY не настроен на сервере"}), 500

    # Получаем данные, которые прислал наш Telegram-бот
    data = request.json
    if not data or 'payload' not in data:
        return jsonify({"error": "Неверный формат запроса. Ожидается 'payload'."}), 400

    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={GEMINI_API_KEY}"
    
    try:
        # Напрямую отправляем запрос в Google. Прокси не нужны, т.к. сервер в США.
        response = requests.post(api_url, json=data['payload'], timeout=40)
        
        # Возвращаем ответ от Google (успешный или с ошибкой) как есть нашему боту
        return jsonify(response.json()), response.status_code

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Ошибка при подключении к API Gemini: {e}"}), 503

# Эта часть нужна для локального тестирования, на хостинге она не используется
if __name__ == '__main__':
    # Для запуска на хостинге будет использоваться gunicorn
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
