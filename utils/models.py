class Movie:
    def __init__(self, id, title, genre, duration):
        self.id = id
        self.title = title
        self.genre = genre
        self.duration = duration

    def to_dict(self):
        return {'id': self.id, 'title': self.title, 'genre': self.genre, 'duration': self.duration}


class Cinema:
    def __init__(self, id, name, location, movies_playing):
        self.id = id
        self.name = name
        self.location = location
        self.movies_playing = movies_playing

    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'location': self.location, 'movies_playing': self.movies_playing}


class Screening:
    def __init__(self, id, movie_id, cinema_id, time):
        self.id = id
        self.movie_id = movie_id
        self.cinema_id = cinema_id
        self.time = time

    def to_dict(self):
        return {'id': self.id, 'movie_id': self.movie_id, 'cinema_id': self.cinema_id, 'time': self.time}


class User:
    def __init__(self, id, username, email):
        self.id = id
        self.username = username
        self.email = email

    def to_dict(self):
        return {'id': self.id, 'username': self.username, 'email': self.email}
