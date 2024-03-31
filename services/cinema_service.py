from spyne import rpc, ServiceBase
from spyne.model.complex import ComplexModel
from spyne.model.primitive import Integer, Unicode

from utils.models import Cinema
from utils.soap_utils import load_cinema_data_from_xml_file_by_name, save_cinema_data_in_file_by_filename


class CinemaService(ServiceBase):
    @rpc(Unicode, Unicode, Unicode, _returns=Unicode)
    def add_cinema(self, name, location, movies_playing):

        data = load_cinema_data_from_xml_file_by_name('cinemas.xml')

        existing_cinema = next((cinema for cinema in data['cinemas'] if cinema['name'] == name), None)
        if existing_cinema:
            return f'Cinema "{name}" already exists'

        if not name:
            return "Name cannot be empty"
        if not location:
            return "Location cannot be empty"
        if not movies_playing:
            return "Movies playing cannot be empty"

        new_cinema = {'id': len(data['cinemas']) + 1, 'name': name,
                      'location': location, 'movies_playing': movies_playing}

        data['cinemas'].append(new_cinema)

        save_cinema_data_in_file_by_filename(data, 'cinemas.xml')

        return f'Cinema "{name}" added successfully'

    @rpc(Integer, _returns=ComplexModel(Cinema))
    def get_cinema(self, cinema_id):
        data = load_cinema_data_from_xml_file_by_name('cinemas.xml')
        cinema = data['cinemas'][cinema_id - 1]
        if cinema:
            return cinema
        else:
            return f'Cinema with ID {cinema_id} not found'

    @rpc(_returns=ComplexModel(Cinema))
    def get_cinemas(self):
        try:
            data = load_cinema_data_from_xml_file_by_name('cinemas.xml')
            return data['cinemas']
        except Exception as e:
            return f'Error occurred while retrieving cinemas: {str(e)}'

    @rpc(Integer, Unicode, Unicode, Unicode, _returns=Unicode)
    def update_cinema(self, cinema_id, name, location, movies_playing):
        try:
            if not name:
                return "Name cannot be empty"
            if not location:
                return "Location cannot be empty"
            if not movies_playing:
                return "Movies playing cannot be empty"

            data = load_cinema_data_from_xml_file_by_name('cinemas.xml')
            for cinema in data['cinemas']:
                if int(cinema['id']) == int(cinema_id):
                    cinema['name'] = name
                    cinema['location'] = location
                    cinema['movies_playing'] = movies_playing
                    save_cinema_data_in_file_by_filename(data, 'cinemas.xml')
                    return f'Cinema with ID {cinema_id} updated successfully'
            return f'Cinema with ID {cinema_id} not found'
        except Exception as e:
            return f'Error occurred while updating cinema: {str(e)}'

    @rpc(Integer, _returns=Unicode)
    def delete_cinema(self, cinema_id):
        try:
            data = load_cinema_data_from_xml_file_by_name('cinemas.xml')
            cinemas = data.get('cinemas', [])

            filtered_cinemas = filter(lambda cinema: int(cinema.get('id')) != int(cinema_id), cinemas)

            filtered_cinemas_dict = [
                {'id': cinema['id'], 'name': cinema['name'], 'location': cinema['location'],
                 'movies_playing': cinema['movies_playing']}
                for cinema in filtered_cinemas]
            if len(filtered_cinemas_dict) == len(cinemas):
                return f'Cinema with ID {cinema_id} not found'

            save_cinema_data_in_file_by_filename({'cinemas': filtered_cinemas_dict}, 'cinemas.xml')
            return f'Cinema with ID {cinema_id} deleted successfully'
        except Exception as e:
            return f'Error occurred while deleting cinema: {str(e)}'
