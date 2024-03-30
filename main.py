from flask import request,jsonify  
from config import app,db
from models import Employee

@app.route('/')
def hello_world():
	return 'Welcome to employ management'

# Get all employess
@app.route("/get_employees",methods=["GET"])
def get_employees():
    employees = Employee.query.all()
    json_employess = list(map(lambda x:x.to_json(),employees))
    return jsonify({"employees":json_employess})

#Create employess
@app.route("/create_employee",methods=["POST"])
def create_employee():
    name = request.json.get("name")
    email = request.json.get("email")
    designation = request.json.get("designation")

    if not name or not email or not designation:
        return (jsonify({"message":"Must include name,email,designation"}),400)
    
    new_employee = Employee(name=name,email=email,designation=designation)

    try:
        db.session.add(new_employee)
        db.session.commit()
    except Exception as e:
        return (jsonify({"message":str(e)}),400)
    
    return (jsonify({"message":"Employee Created"}))


#Update employess
@app.route("/update_employee/<int:emp_id>",methods=["PATCH"])
def update_employee(emp_id):
    employee = Employee.query.get(emp_id)

    if not employee:
        return (jsonify({"message":"Employee details not found"}),404)
    data = request.json
    #console.log(data)
    employee.name = data.get("name",employee.name)
    employee.email = data.get("email",employee.email)
    employee.designation = data.get("designation",employee.designation)

    db.session.commit()
    return (jsonify({"message":"Employee details updated"}),200 )


#Delete employess
@app.route("/delete_employee/<int:emp_id>",methods=["DELETE"])
def delete_employee(emp_id):
    empployee = Employee.query.get(emp_id)

    if not empployee:
        return (jsonify({"message":"Employee details not found"}),404)
    
    db.session.delete(empployee)
    db.session.commit()

    return (jsonify({"message":"Employee deleted"}),200)






if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)