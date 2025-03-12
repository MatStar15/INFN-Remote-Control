from flask import Blueprint, render_template, redirect, url_for, flash, request, get_flashed_messages
from app.models.job import CalculationJob, ResultFile
from app import db

main = Blueprint('main', __name__)


@main.route('/')
def index():
    """Dashboard showing jobs and files"""
    jobs = CalculationJob.query.order_by(CalculationJob.started_at.desc()).all()
    return render_template('index.html', jobs=jobs)


@main.route('/job/<int:job_id>')
def job_detail(job_id):
    """View for a specific job"""
    job = CalculationJob.query.get_or_404(job_id)
    return render_template('job_detail.html', job=job)


@main.route('/new-job', methods=['GET', 'POST'])
def new_job():
    if request.method == 'POST':
        try:
            # Ensure parameters is a dictionary

            print("New-job request!")

            parameters = {
                'param1': request.form.get('param1', ''),
                'param2': request.form.get('param2', ''),
                # Add other parameters as needed
            }

            # Remove any None or empty string values
            parameters = {k: v for k, v in parameters.items() if v}

            # Create job
            job = CalculationJob(
                status='pending',
                parameters=parameters
            )
            db.session.add(job)
            db.session.commit()

            # Start the calculation task
            from app.tasks.calculation import run_calculation
            run_calculation.delay(job.id, parameters)

            flash('Job created successfully!', 'success')
            return redirect(url_for('main.job_detail', job_id=job.id))

        except Exception as e:
            # Log the error
            print(f"Error creating job: {str(e)}")
            flash(f'Error creating job: {str(e)}', 'error')
            return redirect(url_for('main.index'))

    # GET request - render the form
    return render_template('new_job.html')