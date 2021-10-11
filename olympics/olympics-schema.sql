CREATE TABLE athletes(
  id SERIAL,
  surname text,
  given_name text,
  sex text,
  age integer,
  height integer,
);

CREATE TABLE games(
  id SERIAL,
  year integer,
  season text,
  city text
);

CREATE TABLE events(
  id SERIAL,
  name text,
  sport text
);

CREATE TABLE noc(
  id SERIAL,
  name text,
  abbreviation text
);

CREATE TABLE results(
  games_id integer,
  event_id integer,
  athlete_id integer,
  noc_id integer,
  result text
);
