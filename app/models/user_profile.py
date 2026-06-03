from app import db

class UserProfile(db.Model):
    __tablename__ = 'user_profiles'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), unique=True, nullable=False)
    
    # Personal Info
    phone = db.Column(db.String(20), nullable=True)
    
    # Address
    address_line1 = db.Column(db.String(255), nullable=True)
    address_line2 = db.Column(db.String(255), nullable=True)
    city = db.Column(db.String(100), nullable=True)
    state = db.Column(db.String(100), nullable=True)
    zip_code = db.Column(db.String(20), nullable=True)
    country = db.Column(db.String(100), nullable=True)

    user = db.relationship('User', backref=db.backref('profile', uselist=False, cascade='all, delete-orphan'))

    def __repr__(self):
        return f'<UserProfile user_id={self.user_id}>'
