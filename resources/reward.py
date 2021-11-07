from flask import Flask, request,jsonify,make_response
from flask_restful import Resource, Api,reqparse,fields, marshal_with

from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    jwt_refresh_token_required, create_refresh_token,
    get_jwt_identity
)

from model import reward,user
from authDecorators import checkAuth
from utils.modelUtils import getUserFromId
from utils.customException import * 



putting = reqparse.RequestParser()
putting.add_argument('user_rewarded',type=str,location='json',help='role id',required=True) 
putting.add_argument('reward_weight',type=str,location='json',help='role id',required=True) 
putting.add_argument('reward_description',type=str,location='json',help='role description')


class reward_view(Resource):
    # get all rewards assignment by all coordinators
    def get(self): 
        try:
            rewardsByCoordinator = reward.query.all()
            rewardList = [] 
            for s_reward in  rewardsByCoordinator:
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
    
    @jwt_required
    @checkAuth
    def put(self):  
        try:
            userTest = get_jwt_identity() #'giovandimeo'
            args = putting.parse_args()
            coordinator = user.query.filter_by(username=userTest).first()
            userRewarded = user.query.filter_by(username=args['user_rewarded']).first() 
            if(userRewarded is None):
                raise UserNotExist
            newReward = reward(coordinator.id_user, userRewarded.id_user, args['reward_weight'], args['reward_description'])
            return jsonify({'state' : 200}) 
        except UserNotExist as e:
            return jsonify({'state' : 404, 'msg' : "User rewarded doesn't exist"}) 
        except Exception as e:
            return jsonify({'state' : 500, 'msg' : str(e)}) 

    
    @jwt_required
    @checkAuth
    def patch(self,id): #edit an exists reward 
        try:
            userTest = get_jwt_identity()
            coordinator = user.query.filter_by(username=userTest).first()
            args = putting.parse_args()
            editReward = reward.query.filter_by(id_reward=id).first()
            
            if(editReward is None):
                raise RewardNotExist
            if(args['user_rewarded'] is not None):
                userCatcher = user.query.filter_by(username=args['user_rewarded']).first()
                editReward.changeUserRewarded(userCatcher.id_user)
            
            if(args['reward_weight'] is not None):
                editReward.setWeight(args['reward_weight'])
            
            if(args['reward_description'] is not None):
                editReward.setRewardDescription(args['reward_description'])
            
            editReward.changeCoordinator(coordinator.id_user)
            return jsonify({'state' : 200})
        except RewardNotExist as e: 
            return jsonify({'state' : 404, 'msg' : "Reward doesn't exist"}) 
        except Exception as e:
            return jsonify({'state' : 500, 'msg' : str(e)}) 

        
    @jwt_required
    @checkAuth
    def delete(self,id): #delete reward assigment by coordinator [in request]
        try: 
            delReward = reward.query.filter_by(id_reward=id).first()
            if(delReward is None):
                raise RewardNotExist
            delReward.deleteReward()
            return jsonify({'state' : 200})
        except RewardNotExist as e: 
            return jsonify({'state' : 404, 'msg' : "Reward doesn't exist"}) 
        except Exception as e:
            return jsonify({'state' : 500, 'msg' : str(e)}) 