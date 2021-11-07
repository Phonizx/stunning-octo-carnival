from flask import Flask, request,jsonify,make_response
from flask_restful import Resource, Api,reqparse,marshal_with,fields

from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    jwt_refresh_token_required, create_refresh_token,
    get_jwt_identity
)

from config import jwt
from model import workTeam
from utils.modelUtils import isUniqueTeamName,existTeam
from authDecorators import checkIsSuperAdmin

resource_fields = {
    'id_team': fields.Integer,
    'teamName': fields.String,
}

teamParams = reqparse.RequestParser()
teamParams.add_argument('teamName',type=str,location='json',help='new team name',required=True) 
teamParams.add_argument('newTeamName',type=str,location='json',help='new edit team name') 


class workTeam_view(Resource):
    @jwt_required
    @checkIsSuperAdmin
    def get(self):
        try: 
            allTeam = workTeam.query.all()
            teamsList = [] 
            for team in allTeam:
                t = {}
                t["id_team"] = team.id_team
                t["teamName"] = team.teamName
                teamsList.append(t)
            return jsonify({"state" : 200,"teams" : teamsList})
        except Exception as e:
            return jsonify({'state' : 500, 'msg' : str(e)}) 
    
    @jwt_required
    @checkIsSuperAdmin
    def put(self): #put new team super admin only
        try:
            args = teamParams.parse_args()
            if(args['teamName'] is not None): 
                teamName = args['teamName']
                if(isUniqueTeamName(teamName)):
                    newTeam = workTeam(args['teamName'])
                    return jsonify({'state' : 200})
                else:
                    return jsonify({'state' : 403})
            else:
                return jsonify({'state' : 400})
        except Exception as e:
            return jsonify({'state' : 500, 'msg' : str(e)}) 
    
    @jwt_required
    @checkIsSuperAdmin
    def delete(self): #delete team super admin only 
        try:
            args = teamParams.parse_args()
            if(args['teamName'] is not None):
                teamName = args['teamName']
                if(existTeam(teamName)):
                    deleteTeam = workTeam.query.filter_by(teamName=args['teamName']).first()
                    deleteTeam.deleteTeam()
                    return jsonify({'state' : 200})
                else:
                    return jsonify({'state' : 404})
            else:
                return jsonify({'state' : 400})
        except Exception as e:
            return jsonify({'state' : 500, 'msg' : str(e)}) 

    @jwt_required
    @checkIsSuperAdmin
    def patch(self): #edit team name only super admin only 
        try:
            args = teamParams.parse_args()
            if(args['teamName'] is not None):
                teamName = args['teamName']
                if(existTeam(teamName)):
                    if(isUniqueTeamName(args['newTeamName'])):
                        editTeam = workTeam.query.filter_by(teamName=teamName).first()
                        editTeam.editTeamName(args['newTeamName'])
                        return jsonify({'state' : 200})
                    else:
                        return jsonify({'state' : 500, "msg" : "TeamName already exist"})
                else:
                    return jsonify({'state' : 404})
            else:
                return jsonify({'state' : 400})
        except Exception as e:
            return jsonify({'state' : 500, 'msg' : str(e)}) 