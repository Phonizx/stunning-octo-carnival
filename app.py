from flask import Flask, request,jsonify,make_response
from flask_restful import Resource, Api,reqparse
from config import app,jwt
from resources.user import user_view
from resources.role import role_view
from resources.auth import auth_view
from resources.workteam import workTeam_view
from resources.userInTeam import userInTeam_view
from resources.reward import reward_view
from resources.publicUser import publicUser_view
from resources.admin_coordinator import adminCoordinator_view
from resources.coordinator import coordinatorUsers_view
from resources.users_teams import userTeam_view
from resources.users_rewards import userRewards_view
from resources.admin_users import adminUsers_view


api = Api(app)

#User endpoint
api.add_resource(auth_view, '/v1/auth')
api.add_resource(user_view, '/v1/user')
api.add_resource(userInTeam_view, '/v1/user/team')
api.add_resource(userTeam_view, '/v1/user/team/show')
api.add_resource(userRewards_view, '/v1/user/reward')

#Admin endpoint 
api.add_resource(workTeam_view, '/v1/admin/team')
api.add_resource(adminUsers_view, '/v1/admin/users')
api.add_resource(adminCoordinator_view, '/v1/admin/coordinator')
api.add_resource(role_view, '/v1/admin/role')

#Coordinator endpoint
#handler user 
api.add_resource(coordinatorUsers_view, '/v1/coordinator/users')


#Reward endpoint
api.add_resource(reward_view, '/v1/reward','/v1/reward/<int:id>')


#Public user endpoint
api.add_resource(publicUser_view, '/v1/publicUser/<string:username>')


if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5050,debug=True,threaded=True)
    #app.run(debug=True)