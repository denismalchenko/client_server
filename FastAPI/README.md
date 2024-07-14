# Ассинхронный клиент-сервер с кэшированием

## Предварительная настройка

1. Установка зависимостей

	* При необходимости, создайте окружение  
	`python3 -m venv venv`  
	`source venv/bin/activate`

	* Установите необходимые зависимости:  
	`python3 -m pip install -r requirements.txt`

## Запуск

1. Запустите сервер
	`python3 server.py`

2. В другом терминале запустите клиент со списком url. Например:  
	`python3  crawl.py ya.ru https://www.google.com https://www.wikipedia.org/404 https://www.example.com https://ya.ru`

3. Ещё раз запустите клиент с немного другим списком url. Например:  
	`python3  crawl.py https://www.google.com/search?q=there+is+no+spoon https://www.wikipedia.org/404 https://ya.ru nometa.xyz https://www.google.com "https://yandex.ru/search/?text=аasync+fastapi+favicon&clid=2574587&win=624&lr=65"`

4. Можно повторить несколько раз запуск одного и того же запроса, чтобы увидеть как испольняется запрос первый раз, повторный раз и после очистки кэша.

5. Остановите сервер `Ctrl-C`