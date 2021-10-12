CREATE TABLE athletes(
  id integer,
  name text,
  sex text,
  birth_year integer
);

CREATE TABLE games(
  year integer,
  season text,
  city text
);

CREATE TABLE events(
  id integer,
  name text,
  sport text
);

CREATE TABLE noc(
  abbreviation text,
  name text
);

CREATE TABLE results(
  games_year integer,
  event_id integer,
  athlete_id integer,
  noc_abbr integer,
  result text
);
