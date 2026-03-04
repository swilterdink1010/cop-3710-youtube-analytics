SELECT
  c.category_id,
  Avg(v.vid_views) AS performance_avg_views,
  Avg(v.vid_ctr) AS performance_ctr
FROM
  (
    category AS c
    INNER JOIN video_category AS vc ON c.category_id = vc.category_id
  )
  INNER JOIN video AS v ON vc.vid_id = v.vid_id
GROUP BY
  c.category_id;
