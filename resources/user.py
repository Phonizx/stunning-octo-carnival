from flask import Flask, request,jsonify,make_response
from flask_restful import Resource, Api,reqparse

from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    jwt_refresh_token_required, create_refresh_token,
    get_jwt_identity
)

from config import jwt
from model import user
from utils.modelUtils import isValidUsername
from utils.customException import * 


patcher = reqparse.RequestParser()
patcher.add_argument('username',type=str,location='json',help='edit username') 



class user_view(Resource):
    @jwt_required
    def get(self): #private user info
        try:
            userTest = get_jwt_identity()
            getUser = user.query.filter_by(username=userTest).first()
            if(getUser is None):
                raise UserNotExist
            userPayload = {} 
            userPayload['state'] = 200
            userPayload['username'] = getUser.username
            userPayload['role'] = getUser.getRoleName()
            userPayload['tg'] = "https://tg.me/handlerconvbot?user={}".format(getUser.dl_token) 
            return userPayload
        except UserNotExist as e:
            return jsonify({'state' : 404, 'msg' : "User doesn't exist"}) 
        except Exception as e:
            return jsonify({'state' : 500, 'msg' : str(e)}) 


    @jwt_required
    def patch(self): #user update info 
        try:
            args = patcher.parse_args()
            userTest = get_jwt_identity()
            if(args["username"] is not None):
                editUsername = args['username'] 
                if(isValidUsername(editUsername)):
                    editUser = user.query.filter_by(username=userTest).first()
                    editUser.setUsername(editUsername)
                    return jsonify({'state' : 200})
                else:
                    return jsonify({'state' : 500,"msg" : "username already exist"})
            else:
                return jsonify({'state' : 400})
        except Exception as e:
            return jsonify({'state' : 500, 'msg' : str(e)}) 
    
    @jwt_required
    def delete(self): #delete user
        try:
            userTest = get_jwt_identity()
            deleteUser = user.query.filter_by(username=userTest).first()
            if(deleteUser is None):
                raise UserNotExist
            deleteUser.deleteAccount()
            return jsonify({'state' : 200})
        except UserNotExist as e:
            return jsonify({'state' : 404, 'msg' : "User doesn't exist"})
        except Exception as e:
            return jsonify({'state' : 500, 'msg' : str(e)}) 





