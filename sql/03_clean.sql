-- SQL demonstration of trimming, lowercasing, rejection, and upsert.
INSERT INTO rejected_records(run_id,source_row,reason)
SELECT run_id,source_row,'Missing account_id' FROM staging_records
WHERE nullif(btrim(account_id),'') IS NULL;
INSERT INTO clean_records(account_id,first_name,email_1,deal_stage)
SELECT DISTINCT ON (btrim(account_id)) btrim(account_id),nullif(btrim(payload->>'first_name'),''),lower(nullif(btrim(payload->>'email_1'),'')),nullif(btrim(payload->>'deal_stage'),'')
FROM staging_records WHERE nullif(btrim(account_id),'') IS NOT NULL
ORDER BY btrim(account_id), id DESC
ON CONFLICT(account_id) DO UPDATE SET first_name=EXCLUDED.first_name,email_1=EXCLUDED.email_1,deal_stage=EXCLUDED.deal_stage
WHERE (clean_records.first_name,clean_records.email_1,clean_records.deal_stage) IS DISTINCT FROM (EXCLUDED.first_name,EXCLUDED.email_1,EXCLUDED.deal_stage);
