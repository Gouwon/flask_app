# from flask_server import app
# from flaskr import app

# app.run(host='0.0.0.0')  # 127.0.0.1 == localhost

from flaskr import create_app

app = create_app()
app.run(host='0.0.0.0')
