-- SQLite
SELECT
l.id as load_id,
t.alias as truck_alias,
t.current_city || ", " || t.current_state as truck_location
FROM roadrunnerapi_load as l
JOIN 
roadrunnerapi_bid as b,
roadrunnerapi_truck as t
ON l.id = b.load_id
AND b.truck_id = t.id
WHERE b.is_accepted = true


