CREATE TABLE userRole(
    id_role int AUTO_INCREMENT NOT NULL,
    role varchar(50) NOT NULL,
    role_description varchar(150),
    PRIMARY KEY (id_role)
);


CREATE TABLE workteam (
    id_team int AUTO_INCREMENT NOT NULL,
    PRIMARY KEY (id_team)
);


CREATE TABLE rel_team_user(
    id_rel int AUTO_INCREMENT NOT NULL,
    id_user int NOT NULL,
    id_team int NOT NULL, 
    id_role int NOT NULL,
    FOREIGN KEY (id_user) REFERENCES user(id_user),
    FOREIGN KEY (id_team) REFERENCES workteam(id_team),
    FOREIGN KEY (id_role) REFERENCES userRole(id_role),
    PRIMARY KEY (id_rel)
);

CREATE TABLE user(
    id_user int AUTO_INCREMENT NOT NULL,
    indentifier_tg varchar(150) NOT NULL,
    name_user varchar(150),
    surname varchar(150),
    fk_role int,
    FOREIGN KEY (fk_role) REFERENCES userRole(id_role),
    PRIMARY KEY (id_user)
);


CREATE TABLE reward(
    id_reward int AUTO_INCREMENT NOT NULL,
    reward_weight int NOT NULL,
    reward_description varchar(200),
    coordinator_f int NOT NULL,
    user_f int NOT NULL,
    date_reward date,
    FOREIGN KEY (coordinator_f) REFERENCES user(id_user),
    FOREIGN KEY (user_f) REFERENCES user(id_user),
    PRIMARY KEY (id_reward)
);


CREATE TABLE user_login(
    user varchar(50) NOT NULL,
    user_password varchar(50) NOT NULL,
    fst_question  varchar(100),
    fst_answer varchar(100),
    scd_question varchar(100),
    scd_answer varchar(100),
    PRIMARY KEY (user)
);


CREATE TABLE tg_authorization(
    token varchar(150) NOT NULL,
    user_token varchar(150),
    username  varchar(150),
    PRIMARY KEY (token)
); 


CREATE TABLE super_admin(
    id_admin int AUTO_INCREMENT NOT NULL,
    username varchar(50) NOT NULL,
    admin_password varchar(150) NOT NULL,
    fk_role int NOT NULL,
    FOREIGN KEY (fk_role) REFERENCES userRole(id_role),
    PRIMARY KEY (id_admin)
);
