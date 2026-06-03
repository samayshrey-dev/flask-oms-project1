from app import db

class SupplierProfile(db.Model):
    __tablename__ = 'supplier_profiles'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), unique=True, nullable=False)
    
    pan_number = db.Column(db.String(50), nullable=True)
    gst_number = db.Column(db.String(50), nullable=True)
    bank_account = db.Column(db.String(50), nullable=True)
    ifsc_code = db.Column(db.String(20), nullable=True)
    address = db.Column(db.Text, nullable=True)
    verification_status = db.Column(db.Enum('Pending', 'Verified', name='verification_status_enum'), default='Pending')
    documents_submitted = db.Column(db.Boolean, default=False)

    user = db.relationship('User', backref=db.backref('supplier_profile', uselist=False, cascade='all, delete-orphan'))

    def __repr__(self):
        return f'<SupplierProfile user_id={self.user_id} status={self.verification_status}>'
