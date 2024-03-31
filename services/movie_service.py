from spyne import rpc, ServiceBase
from spyne.model.complex import ComplexModel
from spyne.model.primitive import Integer, Unicode

from utils.models import Movie
from utils.soap_utils import load_data_from_xml_file_by_name, save_data_in_file_by_filename


class MovieService(ServiceBase):
    @rpc(Unicode, Unicode, Unicode, _returns=Unicode)
    def add_movie(self, title, genre, duration):

        data = load_data_from_xml_file_by_name('movies.xml')

        existing_movie = next((movie for movie in data['movies'] if movie['title'] == title), None)
        if existing_movie:
            return f'Movie "{title}" already exists'

        if not title:
            return "Title cannot be empty"
        if not duration:
            return "Duration cannot be empty"
        if not genre:
            return "Genre cannot be empty"

        new_movie = Movie(None, title, genre, duration)

        new_movie.id = len(data['movies']) + 1

        data['movies'].append(new_movie.to_dict())

        save_data_in_file_by_filename(data, 'movies.xml')

        return f'Movie "{title}" added successfully'

    @rpc(Integer, _returns=ComplexModel(Movie))
    def get_movie(self, movie_id):
        data = load_data_from_xml_file_by_name('movies.xml')
        movie = data['movies'][movie_id - 1]
        if movie:
            if int(movie['id']) == int(movie_id):
                return movie
        else:
            return f'Movie with ID {movie_id} not found'

    @rpc(_returns=ComplexModel(Movie))
    def get_movies(self):
        try:
            data = load_data_from_xml_file_by_name('movies.xml')
            return data['movies']
        except Exception as e:
            return f'Error occurred while retrieving movies: {str(e)}'

    @rpc(Integer, Unicode, Unicode, Unicode, _returns=Unicode)
    def update_movie(self, movie_id, title, genre, duration):
        try:
            if not title:
                return "Title cannot be empty"
            if not duration:
                return "Duration cannot be empty"
            if not genre:
                return "Genre cannot be empty"

            data = load_data_from_xml_file_by_name('movies.xml')
            for movie in data['movies']:
                if int(movie['id']) == int(movie_id):
                    movie['title'] = title
                    movie['genre'] = genre
                    movie['duration'] = duration
                    save_data_in_file_by_filename(data, 'movies.xml')
                    return f'Movie with ID {movie_id} updated successfully'
            return f'Movie with ID {movie_id} not found'
        except Exception as e:
            return f'Error occurred while updating movie: {str(e)}'

    @rpc(Integer, _returns=Unicode)
    def delete_movie(self, movie_id):
        try:
            data = load_data_from_xml_file_by_name('movies.xml')
            movies = data.get('movies', [])

            filtered_movies = filter(lambda movie: int(movie.get('id')) != int(movie_id), movies)

            filtered_movies_dict = [
                {'id': movie['id'], 'title': movie['title'], 'genre': movie['genre'], 'duration': movie['duration']} for
                movie in filtered_movies]
            if len(filtered_movies_dict) == len(movies):
                return f'Movie with ID {movie_id} not found'

            save_data_in_file_by_filename({'movies': filtered_movies_dict}, 'movies.xml')
            return f'Movie with ID {movie_id} deleted successfully'
        except Exception as e:
            return f'Error occurred while deleting movie: {str(e)}'

