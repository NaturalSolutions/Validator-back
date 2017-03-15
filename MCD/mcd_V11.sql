------------------------------------------------------------
--        Script Postgre
------------------------------------------------------------



------------------------------------------------------------
-- Table: Types
------------------------------------------------------------
CREATE TABLE public.Types(
	id   SERIAL NOT NULL ,
	name VARCHAR (50) NOT NULL UNIQUE,
	size     INT   ,
	CONSTRAINT prk_constraint_Types PRIMARY KEY (id)
)WITHOUT OIDS;


------------------------------------------------------------
-- Table: Values
------------------------------------------------------------
CREATE TABLE public.Values(
	id    SERIAL NOT NULL ,
	value JSON  NOT NULL ,
	createdDate DATE  NOT NULL ,
	users_id     INT  NOT NULL ,
	CONSTRAINT prk_constraint_Values PRIMARY KEY (id)
)WITHOUT OIDS;


------------------------------------------------------------
-- Table: Fields
------------------------------------------------------------
CREATE TABLE public.Fields(
	id      SERIAL NOT NULL ,
	pos           INT   ,
	name     VARCHAR (50)  ,
	required BOOL   ,
	types_id        INT  NOT NULL ,
	CONSTRAINT prk_constraint_Fields PRIMARY KEY (id)
)WITHOUT OIDS;


------------------------------------------------------------
-- Table: Users
------------------------------------------------------------
CREATE TABLE public.Users(
	id       SERIAL NOT NULL ,
	lastName VARCHAR (250) NOT NULL ,
	firstName VARCHAR (250) NOT NULL ,
	email         VARCHAR (180)  ,
	picture   VARCHAR (180)  ,
	categories_id    INT   ,
	accounts_id     INT   ,
	CONSTRAINT prk_constraint_Users PRIMARY KEY (id)
)WITHOUT OIDS;


------------------------------------------------------------
-- Table: TypesPoi
------------------------------------------------------------
CREATE TABLE public.TypesPois(
	id     SERIAL NOT NULL ,
	name    VARCHAR (180) NOT NULL UNIQUE,
	name_fr VARCHAR (180) ,
	name_en VARCHAR (180) ,
	name_es VARCHAR (180) ,
	name_de VARCHAR (180) ,
	name_it VARCHAR (180) ,
	generaltypes_id  INT  NOT NULL ,
	CONSTRAINT prk_constraint_TypesPois PRIMARY KEY (id)
)WITHOUT OIDS;


------------------------------------------------------------
-- Table: GeneralTypes
------------------------------------------------------------
CREATE TABLE public.GeneralTypes(
	Id     SERIAL NOT NULL ,
	name   VARCHAR (180) NOT NULL UNIQUE,
	name_fr VARCHAR (180)  ,
	name_en VARCHAR (180) ,
	name_es VARCHAR (180)  ,
	name_de VARCHAR (180) ,
	name_it VARCHAR (180)  ,
	CONSTRAINT prk_constraint_GeneralTypes PRIMARY KEY (Id)
)WITHOUT OIDS;


------------------------------------------------------------
-- Table: Accounts
------------------------------------------------------------
CREATE TABLE public.Accounts(
	id SERIAL NOT NULL ,
	login     VARCHAR (180) NOT NULL UNIQUE,
	password  VARCHAR (180) NOT NULL ,
	CONSTRAINT prk_constraint_Accounts PRIMARY KEY (id)
)WITHOUT OIDS;


------------------------------------------------------------
-- Table: Categories
------------------------------------------------------------
CREATE TABLE public.Categories(
	id   SERIAL NOT NULL ,
	name VARCHAR (180) NOT NULL UNIQUE,
	CONSTRAINT prk_constraint_Categories PRIMARY KEY (id)
)WITHOUT OIDS;


