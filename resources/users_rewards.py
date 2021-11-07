from flask import Flask, request,jsonify,make_response
from flask_restful import Resource, Api,reqparse

from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    jwt_refresh_token_required, create_refresh_token,
    get_jwt_identity
)

from config import jwt
from model import user,reward
from utils.modelUtils import isValidUsername,getUserFromId
from utils.customException import * 


 

class userRewards_view(Resource):
    @jwt_required
    def get(self):
        try:
            userTest = get_jwt_identity()
            userRewarded = user.query.filter_by(username=userTest).first()
            if(userRewarded is None):
                raise UserNotExist
            rewardsOfUser = reward.query.filter_by(user_f=userRewarded.id_user).all()
            rewardList = [] 
            for s_reward in  rewardsOfUser:
                item = {}
                item['id_reward'] = s_reward.id_reward
                item['coordinator'] = getUserFromId(s_reward.coordinator_f)
                item['reward_weight'] = s_reward.reward_weight
                item['reward_description'] = s_reward.reward_description
                item['user_rewarded'] =  getUserFromId(s_reward.user_f)
                item['date'] = str(s_reward.date_reward)
                rewardList.append(item)
            return jsonify({"state" : 200, "rewards" : rewardList})
        except Exception as e: 
            return jsonify({'state' : 500, 'msg' : str(e)}) 