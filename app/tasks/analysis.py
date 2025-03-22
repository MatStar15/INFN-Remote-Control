from app import celery, db, socketio, app
from app.models.job import ResultFile
import subprocess, os, logging


@celery.task(name='analyze_file')
def analyze_file(file_id):
    """Interface with your analysis script for a specific file"""
    with app.app_context():
        file = ResultFile.query.get(file_id)
        if not file:
            print(f"File {file_id} not found")
            return False

        try:
            # Create output filename - replace extension or add .analyzed
            if '.' in file.filename:
                base_name = os.path.splitext(file.filename)[0]
                analyzed_filename = f"{base_name}" + app.config.get('ANALYZED_FILE_EXTENSION', '.analyzed')
            else:
                analyzed_filename = f"{file.filename}.analyzed"

            # Get output directory (same as input file)
            output_dir = os.path.dirname(file.filepath)
            output_path = os.path.join(output_dir, analyzed_filename)

            # Run your analysis script on this file
            cmd = ['python', 'analysis_script.py',
                   '--input', file.filepath,
                   '--output', output_path]

            logging.info(f"Running analysis command: {' '.join(cmd)}")

            process = subprocess.run(cmd,
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE,
                                     check=True)

            # # Update the file record
            # file.analyzed = True
            file.analysis_filepath = output_path
            db.session.commit()
            return True

        except subprocess.CalledProcessError as e:
            print(f"Analysis failed: {e.stderr.decode('utf-8')}")
            socketio.emit('file_analysis_failed', {
                'file_id': file_id,
                'error': str(e)
            })
            raise e
        except Exception as e:
            print(f"Exception in analysis task: {str(e)}")
            socketio.emit('file_analysis_failed', {
                'file_id': file_id,
                'error': str(e)
            })
            raise e