------------------------------------------------------------
-- Table: Awards
------------------------------------------------------------
CREATE TABLE public.Awards(
	id    SERIAL NOT NULL ,
	type  VARCHAR (50)  ,
	label VARCHAR (80)  ,
	CONSTRAINT prk_constraint_Awards PRIMARY KEY (id)
)WITHOUT OIDS;


------------------------------------------------------------
-- Table: Pois
------------------------------------------------------------
CREATE TABLE public.Pois(
	id     SERIAL NOT NULL ,
	tour_id   INT  NOT NULL UNIQUE,
	typespois_id INT  NOT NULL ,
	CONSTRAINT prk_constraint_Pois PRIMARY KEY (id)
)WITHOUT OIDS;


------------------------------------------------------------
-- Table: possede
------------------------------------------------------------
CREATE TABLE public.Contributions(
	version INT   ,
	status  VARCHAR (25) NOT NULL ,
	idField INT  NOT NULL ,
	idValue INT  NOT NULL ,
	idPoi   INT  NOT NULL ,
	CONSTRAINT prk_constraint_contributions PRIMARY KEY (idField,idValue,idPoi)
)WITHOUT OIDS;


------------------------------------------------------------
-- Table: retribue
------------------------------------------------------------
CREATE TABLE public.Rewards(
	idAward INT  NOT NULL ,
	idUser  INT  NOT NULL ,
	CONSTRAINT prk_constraint_rewards PRIMARY KEY (idAward,idUser)
)WITHOUT OIDS;


------------------------------------------------------------
-- Table: commente
------------------------------------------------------------
CREATE TABLE public.Comments(
	message     VARCHAR (2000)   ,
	title       VARCHAR (25)  ,
	createdDate DATE   ,
	idUser      INT  NOT NULL ,
	idPoi       INT  NOT NULL ,
	CONSTRAINT prk_constraint_comments PRIMARY KEY (idUser,idPoi)
)WITHOUT OIDS;



ALTER TABLE public.Values ADD CONSTRAINT FK_Values_idUser FOREIGN KEY (users_id) REFERENCES public.Users(id);
ALTER TABLE public.Fields ADD CONSTRAINT FK_Fields_idType FOREIGN KEY (types_id) REFERENCES public.Types(id);
ALTER TABLE public.Users ADD CONSTRAINT FK_Users_idCategory FOREIGN KEY (categories_id) REFERENCES public.Categories(id);
ALTER TABLE public.Users ADD CONSTRAINT FK_Users_idAccount FOREIGN KEY (accounts_id) REFERENCES public.Accounts(id);
ALTER TABLE public.TypesPoi ADD CONSTRAINT FK_TypesPoi_IdGeneralType FOREIGN KEY (generaltypes_id) REFERENCES public.GeneralTypes(Id);
ALTER TABLE public.Pois ADD CONSTRAINT FK_Pois_idTypePoi FOREIGN KEY (typespois_id) REFERENCES public.TypesPoi(id);
ALTER TABLE public.contributions ADD CONSTRAINT FK_contributions_idField FOREIGN KEY (idField) REFERENCES public.Fields(id);
ALTER TABLE public.contributions ADD CONSTRAINT FK_contributions_idValue FOREIGN KEY (idValue) REFERENCES public.Values(id);
ALTER TABLE public.contributions ADD CONSTRAINT FK_contributions_idPoi FOREIGN KEY (idPoi) REFERENCES public.Pois(id);
ALTER TABLE public.rewards ADD CONSTRAINT FK_retribue_idAward FOREIGN KEY (idAward) REFERENCES public.Awards(id);
ALTER TABLE public.rewards ADD CONSTRAINT FK_retribue_idUser FOREIGN KEY (idUser) REFERENCES public.Users(id);
ALTER TABLE public.comments ADD CONSTRAINT FK_comments_idUser FOREIGN KEY (idUser) REFERENCES public.Users(id);
ALTER TABLE public.comments ADD CONSTRAINT FK_comments_idPoi FOREIGN KEY (idPoi) REFERENCES public.Pois(id);
