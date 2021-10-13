SELECT abbreviation, name
FROM nocs
ORDER BY abbreviation;

SELECT athletes.name, sex, birth_year, abbreviation
FROM athletes, nocs, results
WHERE athletes.id = results.athlete_id
AND nocs.abbreviation = results.noc_abbr
AND nocs.abbreviation = 'KEN';

SELECT result, year, event.name  
FROM
