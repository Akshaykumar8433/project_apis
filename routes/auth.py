from flask import request
from flask_restx import Resource, fields
from swagger_config import api
from service.AuthenticateService import Authenticate
from common.customJwtDecorator import admin_jwt_required

auth = api.namespace("auth","Signup and Login Endpoint")

singup = api.model("Signup apis", {
    "email": fields.String(required = True,description="Email id of the user",help="Enter the email of type string."),
    "password": fields.String(required = True,description="Password of the user",help="Enter the password of type string."),
    "role": fields.String(required = True,description="Role of the user i.e(admin or user)",help="Enter the role of type string.")
})

login = api.model("Login apis", {
    "email": fields.String(required = True,description="Email id of the user",help="Enter the email of type string."),
    "password": fields.String(required = True,description="Password of the user",help="Enter the password of type string.")
})

delete_user = api.model("Delete user apis", {
    "email": fields.String(required = True,description="Email id of the user",help="Enter the email of type string.")
})

@auth.route("/signup")
class Signup(Resource):
    @api.doc(responses={ 200: 'OK'})
    @api.expect(singup)
    def post(self):
        return Authenticate().singupService(request.json)

@auth.route("/login")
class Login(Resource):
    @api.doc(responses={ 200: 'OK'})
    @api.expect(login)
    def post(self):
        return Authenticate().loginService(request.json)

@auth.route("/deleteuser")
class DeleteUser(Resource):
    @api.doc(responses={ 200: 'OK'})
    @api.expect(delete_user)
    @admin_jwt_required()
    def delete(self):
        return Authenticate().deleteUser(request.json)