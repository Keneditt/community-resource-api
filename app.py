from flask import Flask, request, jsonify
from models import db, User, Resource
from auth import token_required
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///resources.db'
app.config['SECRET_KEY'] = 'your-secret-key-here'

db.init_app(app)

# Create tables
with app.app_context():
    db.create_all()

# Auth routes
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    
    # Check if user exists
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'User already exists'}), 400
    
    # Create new user
    user = User(
        name=data['name'],
        email=data['email'],
        city=data.get('city', ''),
        state=data.get('state', '')
    )
    user.set_password(data['password'])
    
    db.session.add(user)
    db.session.commit()
    
    token = user.generate_token()
    return jsonify({'token': token, 'user_id': user.id})

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(email=data['email']).first()
    
    if user and user.check_password(data['password']):
        token = user.generate_token()
        return jsonify({'token': token, 'user_id': user.id})
    
    return jsonify({'error': 'Invalid credentials'}), 401

# Resource routes
@app.route('/resources', methods=['GET'])
def get_resources():
    category = request.args.get('category')
    city = request.args.get('city')
    
    query = Resource.query.filter_by(is_active=True)
    
    if category:
        query = query.filter_by(category=category)
    if city:
        query = query.filter(Resource.city.ilike(f'%{city}%'))
    
    resources = query.all()
    return jsonify([r.to_dict() for r in resources])

@app.route('/resources', methods=['POST'])
@token_required
def create_resource(current_user):
    data = request.json
    
    resource = Resource(
        title=data['name'],
        description=data['description'],
        category=data['category'],
        address=data.get('address', ''),
        city=data.get('city', ''),
        state=data.get('state', ''),
        contact_phone=data.get('contact_phone', ''),
        contact_email=data.get('contact_email', ''),
        user_id=current_user.id
    )
    
    db.session.add(resource)
    db.session.commit()
    
    return jsonify(resource.to_dict())

@app.route('/resources/<int:resource_id>', methods=['DELETE'])
@token_required
def delete_resource(current_user, resource_id):
    resource = Resource.query.get_or_404(resource_id)
    
    if resource.user_id != current_user.id:
        return jsonify({'error': 'Not authorized'}), 403
    
    db.session.delete(resource)
    db.session.commit()
    
    return jsonify({'message': 'Resource deleted'})

@app.route('/my-resources', methods=['GET'])
@token_required
def get_my_resources(current_user):
    resources = Resource.query.filter_by(user_id=current_user.id).all()
    return jsonify([r.to_dict() for r in resources])

if __name__ == '__main__':
    app.run(debug=True)