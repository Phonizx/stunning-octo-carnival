#public info of user query
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

from utils.modelUtils import getTeamNameFromId,getUserFromId
from model import user,reward,rel_team_user 



class publicUser_view(Resource):
    
    def get(self,username):
        try:
            userPayload = {}  
            pubUser = user.query.filter_by(username=username).first()
            rewardOf = reward.query.filter_by(user_f=pubUser.id_user).all()
            userTeam = rel_team_user.query.filter_by(id_user=pubUser.id_user).all()
            teamNames = []
            for uT in userTeam:
                teamNames.append(getTeamNameFromId(uT.id_team))
            rewardList = []
            for r in rewardOf:
                rewObj = {}
                rewObj["id_reward"] = r.id_reward
                rewObj["coordinator"] = getUserFromId(r.coordinator_f)
                rewObj["reward_weight"] = r.reward_weight
                rewObj["reward_description"] = r.reward_description
                rewObj["date_reward"] = str(r.date_reward)
                rewardList.append(rewObj)
            userPayload['username'] = pubUser.username
            userPayload['role'] = pubUser.getRoleName()
            userPayload['rewards'] = rewardList
            userPayload['teams'] = teamNames
            userPayload['state'] = 200
            return userPayload
        except Exception as e:
            return jsonify({'state' : 500, 'msg' : str(e)}) 
            

