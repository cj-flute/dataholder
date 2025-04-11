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
    """Get a single member by ID"""
    with app.app_context():
        member = User_data.query.get(member_id)  # Query the database by ID
        # print(member.id)

        if member:
            return jsonify(member.to_dict())  # Serialize and return the member
        else:
            return {"error": "Member not found"}, 404


# Create a new member
@app.route('/api/members', methods=['POST'])
def create_member():
    # Create a new member
    new_member_data = request.get_json()
    print(new_member_data)

    # Validate the input data
    required_fields = ['name', 'username', 'age', 'gender', 'address',
                       'password', 'email', 'phone_no']
    missing_fields = [
        field for field in required_fields if field not in new_member_data]
    if missing_fields:
        return jsonify({"error": "Missing fields: " + ", ".join(missing_fields)}), 400

    with app.app_context():
        existing_member = User_data.query.filter_by(
            username=new_member_data['username']).first()
        if existing_member:
            return jsonify({"error": "Username already exists"}), 400
        existing_email = User_data.query.filter_by(
            email=new_member_data['email']).first()
        if existing_email:
            return jsonify({"error": "Email already exists"}), 400
        existing_phone_no = User_data.query.filter_by(
            phone_no=new_member_data['phone_no']).first()
        if existing_phone_no:
            return jsonify({"error": "Phone number already exists"}), 400
        # Check if the member already exists in the list
        for member in members:
            if member.username == new_member_data['username']:
                return jsonify({"error": "M ember already exists"}), 400
        # If the member does not exist, create a new one
        # and add it to the list
        # Create a new User_data object and add it to the database
        # and the list

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
        members.append(new_member)
        return jsonify({
            "message": "Member created successfully",
            "member": new_member.to_dict()
        }), 201


# Update a member
@app.route('/api/members/<int:member_id>', methods=['PUT'])
def update_member(member_id):
    with app.app_context():
        member = User_data.query.get(member_id)
        if not member:
            return {"error": "Member not found"}, 404
        print(member)

        # Update the member's data
        # Validate the input data

        updated_member_data = request.get_json()
        print(updated_member_data)

        # Update the member's fields if they are provided in the request
        if 'name' in updated_member_data:
            member.name = updated_member_data['name']
        if 'username' in updated_member_data:
            # Check if the new username already exists
            existing_member = User_data.query.filter_by(
                username=updated_member_data['username']).first()
            if existing_member and existing_member.id != member_id:
                return jsonify({"error": "Username already exists"}), 400
            member.username = updated_member_data['username']
        if 'age' in updated_member_data:
            member.age = updated_member_data['age']
        if 'gender' in updated_member_data:
            member.gender = updated_member_data['gender']
        if 'address' in updated_member_data:
            member.address = updated_member_data['address']
        if 'password' in updated_member_data:
            member.password = updated_member_data['password']
        if 'email' in updated_member_data:
            # Check if the new email already exists
            existing_email = User_data.query.filter_by(
                email=updated_member_data['email']).first()
            if existing_email and existing_email.id != member_id:
                return jsonify({"error": "Email already exists"}), 400
            member.email = updated_member_data['email']
        if 'phone_no' in updated_member_data:
            # Check if the new phone number already exists
            existing_phone_no = User_data.query.filter_by(
                phone_no=updated_member_data['phone_no']).first()
            if existing_phone_no and existing_phone_no.id != member_id:
                return jsonify({"error": "Phone number already exists"}), 400
            member.phone_no = updated_member_data['phone_no']

        # Commit the changes to the database
        db.session.commit()

        return jsonify({
            "message": "Member updated successfully",
            "member": member.to_dict()
        }), 200


# Delete a member
@app.route('/api/members/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    with app.app_context():
        member = User_data.query.get(member_id)
        if not member:
            return {"error": "Member not found"}, 404
        print(member)

        # Delete the member from the database
        db.session.delete(member)
        db.session.commit()

        # Optionally, remove the member from the in-memory list if used
        global members
        members = [m for m in members if m.id != member_id]

        return jsonify({"message": "Member deleted successfully"}), 200


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html')
