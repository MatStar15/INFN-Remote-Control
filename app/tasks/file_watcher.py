from watchdog.events import FileSystemEventHandler
from app.models.job import CalculationJob, ResultFile
from app import db, socketio
from app.emitters import *
import os, re, threading, logging

logger = logging.getLogger(__name__)


class ResultFileHandler(FileSystemEventHandler):
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ResultFileHandler, cls).__new__(cls)
            cls._instance.__init__(*args, **kwargs)
        return cls._instance

    def __init__(self, app):
        try:
            if self.app:
                logger.debug("Watcher instance already exists")
                return
        except Exception as e:
            logger.debug(f"Creating new watcher instance")
        self.app = app

        # Patterns for file matching
        result_extension = app.config.get('RESULT_FILE_EXTENSION')
        if not result_extension.startswith('.'):
            result_extension = f'.{result_extension}'
        if not result_extension:
            logger.error("Invalid result file extension")
            raise ValueError("Invalid result file extension")

        analyzed_extension = app.config.get('ANALYZED_FILE_EXTENSION')
        if not analyzed_extension.startswith('.'):
            analyzed_extension = f'.{analyzed_extension}'
        if not analyzed_extension:
            logger.error("Invalid analyzed file extension")
            raise ValueError("Invalid analyzed file extension")

        self.result_pattern = re.compile(result_extension)
        self.analyzed_pattern = re.compile(analyzed_extension)

        self.job_pattern = re.compile(r'job_(\d+)')

        logger.info(f"Result pattern: {self.result_pattern.pattern}")
        logger.info(f"Analyzed pattern: {self.analyzed_pattern.pattern}")
        logger.debug(f"Job pattern: {self.job_pattern.pattern}")


    def on_created(self, event):
        if event.is_directory:
            return

        filepath = event.src_path
        filename = os.path.basename(filepath)

        logger.debug(f"New file created: {filename}")

        logger.debug(f"New file created: {filename}")

        # Skip temporary files
        if filename.startswith('.') or filename.startswith('~'):
            logger.debug(f"Skipping temporary file: {filename}")
            return

        with self.app.app_context():
            try:
                if self._is_analyzed_file(filepath):
                    self._handle_analyzed_file(filepath)
                elif self._is_result_file(filepath):
                    self._handle_result_file(filepath)
                else:
                    logger.debug(f"Skipping file: {filepath}")
            except Exception as e:
                logger.error(f"Error handling file {filepath}: {str(e)}")
                socketio.emit('error', {'message': f"Error handling file {filepath}: {str(e)}"})
                # raise e




    def _is_result_file(self, filepath):
        """Check if file is a result file but not an analyzed file"""
        return self.result_pattern.search(filepath)

    def _is_analyzed_file(self, filepath):
        """Check if file is an analyzed result file"""
        return bool(self.analyzed_pattern.search(filepath))

    def _extract_job_id(self, filepath):
        """Extract job ID from filepath or directory name"""
        # Try directory name first
        dir_path = os.path.dirname(filepath)
        dir_name = os.path.basename(dir_path)

        for name in [dir_name, os.path.basename(filepath)]:
            match = self.job_pattern.search(name)
            if match:
                return int(match.group(1))
        return None

    def _handle_result_file(self, filepath):
        """Handle new result file creation"""

        logger.debug(f"Handling new result file: {filepath}")
        job_id = self._extract_job_id(filepath)
        if not job_id:
            logger.warning(f"Could not extract job ID from {filepath}")
            return

        existing = ResultFile.query.filter_by(job_id=self._extract_job_id(filepath),
                                              filename=os.path.basename(filepath)
                                              ).first()
        if existing:
            logger.info(f"File {filepath} already exists in the database")
            return

        job = CalculationJob.query.get(job_id)
        if not job:
            logger.warning(f"Job {job_id} not found for file {filepath}")
            return

        existing_file = ResultFile.query.filter_by(filename=os.path.basename(filepath)).first()
        if existing_file:
            logger.info(f"File {filepath} already exists in the database")
            return

        file = ResultFile(
            job_id=job.id,
            filename=os.path.basename(filepath),
            filepath=filepath,
            analyzed=False
        )
        db.session.add(file)
        db.session.commit()
        # TODO: fix duplicate entry for file in database

        emit_new_file(file, job.id)

        # Auto-analyze if configured
        if self.app.config.get('AUTO_ANALYZE_FILES', False):
            from app.tasks.analysis import analyze_file
            analyze_file.delay(file.id)



    def _handle_analyzed_file(self, filepath):
        """Handle analyzed file creation"""
        logger.debug(f"Handling new analyzed file: {filepath}")

        # Get original filename by removing _analyzed suffix
        original_name = re.sub(r'\.analyzed$', self.app.config.get('RESULT_FILE_EXTENSION', r'.raw'),
                               os.path.basename(filepath))  # TODO: make it more general, get extensions from config

        # Find the original file record
        original_file = ResultFile.query.filter_by(
            filename=original_name
        ).first()

        logger.debug(f"Original name: {original_name}")
        logger.debug(f"Original file: {original_file}")
        if not original_file:
            logger.warning(
                f"Original file not found for analyzed file {filepath}")  # TODO: fix this, always returns this
            socketio.emit('error', {'message': f"Original file not found for analyzed file {filepath}"})
            return

        # Update original file record
        original_file.analyzed = True
        original_file.analysis_filepath = filepath
        db.session.commit()

        # Notify clients
        emit_file_analyzed(original_file, original_file.job_id)



def setup_file_watcher(app):
    """Set up and start the file system watcher"""
    watch_dir = app.config.get('RESULTS_DIRECTORY')  # default directory is ./results
    logger.info(f"Setting up file watcher for {watch_dir}")
    abs_watch_dir = os.path.abspath(watch_dir)

    os.makedirs(abs_watch_dir, exist_ok=True)

    # Create and start observer
    event_handler = ResultFileHandler(app)

    if os.name == 'posix':  # Linux or MacOS
        logging.warning("Posix OS detected, using polling observer")
        from watchdog.observers.polling import PollingObserver as Observer
        observer = Observer(timeout=1.0)
    else:
        logging.warning("Windows OS detected, using regular observer")
        from watchdog.observers import Observer
        observer = Observer()

    observer.schedule(event_handler, watch_dir, recursive=True)

    thread = threading.Thread(target=observer.start, daemon=True)
    thread.start()

    # Store observer reference
    app.file_observer = observer

    def cleanup():
        observer.stop()
        observer.join()

    import atexit
    atexit.register(cleanup)

    return observer