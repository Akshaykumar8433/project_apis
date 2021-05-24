from flask import jsonify
from dbconnect import dbsession
from common.StatusCode import StatusCode, Done
from modules.users import Users
from dataclasses import asdict
from common.Validatefunction import validateParamsFromCheckList
from flask_jwt_extended import create_access_token

class Authenticate():
    def singupService(self,request_body):
        try:
            request_body = validateParamsFromCheckList(request_body,{"email":(str),"password":(str),"role":(str)})

            user_details = self.userDetails(request_body)
            if user_details:
                raise Exception("user_exist")
            
            user = Users(request_body.get("email"),request_body.get("password"),request_body.get("role"))

            dbsession.add(user)
            dbsession.commit()

            return Done(None,message="Successfully Register")
        except Exception as e:
            dbsession.rollback()
            return StatusCode(({False:str(e),True:e.args[0]})[len(e.args)>0])
        finally:
            dbsession.close()

    def loginService(self,request_body):
        try:
            request_body = validateParamsFromCheckList(request_body,{"email":(str),"password":(str)})

            user_details = self.userDetails(request_body)
            if not user_details:
                raise Exception("not_exist")
            elif user_details.get_password() == request_body.get("password"):
                token = create_access_token(identity=user_details.get_email(),additional_claims={"role":user_details.get_role()})
                return Done({"access_token":token})
            else:
                raise Exception("wrong_password")
        except Exception as e:
            return StatusCode(({False:str(e),True:e.args[0]})[len(e.args)>0])

    def userDetails(self,request_body):
        user_details = dbsession.query(Users).filter(Users.email == request_body.get("email")).first()
        dbsession.close()
        return user_details

    def deleteUser(self,request_body):
        try:
            delete_user = dbsession.query(Users).filter(Users.email == request_body.get("email")).delete()
            dbsession.commit()
            if delete_user == 1:
                return Done(None, "Deleted")
            else:
                return StatusCode("not_found","User not found")
        except Exception as e:
            dbsession.rollback()
            return StatusCode(({False:str(e),True:e.args[0]})[len(e.args)>0])
        finally:
            dbsession.close()