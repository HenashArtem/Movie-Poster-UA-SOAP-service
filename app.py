import argparse
from flask import Flask
from spyne import Application
from spyne.server.wsgi import WsgiApplication
from spyne.protocol.soap import Soap11
from services.movie_service import MovieService
from services.cinema_service import CinemaService
from services.user_service import UserService
from services.screening_service import ScreeningService

app = Flask(__name__)

spyne_app = Application(
    [MovieService, CinemaService, ScreeningService, UserService],
    'lab_1.soap',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11()
)
wsgi_app = WsgiApplication(spyne_app)


def parse_arguments():
    parser = argparse.ArgumentParser(description='Specify the resource to display.')
    parser.add_argument('--movies', action='store_true', help='Display movies')
    parser.add_argument('--cinemas', action='store_true', help='Display cinemas')
    parser.add_argument('--screenings', action='store_true', help='Display screenings')
    parser.add_argument('--users', action='store_true', help='Display users')
    return parser.parse_args()


@app.route('/', methods=['GET'])
def home():
    return "Welcome to the SOAP service. Use setup arguments --{resource} to access resources.", 200


@app.route('/soap', methods=['GET', 'POST', 'DELETE', 'PUT'])
def soap_handler():
    args = parse_arguments()

    if args.movies:
        movie_service = MovieService()
        return movie_service.get_movies(wsgi_app)
    elif args.cinemas:
        cinema_service = CinemaService()
        return cinema_service.get_cinemas(wsgi_app)
    elif args.screenings:
        screening_service = ScreeningService()
        return screening_service.get_screenings(wsgi_app)
    elif args.users:
        user_service = UserService()
        return user_service.get_users(wsgi_app)
    else:
        return "Invalid resource. Available resources: movies, cinemas, screenings, users", 400


if __name__ == '__main__':
    app.config['DEBUG'] = True
    app.config['PORT'] = 5000
    app.run()
