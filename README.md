# Deslee Counter

to use:
gunicorn -b localhost:PORT app:app

configure nginx to proxy pass `/counter/` to localhost:PORT

route has to be `/counter/` unless you edit the code
