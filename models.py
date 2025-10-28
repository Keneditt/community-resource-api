from flask_sqlalchemy import SQLAlchemy
import jwt
import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    city = db.Column(db.String(50))
    state = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    
    resources = db.relationship('Resource', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = jwt.encode({'password': password}, 'secret-key', algorithm='HS256')

    def check_password(self, password):
        try:
            decoded = jwt.decode(self.password_hash, 'secret-key', algorithms=['HS256'])
            return decoded['password'] == password
        except:
            return False

    def generate_token(self):
        payload = {
            'user_id': self.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7)
        }
        return jwt.encode(payload, 'secret-key', algorithm='HS256')

class Resource(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)  # food, housing, jobs, healthcare, education
    address = db.Column(db.String(200))
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))
    contact_phone = db.Column(db.String(20))
    contact_email = db.Column(db.String(120))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'category': self.category,
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'contact_phone': self.contact_phone,
            'contact_email': self.contact_email,
            'created_by': self.user.name,
            'created_at': self.created_at.isoformat()
        }