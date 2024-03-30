from flask import request,jsonify  
from config import app,db
from models import Employee

@app.route("/get_employees",methods=["GET"])
def get_employees():
    employees = Employee.query.all()
    json_employess = list(map(lambda x:x.to_json(),employees))
    return jsonify({"employess":json_employess})


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)