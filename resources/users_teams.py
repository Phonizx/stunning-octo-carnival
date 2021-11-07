from flask import Flask, request,jsonify,make_response
from flask_restful import Resource, Api,reqparse

from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    jwt_refresh_token_required, create_refresh_token,
    get_jwt_identity
)

from config import jwt
from model import user,workTeam

from utils.modelUtils import isValidUsername
from utils.customException import * 



class userTeam_view(Resource):
    @jwt_required
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