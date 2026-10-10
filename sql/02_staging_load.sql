-- SQL demonstration: stage messy JSON without discarding duplicate IDs.
-- Requires 01_schema.sql; the Python pipeline stages the full JSON file.
INSERT INTO pipeline_runs (source_file, load_type, status) VALUES ('sql-demo','demo','SUCCESS');
INSERT INTO staging_records(run_id,batch_no,source_row,account_id,payload)
SELECT max(run_id),1,'demo-1','DEMO001','{"account_id":"DEMO001","first_name":" Ada ","email_1":"ADA@EXAMPLE.COM","deal_stage":"New"}'::jsonb FROM pipeline_runs;
