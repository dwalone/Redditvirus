WITH RECURSIVE
    infected_record(level, name) AS (
        VALUES(0, '<reddit user>')

        UNION

        SELECT infected_record.level+1, infections.infector
        FROM infections, infected_record
        WHERE infections.name = infected_record.name
    )
SELECT infected_record.level, infections.name
FROM infections, infected_record
WHERE infections.name = infected_record.name
ORDER BY infected_record.level ASC
