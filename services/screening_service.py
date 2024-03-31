from spyne import rpc, ServiceBase
from spyne.model.complex import ComplexModel
from spyne.model.primitive import Integer, Unicode

from utils.models import Screening
from utils.soap_utils import load_data_from_xml_file_by_name, save_data_in_file_by_filename


class ScreeningService(ServiceBase):
    @rpc(Integer, Integer, Integer, Unicode, _returns=Unicode)
    def add_screening(self, movie_id, cinema_id, screening_id, time):

        data = load_data_from_xml_file_by_name('screenings.xml')

        existing_screening = next((screening for screening in data['screenings'] if screening['id'] == screening_id), None)
        if existing_screening:
            return f'Screening with ID {screening_id} already exists'

        if not movie_id:
            return "Movie ID cannot be empty"
        if not cinema_id:
            return "Cinema ID cannot be empty"
        if not time:
            return "Time cannot be empty"

        new_screening = {'id': screening_id, 'movie_id': movie_id, 'cinema_id': cinema_id, 'time': time}

        data['screenings'].append(new_screening)

        save_data_in_file_by_filename(data, 'screenings.xml')

        return f'Screening with ID {screening_id} added successfully'

    @rpc(Integer, _returns=ComplexModel(Screening))
    def get_screening(self, screening_id):
        data = load_data_from_xml_file_by_name('screenings.xml')
        screening = next((screening for screening in data['screenings'] if int(screening['id']) == int(screening_id)), None)
        if screening:
            return screening
        else:
            return f'Screening with ID {screening_id} not found'

    @rpc(_returns=ComplexModel(Screening))
    def get_screenings(self):
        try:
            data = load_data_from_xml_file_by_name('screenings.xml')
            return data['screenings']
        except Exception as e:
            return f'Error occurred while retrieving screenings: {str(e)}'

    @rpc(Integer, Integer, Integer, Unicode, _returns=Unicode)
    def update_screening(self, movie_id, cinema_id, screening_id, time):
        try:
            if not movie_id:
                return "Movie ID cannot be empty"
            if not cinema_id:
                return "Cinema ID cannot be empty"
            if not time:
                return "Time cannot be empty"

            data = load_data_from_xml_file_by_name('screenings.xml')
            for screening in data['screenings']:
                if int(screening['id']) == int(screening_id):
                    screening['movie_id'] = movie_id
                    screening['cinema_id'] = cinema_id
                    screening['time'] = time
                    save_data_in_file_by_filename(data, 'screenings.xml')
                    return f'Screening with ID {screening_id} updated successfully'
            return f'Screening with ID {screening_id} not found'
        except Exception as e:
            return f'Error occurred while updating screening: {str(e)}'

    @rpc(Integer, _returns=Unicode)
    def delete_screening(self, screening_id):
        try:
            data = load_data_from_xml_file_by_name('screenings.xml')
            screenings = data.get('screenings', [])

            filtered_screenings = filter(lambda screening: int(screening.get('id')) != int(screening_id), screenings)

            filtered_screenings_dict = [
                {'id': screening['id'], 'movie_id': screening['movie_id'],
                 'cinema_id': screening['cinema_id'], 'time': screening['time']}
                for screening in filtered_screenings]
            if len(filtered_screenings_dict) == len(screenings):
                return f'Screening with ID {screening_id} not found'

            save_data_in_file_by_filename({'screenings': filtered_screenings_dict}, 'screenings.xml')
            return f'Screening with ID {screening_id} deleted successfully'
        except Exception as e:
            return f'Error occurred while deleting screening: {str(e)}'
