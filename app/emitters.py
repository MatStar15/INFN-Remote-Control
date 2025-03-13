from . import socketio, get_socketio
import logging

logger = logging.getLogger(__name__)

def emit_job_update(job):
    external_socketio = get_socketio()
    external_socketio.emit('job_update',
                           {'job': job.to_dict()})
    logger.debug(f"Emitted job update for job {job.id} to all clients")


def emit_new_file(file, job_id):
    external_socketio = get_socketio()
    external_socketio.emit('new_file',
                 {'file': file.to_dict(), 'job_id': job_id})
    logger.debug(f"Emitted new file {file.filename} for job {job_id} to all clients")

def emit_file_analyzed(file, job_id):
    external_socketio = get_socketio()
    external_socketio.emit('file_analyzed',
                 {'file': file.to_dict(), 'job_id': job_id})
    logger.debug(f"Emitted file analyzed ( {file.filename} ) for job {job_id} to all clients")

