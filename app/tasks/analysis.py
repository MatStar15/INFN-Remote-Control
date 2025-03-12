from app import celery, db, socketio
from app.models.job import ResultFile
import subprocess
import os


@celery.task
def analyze_file(file_id):
    """Interface with your analysis script for a specific file"""
    file = ResultFile.query.get(file_id)
    if not file:
        print(f"File {file_id} not found")
        return False

    try:
        # Create output filename - replace extension or add .analyzed
        if '.' in file.filename:
            base_name, ext = os.path.splitext(file.filename)[0], os.path.splitext(file.filename)[1]
            analyzed_filename = f"{base_name}.analyzed"
        else:
            analyzed_filename = f"{file.filename}.analyzed"

        # Get output directory (same as input file)
        output_dir = os.path.dirname(file.filepath)
        output_path = os.path.join(output_dir, analyzed_filename)

        # Run your analysis script on this file
        cmd = ['python', 'analysis_script.py',
               '--input', file.filepath,
               '--output', output_path]

        print(f"Running analysis command: {' '.join(cmd)}")

        process = subprocess.run(cmd,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE,
                                 check=True)

        # Update the file record
        file.analyzed = True
        file.analysis_filepath = output_path
        db.session.commit()


        # Notify clients
        # socketio.emit('file_analyzed', {
        #     'file': file.to_dict(),
        #     'job_id': file.job_id
        # })
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
