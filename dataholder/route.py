from flask import render_template, url_for, request, jsonify
from dataholder import app

members = [
    {"name": "John Doe", "gender": "Male", "age": 30, "Phone No:": "08063136532"},
    {"name": "Jane Smith", "gender": "Female",
        "age": 25, "Phone No:": "08063136532"},
    {"name": "Alice Johnson", "gender": "female",
        "age": 28, "Phone No:": "08063136532"},
    {"name": "Johnson Dil", "gender": "Male",
        "age": 40, "Phone No:": "08063136532"},
    {"name": "Job David", "gender": "Male", "age": 55, "Phone No:": "08063136532"},
    {"name": "John Dave", "gender": "Male", "age": 30, "Phone No:": "08063136532"},
    {"name": "Sandra Bush", "gender": "Female",
        "age": 35, "Phone No:": "08063136532"}
]

# Read all data


@app.route('/api/members', methods=['GET'])
def get_members():
    return {"members": members}


# return a single member


@app.route('/api/members/<int:member_id>', methods=['GET'])
def get_member(member_id):
    if 0 <= member_id < len(members):
        return {"member": members[member_id]}
    else:
        return {"error": "Member not found"}, 404


# Create a new member
@app.route('/api/members', methods=['POST'])
def create_member():
    new_member = request.get_json()
    members.append(new_member)
    return {"message": "Member created successfully"}, 201


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
