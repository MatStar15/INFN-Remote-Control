from app import db, celery, app
from app.emitters import emit_job_update
from app.models.job import CalculationJob
import subprocess, os, logging
from datetime import datetime


@celery.task(name='start_calculation')
def run_calculation(job_id, parameters):
    """Run the calculation script as a Celery task

    Args:
        job_id: ID of the calculation job
        parameters: Dictionary of calculation parameters
    """
    logging.info(f"Starting calculation task for job {job_id}")

    with app.app_context():
        job = CalculationJob.query.get(job_id)
        if not job:
            logging.error(f"Job {job_id} not found")
            return False

        try:
            # Create output directory for this job
            output_dir = os.path.join('results', f'job_{job_id}')
            os.makedirs(output_dir, exist_ok=True)

            # Update job status
            job.status = 'running'
            db.session.commit()
            emit_job_update(job)

            # Build command with parameters
            cmd = ['python', 'calculation_script.py',
                   '--output_dir', output_dir,
                   '--job_id', str(job_id),
                   '--iterations', str(parameters.get('iterations', 5)),
                   '--delay', str(parameters.get('delay', 2.0)),
                   '--param1', str(parameters.get('param1', 1.0)),
                   '--param2', str(parameters.get('param2', 2.0))]

            logging.info(f"Running calculation command: {' '.join(cmd)}")

            process = subprocess.run(cmd,
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE,
                                     check=True)

            # Update job status
            job.status = 'completed'
            job.completed_at = datetime.utcnow()
            db.session.commit()
            emit_job_update(job)
            return True

        except subprocess.CalledProcessError as e:
            logging.error(f"Calculation failed: {e.stderr.decode('utf-8')}")
            job.status = 'failed'
            job.completed_at = datetime.utcnow()
            db.session.commit()
            emit_job_update(job)
            return False

        except Exception as e:
            logging.error(f"Exception in calculation task: {str(e)}")
            job.status = 'failed'
            job.completed_at = datetime.utcnow()
            db.session.commit()
            emit_job_update(job)
            return False
