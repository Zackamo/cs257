/* sample SQL queries for the olympics database
  By: Zack Johnson
*/

-- List all National Olympic Committees alphabetially by abbreviation.
SELECT abbreviation, name
FROM nocs
ORDER BY abbreviation;

-- List all athletes from Kenya (KEN)
SELECT DISTINCT athletes.name, sex, birth_year, abbreviation
FROM athletes, nocs, results
WHERE athletes.id = results.athlete_id
AND nocs.abbreviation = results.noc_abbr
AND nocs.abbreviation = 'KEN';

-- List all medals won by Greg Louganis
SELECT games.year, games.city, events.name AS event, athletes.name, nocs.abbreviation, result
FROM athletes, games, results, nocs, events
WHERE athletes.id = results.athlete_id
AND games.year = results.games_year
AND nocs.abbreviation = results.noc_abbr
AND events.id = results.event_id
AND result IS NOT NULL
AND athletes.name LIKE '%Louganis%';

-- List all National Olympic Committees by Number of Gold medal won all time
SELECT count(result) AS Golds, nocs.abbreviation, nocs.name
FROM nocs, results
WHERE nocs.abbreviation = results.noc_abbr
AND LOWER(result) = 'gold'
GROUP BY nocs.abbreviation, nocs.name
ORDER BY Golds DESC;
