CREATE TABLE "events" ("id" VARCHAR PRIMARY KEY  NOT NULL  UNIQUE , "title" TEXT, "start" DATETIME, "end" DATETIME, "details" TEXT);
CREATE TABLE "posts" ("title" VARCHAR NOT NULL , "description" VARCHAR NOT NULL , "author" VARCHAR PRIMARY KEY  NOT NULL );
CREATE TABLE "users" ("first_name"  NOT NULL , "last_name"  NOT NULL , "id"  PRIMARY KEY  NOT NULL  UNIQUE , "password"  NOT NULL , "username"  NOT NULL  UNIQUE );
