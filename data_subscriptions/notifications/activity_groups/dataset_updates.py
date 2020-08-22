QUERY = """
SELECT
  kind,
  user_id,
  activity->>'object_id' AS dataset_id,
  dataset_name,
  user_name,
  activity->>'activity_type' AS activity_type,
  activity,
  to_char(collected_at, 'YYYY-MM-DD"T"HH24:MI:SSOF') AS collected_at
FROM
  dataset_activity_list,
  json_array_elements(dataset_activity_list.blob) AS activity
  JOIN subscription ON (
    activity->>'object_id' = subscription.dataset_id
  )
WHERE
  (subscription.kind = 'DATASET' OR subscription.kind IS NULL) AND
  (activity->>'activity_type' != 'new package') AND
  (collected_at::timestamptz >= :start_time)
"""
