from model import user,workTeam,rel_team_user,role



def isValidUsername(username):
    if(len(username.strip()) == 0):
        return False
    lookFor = user.query.filter_by(username=username).first()
    if(lookFor is None):
        return True
    return False

def isUniqueTeamName(teamName):
    if(len(teamName.strip()) == 0):
        return False
    lookFor = workTeam.query.filter_by(teamName=teamName).first()
    if(lookFor is None):
        return True
    return False

def existTeam(teamName):
    if(len(teamName.strip()) == 0):
        return False
    lookFor = workTeam.query.filter_by(teamName=teamName).first()
    if(lookFor is not None):
        return True
    return False


def getTeamNameFromId(id):
    workQuery = workTeam.query.filter_by(id_team=id).first()
    return workQuery.teamName

def getUserFromId(id):
    userQuery = user.query.filter_by(id_user=id).first()
    return userQuery.username


def getAllUserTeams(userId):
    userTeams = rel_team_user.query.filter_by(id_user=userId).all()
    teams = [] 
    for uT in userTeams:
        teams.append(getTeamNameFromId(uT.id_team))
    return teams

def getRoleNameById(roleId):
    roleQuery = role.query.filter_by(id_role=roleId).first()
    return roleQuery.role
    