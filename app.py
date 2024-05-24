import os
from flask import Flask, request, jsonify, send_file, render_template, g

from auth import basic_auth
from database.base import init_database
from database.utils import insert_file_record, is_owner_file, delete_file_record
from utils import allowed_file, get_hash_file, get_path_file

app = Flask(__name__)
# максимальный размер файла в байтах 16 мб
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = 'store'
app.config.from_prefixed_env()


@app.route('/upload', methods=['POST', 'GET'])
@basic_auth
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if not file:
            return jsonify({"message": "File not loaded"}), 400
        if allowed_file(file.filename):
            hash_filename = get_hash_file(file)
            dir_path = get_path_file(hash_filename, to_dir=True)
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
            file_path = get_path_file(hash_filename)
            if os.path.exists(file_path):
                return jsonify({"message": "File already exist"}), 400

            user = g.user
            insert_file_record(user, hash_filename)
            file.save(file_path)

            return jsonify({"message": hash_filename}), 200
        else:
            return jsonify({"message": "File format is not supported"}), 400
    return render_template('upload_form.html'), 200


@app.route('/download/<hash_filename>', methods=['GET'])
def download_file(hash_filename):
    file_path = get_path_file(hash_filename)
    if os.path.exists(file_path):
        return send_file(file_path)
    else:
        return jsonify({"message": "File not found"}), 404


@app.route('/delete/<hash_filename>', methods=['DELETE'])
@basic_auth
def delete_file(hash_filename):
    file_path = get_path_file(hash_filename)
    if os.path.exists(file_path):
        user = g.user
        if not is_owner_file(hash_filename, user):
            return jsonify({"message": "User not authorized to delete this file"}), 403

        os.remove(file_path)
        delete_file_record(hash_filename)
        return jsonify({"message": "File deleted"}), 204
    else:
        return jsonify({"message": "File not found"}), 404


if __name__ == '__main__':
    init_database()
    app.run(debug=True)
