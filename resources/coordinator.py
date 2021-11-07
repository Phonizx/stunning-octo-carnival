from flask import Flask, request,jsonify,make_response
from flask_restful import Resource, Api,reqparse,fields, marshal_with

from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    jwt_refresh_token_required, create_refresh_token,
    get_jwt_identity
)

from model import reward,user,rel_team_user
from authDecorators import checkAuth
from utils.modelUtils import getUserFromId
from utils.customException import * 



class coordinatorUsers_view(Resource):
    @jwt_required
    @checkAuth
    def get(self):
        try:
            #get all user of my team 
            userTest = get_jwt_identity()
            userQuery = user.query.filter_by(username=userTest).first()
             
            #get team where user its coordinator 
            relQuery = rel_team_user.query.filter_by(id_user=userQuery.id_user,id_role=userQuery.fk_role).first()
            if(relQuery is None):
                return jsonify({'state' : 404})

            teamWhereCoordinator = relQuery.id_team
            #get all user of team where its coordinator 
            getAllsFromTeam = rel_team_user.query.filter_by(id_team=teamWhereCoordinator).all()
            teamUsers = [] 
            for userItem in getAllsFromTeam:
                teamUsers.append(getUserFromId(userItem.id_user))
            return jsonify({'state' : 200,"users" : teamUsers}) 
        except Exception as e:
            return jsonify({'state' : 500, 'msg' : str(e)}) 

    