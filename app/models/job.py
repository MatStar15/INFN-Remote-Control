from app import db
from datetime import datetime




class CalculationJob(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(20), default='pending')  # pending, running, completed, failed, stopped
    parameters = db.Column(db.JSON)
    started_at = db.Column(db.DateTime, default=datetime.utcnow())
    completed_at = db.Column(db.DateTime, nullable=True)
    files = db.relationship('ResultFile', backref='job', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'status': self.status,
            'parameters': self.parameters,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'file_count': len(self.files)
        }


class ResultFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('calculation_job.id'))
    filename = db.Column(db.String(255))
    filepath = db.Column(db.String(255), unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    analyzed = db.Column(db.Boolean, default=False)
    analysis_filepath = db.Column(db.String(255), nullable=True)

    __table_args__ = (
        db.UniqueConstraint('job_id', 'filename', name='unique_job_filename'),
    )

    def to_dict(self):
        return {
            'id': self.id,
            'filename': self.filename,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'analyzed': self.analyzed,
            'job_id': self.job_id
        }
