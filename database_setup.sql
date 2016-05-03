CREATE TABLE users (
    "id" varchar(50) PRIMARY KEY,
    "access_token" text NOT NULL,
    "refresh_token" text NOT NULL,
);

CREATE TABLE loggables (
  "id" varchar(50) PRIMARY KEY,
  "steps" ,
   
)
