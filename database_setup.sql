CREATE TABLE users (
    "id" varchar(50) PRIMARY KEY,
    "access_token" text NOT NULL,
    "refresh_token" text NOT NULL
);

CREATE TABLE loggables (
  "cnt" serial primary key,
  "id" varchar(50),
  "distance" decimal,
  "floors" smallint,
  "steps" smallint,
  "restinghr" smallint,
  "calsout" smallint,
  "day" date
);
