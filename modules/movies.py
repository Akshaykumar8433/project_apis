from sqlalchemy import Column,BigInteger,String,Float,Text
from dbconnect import Base
from dataclasses import dataclass
import json

@dataclass
class Movies(Base):
    __tablename__ = 'movies'
    id: int
    movie_name: str
    imdb_score: str
    genre: str
    director: str
    popularity: str

    id = Column(BigInteger,primary_key=True,autoincrement=True)
    movie_name = Column(String(1000))
    imdb_score = Column(Float)
    genre = Column(Text)
    director = Column(String(1000))
    popularity = Column(Float)

    def __init__(self,movie_name=None,imdb_score=None,genre=None,director=None,popularity=None):
        self.movie_name =  movie_name
        self.imdb_score = imdb_score
        self.genre = genre
        self.director = director
        self.popularity = popularity

    def get_name(self):
        return self.movie_name
    
    def get_genre(self):
        return json.loads(self.genre)
    
