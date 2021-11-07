
from sqlalchemy.orm import relationship,backref
import datetime
from config import db


class role(db.Model):
    __tablename__= 'userRole'
    id_role = db.Column(db.Integer,primary_key=True)
    role = db.Column(db.String())
    role_description = db.Column(db.String())

    def __init__(self,role,role_description):
        self.role = role
        self.role_description = role_description
        db.session.add(self)
        db.session.commit()


class workTeam(db.Model):
    __tablename__= 'workteam'
    id_team = db.Column(db.Integer,primary_key=True)
    teamName = db.Column(db.String())

    def __init__(self,teamName):
        self.teamName = teamName
        db.session.add(self)
        db.session.commit()

    def deleteTeam(self):
        db.session.delete(self)
        db.session.commit()

    def editTeamName(self,teamName):
        self.teamName = teamName
        db.session.commit()


class login_user(db.Model):
    __tablename__= 'login_user'
    user = db.Column(db.String(),primary_key=True)
    user_password = db.Column(db.String())
    fst_question = db.Column(db.String())
    fst_answer = db.Column(db.String()) 
    scd_question = db.Column(db.String())
    scd_answer = db.Column(db.String())
    joined = db.Column(db.DateTime(), default=datetime.datetime.utcnow)
    last_login = db.Column(db.DateTime(), default=datetime.datetime.utcnow)

    def __init__(self,username, user_password,fst_question,fst_answer,scd_question,scd_answer):
        self.user = username
        self.user_password = user_password
        self.fst_question = fst_question
        self.fst_answer = fst_answer
        self.scd_question = scd_question
        self.scd_answer = scd_answer
        self.joined = str(datetime.datetime.now())
        self.last_login = str(datetime.datetime.now()) 
        db.session.add(self)
        db.session.commit()


class user(db.Model):
    __tablename__= 'user'
    id_user = db.Column(db.Integer,primary_key=True)

    fk_role = db.Column(db.Integer, db.ForeignKey('userRole.id_role'),unique=True)
    role = relationship("role",backref=backref("userRole",cascade="all,delete"))

    username = db.Column(db.String())
    name_user = db.Column(db.String())
    surname = db.Column(db.String())
    dl_token = db.Column(db.String())

    def __init__(self,username,token):
        self.username = username
        self.fk_role = 3
        self.dl_token = token
        db.session.add(self)
        db.session.commit()
    
    def setUsername(self,username):
        self.username = username 
        db.session.commit()
    

    def deleteAccount(self):
        #delete user login 
        #delete in: reward,workteam, rel
        login = login_user.query.filter_by(user=self.username).first()
        db.session.delete(login)
        db.session.delete(self)
        db.session.commit()


    def getRoleName(self): 
        roleObj = role.query.filter_by(id_role=self.fk_role).first()
        return roleObj.role
    
    def isAuth(self):
        roleObj = role.query.filter_by(id_role=self.fk_role).first()
        if(roleObj.role == 'coordinator' or roleObj.role == 'super-admin'):
            return True
        return False

    def isSuperAdmin(self):
        roleObj = role.query.filter_by(id_role=self.fk_role).first()
        if(roleObj.role == 'super-admin'):
            return True
        return False


class tg_authorization(db.Model):
    __tablename__= 'tg_authorization'
    token = db.Column(db.String(),primary_key=True)
    user_token = db.Column(db.String())
    username = db.Column(db.String())
    #last_login

    def __init__(self,hash,username): 
        self.token = hash 
        self.username = username 

        db.session.add(self)
        db.session.commit()


class rel_team_user(db.Model): 
    __tablename__= 'rel_team_user'
    id_rel = db.Column(db.Integer,primary_key=True)
    
    id_user = db.Column(db.Integer, db.ForeignKey('user.id_user'),unique=True)
    user = relationship("user",backref=backref("user",cascade="all,delete"))

    id_team = db.Column(db.Integer, db.ForeignKey('workteam.id_team'),unique=True)
    team = relationship("workTeam",backref=backref("workTeam",cascade="all,delete"))


    id_role = db.Column(db.Integer, db.ForeignKey('userRole.id_role'),unique=True)
    role = relationship("role",backref=backref("roleInTeam",cascade="all,delete"))
    
    def __init__(self,user,team):
        self.id_user = user 
        self.id_team = team 
        self.id_role = 3 #member 
        db.session.add(self)
        db.session.commit()
        

    def deleteRel(self):
        db.session.delete(self)
        db.session.commit()
    
    def beCoordinator(self):
        self.id_role = 4
        db.session.commit()


class reward(db.Model):
    __tablename__= 'reward'
    
    id_reward = db.Column(db.Integer,primary_key=True)

    coordinator_f = db.Column(db.Integer, db.ForeignKey('user.id_user'),unique=True)
    #coordinator = relationship("user",backref=backref("rewardUser",cascade="all,delete"))
    
    user_f = db.Column(db.Integer, db.ForeignKey('user.id_user'),unique=True)
    #user = relationship("user",backref=backref("rewardUser",cascade="all,delete")) 
    
    rewardByCoordinator = relationship("user", foreign_keys=[coordinator_f])
    rewardForUser = relationship("user", foreign_keys=[user_f])


    reward_weight = db.Column(db.Integer)
    reward_description = db.Column(db.String())
    date_reward = db.Column(db.DateTime(), default=datetime.datetime.utcnow)

    def __init__(self,coordinator,user,reward_weight,reward_description):
        self.coordinator_f = coordinator 
        self.user_f = user 
        self.reward_weight = reward_weight
        self.reward_description = reward_description
        db.session.add(self)
        db.session.commit()

    def deleteReward(self):
        db.session.delete(self)
        db.session.commit()
    
    def setWeight(self,new_weight):
        self.reward_weight = new_weight
        db.session.commit()
    
    def setRewardDescription(self,new_description):
        self.reward_description = new_description
        db.session.commit()
    
    def changeUserRewarded(self,user):
        self.user_f = user
        db.session.commit()
    
    def changeCoordinator(self,coordianator):
        self.coordinator_f = coordianator
        self.date_reward = datetime.datetime.utcnow()
        db.session.commit()
    
    
