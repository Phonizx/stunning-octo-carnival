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
from utils.modelUtils import existTeam
from utils.customException import * 
from authDecorators import checkIsSuperAdmin
    

patcher = reqparse.RequestParser()
patcher.add_argument('user',type=str,location='json',help='Role User',required=True)
patcher.add_argument('teamName',type=str,location='json',help='Role User',required=True)

#coordinator machine 
class adminCoordinator_view(Resource): 
    @jwt_required
    @checkIsSuperAdmin
    def put(self): #only super admin can edit role about relation ship 
        try:
            args = patcher.parse_args()
            if(args['user'] is None):
                raise KeyError
            if(args['teamName'] is None):
                raise KeyError
            userRel = user.query.filter_by(username=args['user']).first()

            if(userRel is None):
                raise UserNotExist 
            team = workTeam.query.filter_by(teamName=args['teamName']).first()
            if(team is None):
                raise TeamNotExist
            
            grubRel = rel_team_user.query.filter_by(id_user=userRel.id_user,id_team=team.id_team).first()
            if(grubRel is None):
                raise UserRelationNotExist
        
            grubRel.beCoordinator()
            return jsonify({'state' : 200})
        except UserRelationNotExist as e:
            return jsonify({'state' : 404, 'msg' : "User doesn't exist in team"})
        except KeyError as e:
            return jsonify({'state' : 400, 'msg' : "Bad request"})
        except Exception as e:
            print(str(e))
            return jsonify({'state' : 500, 'msg' : str(e)})
