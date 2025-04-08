from flask import render_template, url_for, request, jsonify
from dataholder import app, db
from dataholder.models import User_data

members = []
with app.app_context():
    if not members:
        db.create_all()
        members = User_data.query.all()
    else:
        print("No user in the database")


# Read all data


@app.route('/api/members', methods=['GET'])
def get_members():
    """Get all members"""
    serialized_members = [member.to_dict() for member in members]
    # serialized_members = [member.to_dict() for member in members]
    """ Convert the User_data directly JSON serializable by 
    formating into a dictionary that can be converted to JSON"""
    return jsonify(serialized_members)


# return a single member
@app.route('/api/members/<int:member_id>', methods=['GET'])
def get_member(member_id):
    if member_id >= 0 < len(members):
        return jsonify(members[member_id].to_dict())
    # return jsonify(members[member_id].to_dict())
    else:
        if member_id < 0:
            return {"error": "Member ID cannot be negative"}, 400
        if members_id > len(members):
            return {"error": "Member ID out of range"}, 400
        return {"error": "Member not found"}, 404


# Create a new member
@app.route('/api/members', methods=['POST'])
def create_member():
    new_member_data = request.get_json()
    new_member = User_data(
        name=new_member_data['name'],
        username=new_member_data['username'],
        age=new_member_data['age'],
        gender=new_member_data['gender'],
        address=new_member_data['address'],
        password=new_member_data['password'],
        email=new_member_data['email'],
        phone_no=new_member_data['phone_no']
    )
    db.session.add(new_member)
    db.session.commit()
    members.append(new_member_data)
    return ({"message": "Member created successfully"},
            jsonify(new_member.to_dict()), 201)

# Update a member


@app.route('/api/members/<int:member_id>', methods=['PUT'])
def update_member(member_id):
    if 0 <= member_id < len(members):
        updated_member = request.get_json()
        members[member_id] = updated_member
        return {"message": "Member updated successfully"}
    else:
        return {"error": "Member not found"}, 404


# Delete a member
@app.route('/api/members/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    if 0 <= member_id < len(members):
        members.pop(member_id)
        return {"message": "Member deleted successfully"}
    else:
        return {"error": "Member not found"}, 404


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html')
