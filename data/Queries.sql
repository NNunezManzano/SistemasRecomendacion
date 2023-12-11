
CREATE TABLE reviews_bis
AS 
SELECT *,	
	CASE
		WHEN rating > 6 THEN 1	
		ELSE 0	
	END AS Positive_rate 
FROM	reviews
;
DROP TABLE reviews
;
ALTER TABLE reviews_bis RENAME TO reviews
;

CREATE TABLE usuarios AS SELECT DISTINCT id_usuario FROM reviews;

