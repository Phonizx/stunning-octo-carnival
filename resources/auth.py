from model import login_user,user,tg_authorization
from utils.modelUtils import getAllUserTeams

from datetime import timedelta

from flask import Flask, request,jsonify,make_response
from flask_restful import Resource, Api,reqparse,fields, marshal_with
from werkzeug.security import generate_password_hash,check_password_hash

import json 
from hashids import Hashids

import datetime
from datetime import datetime 

hashids = Hashids(salt='precipitato a sattare in atto')

from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    jwt_refresh_token_required, create_refresh_token,
    get_jwt_identity
)

from utils.modelUtils import isValidUsername

#signup arguments 
putting = reqparse.RequestParser()
putting.add_argument('username',type=str,location='json',required=True) 
putting.add_argument('password',type=str,location='json',required=True)

putting.add_argument('question1',type=str,location='json')
putting.add_argument('answer1',type=str,location='json')

putting.add_argument('question2',type=str,location='json')
putting.add_argument('answer2',type=str,location='json')

#login arguments
posting = reqparse.RequestParser()
posting.add_argument('username',type=str,location='json',required=True) 
posting.add_argument('password',type=str,location='json',required=True)



class auth_view(Resource):
    def put(self): # signup 
        try:
            data = putting.parse_args()
            if(isValidUsername(data['username'])):
                hashed_password = generate_password_hash(data['password'], method='sha256')
                signup = login_user(username=data['username'], user_password=hashed_password,
                            fst_question=data['question1'],fst_answer=data['answer1'],
                            scd_question=data['question2'],scd_answer=data['answer2'])
                
                seed = datetime.now()
                hashid = hashids.encode(1,seed.month,seed.day,seed.hour,seed.second)
                
                
                newUser = user(username=data['username'],token=hashid)
                expires = timedelta(minutes=30)
                access = {
                        'access_token': create_access_token(identity=str(data['username']),expires_delta=expires),
                        'refresh_token' : create_refresh_token(identity=str(data['username']),expires_delta=expires)
                }

                tg_user = tg_authorization(hash=hashid,username=data['username'])

                return jsonify({"state" : 200, "access" : access, "profileObj" : {"username" : newUser.username,
                            "role" : newUser.getRoleName(), "role_id" : newUser.fk_role,"tg" : "https://tg.me/handlerconvbot?user={}".format(tg_user.token)}})
            else:
                return jsonify({'state' : 500, 'msg' : "Username already exist"})
        except Exception as e:
            return jsonify({'state' : 500, 'msg' : str(e)})

    def post(self): #login 
        try:
            data = posting.parse_args()
            user_logging = login_user.query.filter_by(user=data['username']).first()  
            if(check_password_hash(user_logging.user_password, data['password'])):
                user_logged = user.query.filter_by(username=user_logging.user).first()  
                #todo add token expired
                access = {
                    'access_token': create_access_token(identity=user_logged.username),
                    'refresh_token' : create_refresh_token(identity=user_logged.username)
                }   
                tg_deep = tg_authorization.query.filter_by(username=user_logging.user).first()  
                teams = getAllUserTeams(user_logged.id_user)
                return jsonify({"state" : 200, "access" : access, "profileObj" : {"username" : user_logged.username,"teams" : teams,
                        "role" : user_logged.getRoleName(), "role_id" : user_logged.fk_role,"tg" : "https://tg.me/handlerconvbot?user={}".format(tg_deep.token)}})        
            else:
                return make_response('could not verify',  401, {'WWW.Authentication': 'Basic realm: "login required"'})
        except Exception as e:
            return jsonify({'state' : 500, 'msg' : str(e)})
