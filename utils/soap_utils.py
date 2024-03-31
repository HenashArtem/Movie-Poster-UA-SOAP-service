import os
import xml.etree.ElementTree as ET


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')


def load_data_from_xml_file_by_name(filename):
    try:
        tree = ET.parse(os.path.join(DATA_DIR, filename))
        root = tree.getroot()
        data = []
        for child in root:
            entity = {}
            for sub_child in child:
                entity[sub_child.tag] = sub_child.text
            data.append(entity)
        return {filename[:-4]: data}
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
        return None


def load_cinema_data_from_xml_file_by_name(filename):
    try:
        tree = ET.parse(os.path.join(DATA_DIR, filename))
        root = tree.getroot()
        data = []
        for child in root.findall('cinema'):
            cinema = {'id': child.find('id').text, 'name': child.find('name').text,
                      'location': child.find('location').text}
            movies_playing = []
            for movie in child.find('movies_playing').findall('movie_id'):
                movies_playing.append(movie.text)
            cinema['movies_playing'] = movies_playing
            data.append(cinema)
        return {filename[:-4]: data}
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
        return None


def save_data_in_file_by_filename(data, filename):
    try:
        root = ET.Element(filename[:-4] + 's')
        for entity in data.get(filename[:-4], []):
            child = ET.SubElement(root, filename[:-4])
            for key, value in entity.items():
                sub_child = ET.SubElement(child, key)
                sub_child.text = str(value)
        tree = ET.ElementTree(root)
        tree.write(os.path.join(DATA_DIR, filename))
    except Exception as e:
        print(f"An error occurred while saving data to '{filename}': {e}")


def save_cinema_data_in_file_by_filename(data, filename):
    try:
        root = ET.Element('cinemas')
        for entity in data.get(filename[:-4], []):
            cinema = ET.SubElement(root, 'cinema')
            ET.SubElement(cinema, 'id').text = str(entity['id'])
            ET.SubElement(cinema, 'name').text = entity['name']
            ET.SubElement(cinema, 'location').text = entity['location']
            movies_playing = ET.SubElement(cinema, 'movies_playing')
            for movie_id in entity['movies_playing']:
                ET.SubElement(movies_playing, 'movie_id').text = movie_id
        tree = ET.ElementTree(root)
        tree.write(os.path.join(DATA_DIR, filename))
    except Exception as e:
        print(f"An error occurred while saving data to '{filename}': {e}")


def get_next_id(data, entity_type):
    entities = data.get(entity_type, [])
    if entities:
        return max(int(entity.get('id', 0)) for entity in entities) + 1
    else:
        return 1
