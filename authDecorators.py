from functools import wraps
from flask_restful import abort
from model import user

from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    jwt_refresh_token_required, create_refresh_token,
    get_jwt_identity
)


def checkAuth(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        tester = user.query.filter_by(username=get_jwt_identity()).first()
        if(tester.isAuth()):
            return func(*args, **kwargs)
        return abort(403)
    return wrapper

def checkIsSuperAdmin(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        tester = user.query.filter_by(username=get_jwt_identity()).first()
        if(tester.isSuperAdmin()):
            return func(*args, **kwargs)
        return abort(403)
    return wrapper