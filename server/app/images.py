import os
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
from exif import Image
import reverse_geocoder as rg
import pycountry
import zipfile

from flask import (
    Blueprint, g, request, session, current_app, send_from_directory, send_file, jsonify, make_response
)

from app.db import get_db

bp = Blueprint('images', __name__, url_prefix='/images')

 # upload images to system with new metadata
@bp.route('', methods=["GET", "POST"])
def images():
    if request.method == "GET":
        db = get_db()
        zipfolder = zipfile.ZipFile('photos.zip','w', compression = zipfile.ZIP_STORED)
        photos = db.execute("SELECT photo_path, photo_name, photo_description FROM photos").fetchall()
        for photo in photos:
            zipfolder.write(photo[0])
        zipfolder.close()
        return send_file(os.path.dirname(current_app.instance_path) + '\\photos.zip')

    if request.method == "POST":
        images = []
        db = get_db()
        for file in request.files:
            filename = secure_filename(request.files[file].filename)
            request.files[file].save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            with open(current_app.config['UPLOAD_FOLDER'] + filename, "rb") as photo_file:
                photo_image = Image(photo_file)
                if photo_image.has_exif == False:
                    photo_image.image_description = 'unknown'
                else:
                    decimal_latitude = dms_coordinates_to_dd_coordinates(photo_image.get('gps_latitude','unknown'), photo_image.get('gps_latitude_ref', 'unknown'))
                    decimal_longitude = dms_coordinates_to_dd_coordinates(photo_image.get('gps_longitude','unknown'), photo_image.get('gps_longitude_ref', 'unknown'))
                    if decimal_latitude != 'unknown' and decimal_longitude != 'unknown':
                        coordinates = (decimal_latitude, decimal_longitude)
                        location_info = rg.search(coordinates)[0]
                        location_info['country'] = pycountry.countries.get(alpha_2=location_info['cc'])
                        photo_image.image_description = f'Location: {location_info.get("name")}, {location_info.get("admin1")}'
                db.execute("INSERT INTO photos (photo_path, photo_name, photo_description) VALUES (?, ?, ?)", 
                            (os.path.join(current_app.config['UPLOAD_FOLDER'], filename), filename, photo_image.get('image_description', 'unknown'))
                            )
                db.commit()

                with open(current_app.config['UPLOAD_FOLDER'] + filename, "wb") as photo_file_updated:
                    photo_file_updated.write(photo_image.get_file())
                
        return ('', 200)


    return ('', 500)

def dms_coordinates_to_dd_coordinates(coordinates, coordinates_ref):
    if coordinates == 'unknown' and coordinates_ref == 'unknown':
        return coordinates

    decimal_degrees = coordinates[0] + \
                    coordinates[1] / 60 + \
                    coordinates[2] / 3600
    
    if coordinates_ref == "S" or coordinates_ref == "W":
        decimal_degrees = -decimal_degrees
    
    return decimal_degrees
    