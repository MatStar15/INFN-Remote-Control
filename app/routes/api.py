from flask import Blueprint, jsonify, request, send_from_directory
from app import db
from app.models.job import CalculationJob, ResultFile
from app.tasks.calculation import run_calculation
from app.emitters import emit_job_update
import os

api = Blueprint('api', __name__)


@api.route('/start-job', methods=['POST'])
def create_job():
    try:
        data = request.get_json()
        if not data or 'parameters' not in data:
            return jsonify({'message': 'No parameters provided'}), 400

        parameters = data.get('parameters')

        # Create new job record
        job = CalculationJob(
            status='pending',
            parameters=parameters
        )
        db.session.add(job)
        db.session.commit()  # Commit first to ensure job exists

        # job = CalculationJob.query.get_or_404(parameters.get('job_id'))
        # if job is None:
        #     return jsonify({'message': 'Job not found'}),

        # Launch calculation task with error handling
        try:
            print("Creating job")
            task = run_calculation.delay(job.id, parameters)
            job.task_id = task.id

            print(f"Task started: {task.id}")
            job.status = 'running'
            db.session.commit()
            emit_job_update(job)

            return jsonify({
                'message': 'Job started successfully',
                'job': job.to_dict(),
                'status': 'success'
            }), 201

        except Exception as task_error:
            print(f"Task error: {str(task_error)}")
            job.status = 'failed'
            db.session.commit()
            return jsonify({
                'message': f'Failed to start job: {str(task_error)}'
            }), 500

    except Exception as e:
        print(f"Server error: {str(e)}")
        db.session.rollback()  # Roll back any failed transaction
        return jsonify({
            'message': f'Server error: {str(e)}'
        }), 500

@api.route('/jobs/<int:job_id>/stop', methods=['POST'])
def stop_job(job_id):
    job = CalculationJob.query.get_or_404(job_id)

    if job.status != 'running':
        return jsonify({'message': 'Job is not running'}), 400

    try:
        # Implement job stopping logic here
        job.status = 'stopped'
        db.session.commit()

        return jsonify({
            'message': 'Job stopped successfully',
            'job': job.to_dict()
        })

    except Exception as e:
        return jsonify({
            'message': f'Failed to stop job: {str(e)}'
        }), 500


@api.route('/files/<int:file_id>/download')
def download_file(file_id):
    print(f"Downloading file {file_id}")
    file = ResultFile.query.get_or_404(file_id)
    analyzed = request.args.get('analyzed', '').lower() == 'true'

    filepath = file.analysis_filepath if analyzed else file.filepath

    if not filepath or not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return jsonify({'message': 'File not found'}), 404

    directory = os.path.dirname(filepath)
    filename = os.path.basename(filepath)

    if not directory or not os.path.exists(directory):
        print(f"Directory not found: {directory}")
        return jsonify({'message': 'File directory not found'}), 404

    package = send_from_directory(
        directory,
        filename,
        as_attachment = True
    )

    print(package)

    return package


@api.route('/files/<int:file_id>/analyze', methods=['POST'])
def analyze_file(file_id):
    file = ResultFile.query.get_or_404(file_id)

    if file.analyzed:
        return jsonify({'message': 'File already analyzed'}), 400

    try:
        from app.tasks.analysis import analyze_file as analyze_file_task
        analyze_file_task.delay(file.id)

        return jsonify({
            'message': 'Analysis started successfully',
            'file': file.to_dict()
        })

    except Exception as e:
        return jsonify({
            'message': f'Failed to start analysis: {str(e)}'
        }), 500