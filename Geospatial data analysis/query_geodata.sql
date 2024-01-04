--SELECT PostGIS_Version();

--CREATE EXTENSION postgis;


WITH points AS (
    SELECT
        ST_Transform(ST_SetSRID(ST_MakePoint(CAST(radlongitude AS double precision), CAST(radlatitude AS double precision)), 4326), 32633) AS geom
    FROM
        location_data
),
clusters AS (
    SELECT
        ST_ClusterDBSCAN(geom, eps := 12874.8, minpoints := 1) OVER() AS cid,
        geom
    FROM
        points
)
SELECT
    COUNT(cid) AS number_of_points,
    ST_Collect(ST_Transform(geom, 4326)) AS geometry
FROM
    clusters
GROUP BY
    cid
ORDER BY
    number_of_points DESC;
