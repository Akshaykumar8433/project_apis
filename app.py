from swagger_config import app
from dbconnect import init_db
# from api_test_cases import ApiTest

#routes import
import routes.movies
import routes.auth


if __name__ == '__main__':
    init_db()
    app.run(debug=True,port=5001)
    # ApiTest()
    