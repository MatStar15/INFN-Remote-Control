from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from app.models.job import CalculationJob, ResultFile
from app import db, socketio
from app.emitters import *
import os, re, time, threading, logging

logger = logging.getLogger(__name__)


class ResultFileHandler(FileSystemEventHandler):
    def __init__(self, app):
        self.app = app

        # Patterns for file matching
        self.result_pattern = re.compile(app.config.get('RESULT_FILE_PATTERN', r'.*\.raw$'))
        self.analyzed_pattern = re.compile(app.config.get('ANALYZED_FILE_PATTERN', r'.*\.analyzed$'))
        self.job_pattern = re.compile(r'job_(\d+)')

        logger.debug(f"Result pattern: {self.result_pattern.pattern}")
        logger.debug(f"Analyzed pattern: {self.analyzed_pattern.pattern}")
        logger.debug(f"Job pattern: {self.job_pattern.pattern}")


    def on_created(self, event):
        if event.is_directory:
            return

        filepath = event.src_path
        filename = os.path.basename(filepath)


        logger.debug(f"New file created: {filename}")

        # Skip temporary files
        if filename.startswith('.') or filename.startswith('~'):
            logger.debug(f"Skipping temporary file: {filename}")
            return

        with self.app.app_context():
            try:
                if self._is_analyzed_file(filepath):
                    logger.debug(f"Handling analyzed file: {filepath}")
                    self._handle_analyzed_file(filepath)
                elif self._is_result_file(filepath):
                    logger.debug(f"Handling result file: {filepath}")
                    self._handle_result_file(filepath)
                else:
                    logger.info(f"Skipping file: {filepath}")
            except Exception as e:

                logger.error(f"Error handling file {filepath}: {str(e)}")


    def _is_result_file(self, filepath):
        """Check if file is a result file but not an analyzed file"""
        return (self.result_pattern.search(filepath) and
                not self.analyzed_pattern.search(filepath))

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
        logger.info(f"Handling new result file: {filepath}")
        job_id = self._extract_job_id(filepath)
        if not job_id:
            logger.warning(f"Could not extract job ID from {filepath}")
            return

        with db.session.begin():
            job = CalculationJob.query.get(job_id)
            if not job:
                logger.warning(f"Job {job_id} not found for file {filepath}")
                return

            existing_file = ResultFile.query.filter_by(filepath=filepath).with_for_update().first()
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
        # Get original filename by removing _analyzed suffix
        original_name = re.sub(r'\.analyzed$', '', os.path.basename(filepath))

        # Find the original file record
        original_file = ResultFile.query.filter(
            ResultFile.filename == original_name
        ).first()

        if not original_file:
            logger.warning(f"Original file not found for analyzed file {filepath}")
            return

        # Update original file record
        original_file.analyzed = True
        original_file.analysis_filepath = filepath
        db.session.commit()

        # Notify clients
        emit_file_analyzed(original_file, original_file.job_id)



def setup_file_watcher(app):
    """Set up and start the file system watcher"""
    watch_dir = app.config.get('RESULTS_DIRECTORY', './results')
    logger.info(f"Setting up file watcher for {watch_dir}")
    abs_watch_dir = os.path.abspath(watch_dir)

    os.makedirs(abs_watch_dir, exist_ok=True)

    # Create and start observer
    event_handler = ResultFileHandler(app)
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