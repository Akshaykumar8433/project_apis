from common.JsonResponse import JsonResponse
from flask import g

error_codes = {
    1401: ["type_mismatch"],
    1402: ["wrong_password"],
    1403: ["no_data","'NoneType' object is not iterable"],
    1404: ["not_empty","empty"],
    1405: ["not_exist"],
    1601: ["permission_denied"],
    1602: ["extension_not_allowed"],
    1202: ["user_exist"],
    1501: ["not_able_to_convert"],
    1502: ["type_is_not_exist"],
    1503: ["transfer_data_error","data_transfer"],
    1406: ["token_expired"],
    1407: ["(invalid_grant) Bad Request"],
    1504: ["check_connection","An error occurred while calling o37.load.\n","An error occurred while calling o74.load.\n"]
}

code_message = {
    1500: "Internal Sever Error!",
    1401: "Type Mismatch! Check the parameter and request body,required key pairs and their value format",
    1601: "Permission Denied",
    1402: "Wrong Password",
    1403: "Not Data",
    1405: "User not exist",
    1202: "User with same email id is already exist.",
    1502: "Type is not exist avaliable types are name,genre,imdbscore,director and popularity",
    1503: "Error occur while copying data",
    1602: "File Extension not allowed.Please Check the file extension.",
    1406: "Invalid Token.",
    1504: "Not Connected",
    1404: "Check one of the field is empty",
    1407: "Authentication link is expired"
}

def StatusCode(error,message=None,data=None):
    response = JsonResponse()
    for i in error_codes:
        if error in error_codes.get(i):
            response.set_status(i)
            response.set_message(({True:code_message.get(i),False:message})[message in (None,"")])
            response.set_data(data)
            g.response = response.returnResponse()
            return response.returnResponse()
    
    response.set_status(1500)
    response.set_message(({True:code_message.get(1500),False:message})[message in (None,"")])
    response.set_data(data)
    g.response = response.returnResponse()

    return g.response

def Done(data,message=None):
    response = JsonResponse()
    response.set_status(200)
    response.set_data(data)
    response.set_message(message)
    g.response = response.returnResponse()

    return g.response