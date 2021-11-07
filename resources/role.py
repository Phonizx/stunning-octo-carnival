from flask import Flask, request,jsonify,make_response
from flask_restful import Resource, Api,reqparse,fields, marshal_with

from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    jwt_refresh_token_required, create_refresh_token,
    get_jwt_identity
)

from model import role
from authDecorators import checkIsSuperAdmin



getter = reqparse.RequestParser()
getter.add_argument('id',type=str,location='args',help='role id',required=True)


putting = reqparse.RequestParser()
putting.add_argument('role',type=str,location='json',help='role id',required=True) 
putting.add_argument('role_description',type=str,location='json',help='role description')



resource_fields = {
    'id_role': fields.Integer,
    'role': fields.String,
    'role_description': fields.String,
}


class role_view(Resource):
    @jwt_required
    @checkIsSuperAdmin
    @marshal_with(resource_fields)
    def get(self): #show all roles only super admin
        try:
            args = getter.parse_args()
            roleQuery = role.query.all()
            return roleQuery
        except Exception as e:
            return jsonify({'state' : 500, 'msg' : str(e)})

    @jwt_required
    @checkIsSuperAdmin
    def put(self): #put new role only super admin 
        try:
            data = putting.parse_args()
            r = role(data['role'],data['role_description'])
            return 200
        except Exception as e:
            return jsonify({'state' : 500, 'msg' : str(e)})
    
    @jwt_required
    @checkIsSuperAdmin
    def delete(self): #delete role only super admin
        pass 