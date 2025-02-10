# Copyright (c) 2025 The OSCAL Compass Authors. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import os
import subprocess
import tempfile
from typing import List

from flask import Flask, request, jsonify, send_file
from flasgger import Swagger
from werkzeug.utils import secure_filename

app = Flask(__name__)

# configure swagger with custom title and version
app.config['SWAGGER'] = {
    'title': 'OSCAL Compass: trestle transformation services',
    'description': 'Employ OSCAL Compass trestle to materialize OSCAL documents from source documents\n <img src="/static/images/oscal-compass-color.png" width="150" height="150"/>',
    'version': '1.0.0',
    'termsOfService': None,
}

swagger = Swagger(app)

# define allowed extensions
ALLOWED_EXTENSIONS_CISB = {'xlsx'}

def allowed_file(filename: str, allowed_extenstions: List[str]) -> bool:
    """Allowed file."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extenstions

def create_trestle_task_config_file(tmpdirname: str, cfg_filepath: str, src_filename: str) -> str:
    """Create trestle task config file."""
    rval = None
    with open(cfg_filepath, 'w') as task_config_file:
        tcf_line(task_config_file, '[task.cis-xlsx-to-oscal-cd]')
        tcf_kvp(task_config_file, 'benchmark-file', src_filename)
        tcf_kvp(task_config_file, 'benchmark-title', get_benchmark_title(src_filename))
        tcf_kvp(task_config_file, 'benchmark-version', get_benchmark_version(src_filename))
        tcf_kvp(task_config_file, 'component-name', get_component_name(src_filename))
        tcf_kvp(task_config_file, 'component-description', get_component_description(src_filename))
        tcf_kvp(task_config_file, 'component-type', get_component_type())
        tcf_kvp(task_config_file, 'namespace', get_namespace())
        tcf_kvp(task_config_file, 'profile-source', get_profile_source())
        tcf_kvp(task_config_file, 'profile-version', get_profile_version())
        tcf_kvp(task_config_file, 'profile-description', get_profile_description())
        tcf_kvp(task_config_file, 'output-dir', get_output_dir(tmpdirname))
        tcf_kvp(task_config_file, 'output-overwrite', get_output_overwrite())
    return rval

def tcf_line(task_config_file, line: str) -> None:
    """Write line to task config file."""
    if line:
        task_config_file.write(f'{line}\n')
        
def tcf_kvp(task_config_file, key: str, value: str) -> None:
    """Write key:value to task config file."""
    if value:
        task_config_file.write(f'{key} = {value}\n')
                
def get_benchmark_title(src_filename: str) -> str:
    """Get benchmark title."""
    try:
        part = src_filename
        part = part.split('Benchmark_v')[0]
        part = part.replace('_', ' ')
        part = f'{part}Benchmark'
        default = part
    except Exception:
        default = None
    rval = request.args.get('benchmark-title', default)
    return rval

def get_benchmark_version(src_filename: str) -> str:
    """Get benchmark version."""
    try:
        part = src_filename
        part = part.split('Benchmark_v')[1]
        default = part
    except Exception:
        default = None
    rval = request.args.get('benchmark-version', default)
    return rval

def get_component_name(src_filename: str) -> str:
    """Get component name."""
    try:
        part = src_filename
        part = part.split('_Benchmark')[0]
        part = part.split('CIS_')[1]
        default = part.replace('_', ' ')
    except Exception:
        default = None
    rval = request.args.get('component-name', default)
    return rval
                
def get_component_description(src_filename: str) -> str:
    """Get component description."""
    try:
        part = src_filename
        part = part.split('_Benchmark')[0]
        part = part.split('CIS_')[1]
        default = part.replace('_', ' ')
    except Exception:
        default = None
    rval = request.args.get('component-description', default)
    return rval

def get_component_type() -> str:
    """Get component-type."""
    default = 'software'
    rval = request.args.get('component-type', default)
    return rval

def get_namespace() -> str:
    """Get namespace."""
    default = 'https://oscal-compass/compliance-trestle/schemas/oscal/cd'
    rval = request.args.get('namespace', default)
    return rval

def get_profile_source() -> str:
    """Get profile-source."""
    default = 'data/catalogs/CIS_controls_v8/catalog.json'
    rval = request.args.get('profile-source', default)
    return rval

def get_profile_version() -> str:
    """Get profile-version."""
    try:
        parts = get_profile_source().split('/')
        default = parts[-2].replace('CIS_controls_', '')
    except Exception:
        default = None
    rval = request.args.get('profile-version', default)
    return rval

def get_profile_description() -> str:
    """Get profile-description."""
    try:
        parts = get_profile_source().split('/')
        default = parts[-2].replace('_', ' ')
    except Exception:
        default = None
    rval = request.args.get('profile-description', default)
    return rval

def get_output_dir(tmpdirname: str) -> str:
    """Get output-dir."""
    rval = tmpdirname
    return rval

def get_output_overwrite() -> str:
    """Get output-overwrite."""
    rval = 'true'
    return rval

@app.route('/cis-xlsx-to-oscal-cd', methods=['POST'])
def task_cis_xlsx_to_oscal_cd():
    """
    Upload CIS Benchmark (.xlsx); return corresponding OSCAL Component Definition (.json)
    ---
    tags: 
      - CIS Benchmark to OSCAL Component Definition
    parameters:
      - name: file
        in: formData
        type: file
        required: true
        description: The CIS Benchmark .xlsx file to upload, e.g "CIS_IBM_Db2_13_for_z_OS_Benchmark_v1.0.0.xlsx".
      - name: benchmark-title
        in: query
        type: string
        required: false
        description: The benchmark-title for the OSCAL Component Definition (optional); default is derived from required file name, e.g. "CIS IBM Db2 13 for z OS Benchmark".
      - name: benchmark-version
        in: query
        type: string
        required: false
        description: The benchmark-version for the OSCAL Component Definition (optional); default is derived from required file name, e.g. "1.0.0".
      - name: component-name
        in: query
        type: string
        required: false
        description: The component-name for the OSCAL Component Definition (optional); default is derived from required file name, e.g. "IBM Db2 13 for z OS".
      - name: component-description
        in: query
        type: string
        required: false
        description: The component-description for the OSCAL Component Definition (optional); default is derived from required file name, e.g. "IBM Db2 13 for z OS".
      - name: component-type
        in: query
        type: string
        required: false
        description: The component-type for the OSCAL Component Definition (optional); default is "software".
      - name: namespace
        in: query
        type: string
        required: false
        description: The namespace for the OSCAL Component Definition (optional); default is "https://oscal-compass/compliance-trestle/schemas/oscal/cd".
      - name: profile-source
        in: query
        type: string
        required: false
        description: The profile-source for the OSCAL Component Definition (optional); default is "data/catalogs/CIS_controls_v8/catalog.json".
      - name: profile-version
        in: query
        type: string
        required: false
        description: The profile-version for the OSCAL Component Definition (optional); default is derived from profile-source, e.g. "v8".
      - name: profile-description
        in: query
        type: string
        required: false
        description: The profile-description for the OSCAL Component Definition (optional); default is derived from profile-source, e.g. "CIS controls v8".
    responses:
      200:
        description: File uploaded and transformed successfully
      400:
        description: File missing or invalid, or a default value could not be properly inferred for an optional field that was left blank
      500:
        description: Server error
    """
    try:
        # check if the file part is present in the request
        if 'file' not in request.files:
            return jsonify({'message': 'No file part'}), 400
        file = request.files['file']
        # check if no file is selected
        if file.filename == '':
            return jsonify({'message': 'No selected file'}), 400
        # check if the file is allowed
        if not allowed_file(file.filename, ALLOWED_EXTENSIONS_CISB):
            return jsonify({'message': 'Invalid file format'}), 400
        # process file
        with tempfile.TemporaryDirectory() as tmpdirname:
            # save src file
            src_filename = secure_filename(file.filename)
            file.save(os.path.join(tmpdirname, src_filename))
            # create cfg file
            cfg_filename = 'task.config'
            cfg_filepath = os.path.join(tmpdirname, cfg_filename)
            status = create_trestle_task_config_file(tmpdirname, cfg_filepath, src_filename)
            if status:
                text = f'Unable to create {cfg_filepath}: {status}'
                return jsonify({'message': f'{text}'}), 400
            # change working directory
            cwd = os.getcwd()
            os.chdir(tmpdirname)
            # trestle init
            command = 'trestle init'
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            text = f'{command} rc={result.returncode}, stdout={result.stdout} stderr={result.stderr}'
            if result.returncode != 0:
                return jsonify({'message': f'{text}'}), 400
            # trestle task
            command = f'trestle task cis-xlsx-to-oscal-cd -c {cfg_filename}'
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            text = f'{command} rc={result.returncode}, stdout={result.stdout} stderr={result.stderr}'
            if result.returncode != 0:
                return jsonify({'message': f'{text}'}), 400
            # OSCAL component-defintion.json
            json_filename = 'component-definition.json'
            json_file_path = os.path.join(tmpdirname, json_filename)
            # send file
            message = send_file(
                json_file_path,
                as_attachment=True,
                download_name=json_filename,  # this will be the filename on the client
                mimetype='application/json'
            )
            return message, 200
    except Exception as e:
        return jsonify({'message': f'Server error: {e}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
