QUERY = """
SELECT
  kind,
  user_id,
  activity->>'object_id' AS dataset_id,
  dataset_name,
  user_name,
  activity->>'activity_type' AS activity_type,
  activity
FROM
  dataset_activity_list,
  json_array_elements(dataset_activity_list.blob) AS activity
  JOIN subscription ON (
    activity->>'activity_type' = 'new package'
  )
WHERE
  (subscription.kind = 'NEW_DATASETS') AND
  ((activity->>'timestamp')::timestamptz > :start_time)
"""
