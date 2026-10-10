SELECT 'staging' AS layer,count(*) FROM staging_records UNION ALL SELECT 'clean',count(*) FROM clean_records UNION ALL SELECT 'final',count(*) FROM final_leads UNION ALL SELECT 'rejected',count(*) FROM rejected_records;
SELECT account_id,count(*) FROM final_leads GROUP BY account_id HAVING count(*)>1;
SELECT count(*) AS missing_ids FROM final_leads WHERE account_id IS NULL;
SELECT status,load_type,records_extracted,records_loaded,records_rejected,error_message FROM pipeline_runs ORDER BY run_id;
SELECT * FROM pipeline_checkpoint;
SELECT source,count(*) FROM final_leads GROUP BY source ORDER BY count(*) DESC;
