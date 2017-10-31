DROP VIEW IF EXISTS article_log CASCADE;

CREATE VIEW article_log AS
  SELECT
    a.author as author_id,
    a.title,
    a.slug,
    count(a.id) as popularity
  FROM articles as a INNER JOIN log as l
  ON l.path LIKE CONCAT('%', a.slug, '%')
  group by (a.author, a.title,
  a.slug);
