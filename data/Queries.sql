
CREATE TABLE reviews_bis
AS 
SELECT *,	
	CASE
		WHEN rating > 5 THEN 1	
		ELSE 0	
	END AS Positive_rate 
FROM	
	reviews
;
DROP TABLE reviews
;
ALTER TABLE reviews_bis RENAME TO reviews
;

CREATE TABLE usuarios AS 
	SELECT DISTINCT 
		id_usuario 
	FROM 
		reviews;

SELECT * 
FROM 
	usuarios 
WHERE id_usuario = "nname"

DELETE FROM reviews WHERE id_usuario='noname';

SELECT * 
FROM 
	reviews r 
WHERE 
	id_review IN (SELECT 
						id_review  
				FROM 
					(SELECT DISTINCT 
						ID_REVIEW, 
						COUNT(ID_REVIEW) AS CANTIDAD 
					FROM 
						reviews r 
					GROUP BY 
						id_review 
					HAVING 
						CANTIDAD > 1
					)
				)

SELECT * FROM juegos WHERE game IS NULL;

DELETE FROM juegos WHERE game IS NULL ;


CREATE TABLE juegos_bis
AS 
SELECT 
	j.*,
	r.rating_avg  
FROM 
	juegos j 

INNER JOIN 
	(SELECT 
		id_juego, 
		ROUND(AVG(rating),1) AS rating_avg 
	FROM reviews r 
	GROUP BY id_juego
	) AS r 
		ON r.id_juego = j.id_juego;

DROP TABLE juegos
;

ALTER TABLE juegos_bis RENAME TO juegos
;

SELECT * FROM juegos j WHERE game = 'The Last Of Us Part Ii';

SELECT DISTINCT id_usuario FROM reviews r WHERE rating > 10;

UPDATE reviews SET rating = rating/10 WHERE rating > 10;

SELECT * FROM reviews r WHERE rating > 10;


SELECT id_juego, AVG(rating) as rating, count(*) AS cant

          FROM reviews
         WHERE id_juego NOT IN (SELECT id_juego FROM reviews WHERE id_usuario = ?)
           AND rating > 0
         
         GROUP BY 1
         HAVING cant > 10
         ORDER BY 2 DESC, 3 DESC         
         LIMIT 9
         
SELECT * FROM juegos g WHERE id_juego LIKE '%six%';
SELECT * FROM reviews g WHERE id_usuario = 'Johnsonsteed91';

SELECT id_juego, COUNT(1)  FROM reviews g WHERE  id_juego = 'ghost-of-tsushima';
 
SELECT * FROM juegos g WHERE game in  ("Fallout 76",
"Destiny The Dark Below",
"Mortal Kombat 11",
"Final Fantasy Xiv Online A Realm Reborn",
"Tom Clancy's The Division 2",
"Teenage Mutant Ninja Turtles Shredder's Revenge",
"Tom Clancy's Rainbow Six Siege");

SELECT * FROM juegos g WHERE Imagen in ("https://www.metacritic.com/a/img/resize/7d8d5baa92601c2301229ec14ea708364763c458/catalog/provider/6/3/6-1-92304-13.jpg?auto=webp&fit=cover&height=72&width=48",
"https://www.metacritic.com/a/img/resize/43306e0728d1bcbccef51bbac81f6ab3ba527b1f/catalog/provider/6/3/6-1-60703-13.jpg?auto=webp&fit=cover&height=72&width=48",
"https://www.metacritic.com/a/img/resize/ec4940f3d236d1b140773a5e0f1ccc72c602a94b/catalog/provider/6/3/6-1-19464-13.jpg?auto=webp&fit=cover&height=72&width=48",
"https://www.metacritic.com/a/img/resize/0a0525c56a2c92e519e4249bc70d02041420bbf3/catalog/provider/6/3/6-1-12013-13.jpg?auto=webp&fit=cover&height=72&width=48",
"https://www.metacritic.com/a/img/resize/a1cfbe720f0b33b47fdd5bd5b7a790aba92a807f/catalog/provider/6/12/6-1-779717-52.jpg?auto=webp&fit=cover&height=72&width=48",
"https://www.metacritic.com/a/img/resize/3b8158ac43e445d6c16b2add36f512d44cac7e62/catalog/provider/6/3/6-1-12131-13.jpg?auto=webp&fit=cover&height=72&width=48",
"https://www.metacritic.com/a/img/resize/ec0231fe75ac5d0869973b9ee8fe629057655844/catalog/provider/6/3/6-1-15438-13.jpg?auto=webp&fit=cover&height=72&width=48");







