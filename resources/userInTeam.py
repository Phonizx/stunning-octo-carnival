#user can choose multi teams, can delete from a team
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


teamParams = reqparse.RequestParser()
teamParams.add_argument('teamName',type=str,location='json',help='Team name',required=True) 



class userInTeam_view(Resource):
    @jwt_required
    def get(self):  
        try:
            userTest = get_jwt_identity() 
            userInTeam = user.query.filter_by(username=userTest).first()
            if(userInTeam is None):
                raise UserNotExist
            userRelation = rel_team_user.query.filter_by(id_user=userInTeam.id_user).all()
            if(userRelation is None):
                raise UserRelationNotExist
            relations = [] 
            for r in userRelation:
                relItem = {}
                relItem["id_rel"] = r.id_team
                relItem["id_user"] = r.id_user
                relItem["id_team"] = r.id_team
                relItem["teamName"] = getTeamNameFromId(r.id_team) 
                relItem["id_role"] = r.id_role
                relItem["role"] = getRoleNameById(r.id_role)
                relations.append(relItem)
            return jsonify({"state" : 200, "teams" : relations})
        except UserRelationNotExist as e:
            return jsonify({'state' : 404, 'msg' : "User relationships doesn't exists"})
        except UserNotExist as e:
            return jsonify({'state' : 404, 'msg' : "User doesn't exist"}) 
        except Exception as e:
            return jsonify({'state' : 500, 'msg' : str(e)}) 
        
    
    @jwt_required
    def put(self): #user can put a simple relation with is team 
        try:
            userTest = get_jwt_identity()
            userInTeam = user.query.filter_by(username=userTest).first()
            args = teamParams.parse_args()
            if(args['teamName'] is not None): 
                teamName = args['teamName']
                if(existTeam(teamName)):
                    grubTeam = workTeam.query.filter_by(teamName=teamName).first()
                    newRelUserTeam = rel_team_user(user=userInTeam.id_user,team=grubTeam.id_team)
                    return jsonify({'state' : 200})
                else:
                    return jsonify({'state' : 404})
            else:
                return jsonify({'state' : 400})
        except Exception as e:
            return jsonify({'state' : 500, 'msg' : str(e)})

    @jwt_required
    def delete(self): #user can delete a simple relation with is team 
        try:
            userTest = get_jwt_identity()
            userInTeam = user.query.filter_by(username=userTest).first()
            args = teamParams.parse_args()
            if(args['teamName'] is not None): 
                teamName = args['teamName']
                if(existTeam(teamName)):
                    grubTeam = workTeam.query.filter_by(teamName=teamName).first()
                    lookForRel = rel_team_user.query.filter_by(id_user=userInTeam.id_user,id_team=grubTeam.id_team).first()
                    lookForRel.deleteRel()
                    return jsonify({'state' : 200})
                else:
                    return jsonify({'state' : 403})
            else:
                return jsonify({'state' : 400})
        except Exception as e:
            return jsonify({'state' : 500, 'msg' : str(e)})