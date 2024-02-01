from models.movie import Movie as MovieModel
from schemas.movie_schema import Movie


class GetMovieService:
    def __init__(self, db) -> None:
        self.db = db


    def get_movie(self, id: int):
        movie = self.db.query(MovieModel).filter(id == MovieModel.id).first()

        return movie


class MovieServices:
    def __init__(self, db) -> None:
        self.db = db

    
    def get_movies(self):
        movies = self.db.query(MovieModel).all()

        return movies
    

    def get_movie_by_name_query(self, name):
        movie = self.db.query(MovieModel).filter(name == MovieModel.nombre).first()

        return movie
    

    def get_movie_by_category_query(self, category):
        movie = self.db.query(MovieModel).filter(category == MovieModel.categoria).first()

        return movie


    def add_movie(self, movie_data: Movie):
        new_movie = MovieModel(**movie_data.dict())

        self.db.add(new_movie)
        self.db.commit()


    def update_a_movie(self, id: int, data_to_update: Movie):
        movie_to_update = GetMovieService(self.db).get_movie(id)

        movie_to_update.nombre = data_to_update.nombre
        movie_to_update.año = data_to_update.año
        movie_to_update.categoria = data_to_update.categoria
        movie_to_update.reseñas = data_to_update.reseñas
        
        self.db.commit()


    def delete_a_movie(self, id: int):
        movie_to_delete = GetMovieService(self.db).get_movie(id)

        self.db.delete(movie_to_delete)
        self.db.commit()
