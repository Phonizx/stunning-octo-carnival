
from flask import Flask, request,jsonify,make_response
from flask_restful import Resource, Api,reqparse,marshal_with,fields

from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    jwt_refresh_token_required, create_refresh_token,
    get_jwt_identity
)

from config import jwt
from model import workTeam,user,rel_team_user

from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    jwt_refresh_token_required, create_refresh_token,
    get_jwt_identity
)
from utils.modelUtils import existTeam,getTeamNameFromId,getRoleNameById
from utils.customException import * 
from authDecorators import checkIsSuperAdmin
    

patcher = reqparse.RequestParser()
patcher.add_argument('user',type=str,location='json',help='Role User',required=True)
patcher.add_argument('teamName',type=str,location='json',help='Role User',required=True)

#user system handler by super admin 

class adminUsers_view(Resource):
    @jwt_required
    @checkIsSuperAdmin
    def get(self):
        try:
            userList = [] 
            getAllUsers = user.query.all()
            for ut in getAllUsers:
                userItem = {}
                userItem['id_user'] = ut.id_user 
                userItem['username'] = ut.username 
                userItem['role'] = ut.getRoleName()
                userItem['teams'] = [] #team List
                utRelation = rel_team_user.query.filter_by(id_user=ut.id_user).all()
                if(utRelation is not None):
                    for r in utRelation:
                        relItem = {}
                        relItem["id_rel"] = r.id_team
                        relItem["id_user"] = r.id_user
                        relItem["id_team"] = r.id_team
                        relItem["teamName"] = getTeamNameFromId(r.id_team) 
                        relItem["id_role"] = r.id_role
                        relItem["role"] = getRoleNameById(r.id_role)
                        userItem['teams'].append(relItem)
                userList.append(userItem)
            return jsonify({"state" : 200, "users" : userList})
        except Exception as e:
            return jsonify({"state" : 200, "msg" : str(e)})

            