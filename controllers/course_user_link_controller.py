from flask import Flask, jsonify, make_response, request
from model.associations import course_user_link
from model.base import db
from model.course_user_link import CourseUserLink as UserRecord

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../../SQLite_DB.sqlite'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Redwo0d$@127.0.0.1:3306/webadvisor_reboot'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

def create_tables():
    with app.app_context():
        db.create_all()

# --- CRUD Operations ---

# Read all user/course records (GET)
@app.route('/userrecord', methods=['GET'])
def get_records():
    records = UserRecord.query.all()
    return make_response(jsonify([course_user_link.json() for record in records]), 200)

# Read a single record by user ID (GET)
@app.route('/userrecord/<int:user_id>', methods=['GET'])
def get_record(user_id):
    record = UserRecord.query.get_or_404(user_id)
    return make_response(jsonify({'record': course_user_link.json()}), 200)

# Update a record by user ID (PUT/PATCH)
@app.route('/userrecord/<int:user_id>', methods=['PUT'])
def update_userrecord(user_id):
    userrecord = UserRecord.query.get_or_404(user_id)
    data = request.get_json()

    userrecord.user_id = data.get('user_id', userrecord.user_id)
    userrecord.course_id = data.get('course_id', userrecord.course_id)
    # This might have issues later...
    db.session.commit()
    return make_response(jsonify({'message': 'user record updated', 'userrecord': userrecord.json()}), 200)

# Delete a user record by ID (DELETE)
@app.route('/userrecord/<int:user_id>', methods=['DELETE'])
def delete_userrecord(user_id):
    userrecord = UserRecord.query.get_or_404(user_id)
    db.session.delete(userrecord)
    db.session.commit()
    return make_response(jsonify({'message': 'user record deleted'}), 200)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)