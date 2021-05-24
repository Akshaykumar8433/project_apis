from flask import Flask, g
from flask_restx import Api
from flask_jwt_extended import JWTManager
import time, decimal, datetime, json

app = Flask(__name__)

authorizations = {
    'access_token': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'AUTHORIZATION'
        },
}
api = Api(
    app,
    version="1.0",
    title = "IMDB Apis",
    description = "Through this apis you can insert new,fetch, update and delete the movies according to the authentication wirtes",
    security=["access_token"],
    authorizations=authorizations
)


app.config["JWT_SECRET_KEY"] = "imdb_key"
app.config["JWT_ACCESS_TOKEN_EXPERIES"] = False
jwt = JWTManager(app)

def myconverter(o):
    if isinstance(o, datetime.datetime) or isinstance(o,datetime.date):
        return o.__str__()
    elif isinstance(o,decimal.Decimal):
        return float(o)

@app.before_request
def before_request():
    g.start_time = time.time()
    g.response = {}

@app.after_request
def after_request(res):
    try:
        if ((res.get_data()).decode("utf-8") == "null\n"):
            res.set_data(json.dumps(g.response,default=myconverter))
        return res
    except Exception as e:
        return res