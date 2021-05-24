import unittest,requests, json

class ApiTest(unittest.TestCase):
    API_URL = "http://127.0.0.1:5001"
    MOVIE_URL = "{}/movies/".format(API_URL)
    AUTH_URL = "{}/auth".format(API_URL)
    URL_HEADERS = {
        'Content-Type':'application/json'
    }
    NEW_MOVIE = {
        "movie_name": "Test New Movie",
        "imdb_score": 90.0,
        "popularity": 74.0,
        "director": "Unit Testing",
        "genre": ["Action","Comedie"]
    }
    INCOMPLETE_NEW_MOVIE = {
        "movie_name": "Test New Movie",
        "imdb_score": 90.0,
        "director": "Unit Testing",
        "genre": ["Action","Comedie"]
    }
    ACCESS_TOKEN = ""

    def test_1_signup(self):
        user_obj = {"email":"akshay.deekonda@gmail.com","password":"123456","role":"admin"}
        r = requests.post("{}/signup".format(ApiTest.AUTH_URL),json=user_obj)
        self.assertEqual(r.headers.get("Content-Type"), "application/json")
        self.assertEqual((r.json()).get("status"),200)
    
    def test_2_login(self):
        user_obj = {"email":"akshay.deekonda@gmail.com","password":"123456"}
        r = requests.post("{}/login".format(ApiTest.AUTH_URL),json=user_obj)
        ApiTest.URL_HEADERS["Authorization"] = "Bearer {}".format((r.json())["data"].get("access_token"))
        self.assertEqual(r.headers.get("Content-Type"), "application/json")
        self.assertEqual((r.json()).get("status"),200)

    def test_3_get_movie_list(self):
        params = {"type":"genre","query":"Horror,Action"}
        r = requests.get(ApiTest.MOVIE_URL,headers=ApiTest.URL_HEADERS,params=params)
        self.assertEqual(r.headers.get("Content-Type"), "application/json")
        self.assertEqual((r.json()).get("status"),200)
    
    def test_4_create_new_movie(self):
        r = requests.post(ApiTest.MOVIE_URL,headers=ApiTest.URL_HEADERS,json=ApiTest.NEW_MOVIE)
        ApiTest.NEW_MOVIE["id"] = (r.json())["data"].get("id")
        self.assertEqual(r.headers.get("Content-Type"), "application/json")
        self.assertEqual((r.json()).get("status"),200)
    
    @unittest.expectedFailure
    def test_5_create_new_movie_with_incomplete_data(self):
        r = requests.post(ApiTest.MOVIE_URL,headers=ApiTest.URL_HEADERS,json=ApiTest.INCOMPLETE_NEW_MOVIE)
        self.assertEqual(r.headers.get("Content-Type"), "application/json")
        self.assertEqual((r.json()).get("status"),200)

    def test_6_update_movie_details(self):
        r = requests.put(ApiTest.MOVIE_URL,headers=ApiTest.URL_HEADERS,json=ApiTest.NEW_MOVIE)
        self.assertEqual(r.headers.get("Content-Type"), "application/json")
        self.assertEqual((r.json()).get("status"),200)
    
    def test_7_delete_movie_details(self):
        r = requests.delete(ApiTest.MOVIE_URL,headers=ApiTest.URL_HEADERS,json={"id":ApiTest.NEW_MOVIE.get("id")})
        self.assertEqual(r.headers.get("Content-Type"), "application/json")
        self.assertEqual((r.json()).get("status"),200)

    def test_8_delete_user(self):
        r = requests.delete("{}/deleteuser".format(ApiTest.AUTH_URL),headers=ApiTest.URL_HEADERS,json={"email":"akshay.deekonda@gmail.com"})
        self.assertEqual(r.headers.get("Content-Type"), "application/json")
        self.assertEqual((r.json()).get("status"),200)

if __name__ == "__main__":
    unittest.main()
