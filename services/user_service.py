from spyne import rpc, ServiceBase
from spyne.model.complex import ComplexModel
from spyne.model.primitive import Integer, Unicode

from utils.soap_utils import load_data_from_xml_file_by_name, save_data_in_file_by_filename


class UserService(ServiceBase):
    @rpc(Unicode, Unicode, _returns=Unicode)
    def add_user(self, username, email):

        data = load_data_from_xml_file_by_name('users.xml')

        existing_user = next((user for user in data['users'] if user['username'] == username), None)
        if existing_user:
            return f'User "{username}" already exists'

        if not username:
            return "Username cannot be empty"
        if not email:
            return "Email cannot be empty"

        new_user = {'id': len(data['users']) + 1, 'username': username, 'email': email}

        data['users'].append(new_user)

        save_data_in_file_by_filename(data, 'users.xml')

        return f'User "{username}" added successfully'

    @rpc(Integer, _returns=ComplexModel(dict))
    def get_user(self, user_id):
        data = load_data_from_xml_file_by_name('users.xml')
        user = next((user for user in data['users'] if int(user['id']) == int(user_id)), None)
        if user:
            return user
        else:
            return f'User with ID {user_id} not found'

    @rpc(_returns=ComplexModel(dict))
    def get_users(self):
        try:
            data = load_data_from_xml_file_by_name('users.xml')
            return data['users']
        except Exception as e:
            return f'Error occurred while retrieving users: {str(e)}'

    @rpc(Integer, Unicode, Unicode, _returns=Unicode)
    def update_user(self, user_id, username, email):
        try:
            if not username:
                return "Username cannot be empty"
            if not email:
                return "Email cannot be empty"

            data = load_data_from_xml_file_by_name('users.xml')
            for user in data['users']:
                if int(user['id']) == int(user_id):
                    user.update({'username': username, 'email': email})
                    save_data_in_file_by_filename(data, 'users.xml')
                    return f'User with ID {user_id} updated successfully'
            return f'User with ID {user_id} not found'
        except Exception as e:
            return f'Error occurred while updating user: {str(e)}'

    @rpc(Integer, _returns=Unicode)
    def delete_user(self, user_id):
        try:
            data = load_data_from_xml_file_by_name('users.xml')
            users = data.get('users', [])

            filtered_users = [user for user in users if int(user['id']) != int(user_id)]

            if len(filtered_users) == len(users):
                return f'User with ID {user_id} not found'

            save_data_in_file_by_filename({'users': filtered_users}, 'users.xml')
            return f'User with ID {user_id} deleted successfully'
        except Exception as e:
            return f'Error occurred while deleting user: {str(e)}'
