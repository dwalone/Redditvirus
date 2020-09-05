SELECT infector, COUNT(*) AS cnt FROM infections 
GROUP BY infector 
ORDER BY cnt DESC 
LIMIT 10
