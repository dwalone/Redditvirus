SELECT AVG(cnt) FROM (
	SELECT COUNT(*) AS cnt FROM infections GROUP BY infector
        )

