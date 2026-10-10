INSERT INTO final_leads(account_id,full_name,company,email,source,deal_stage)
SELECT account_id,concat_ws(' ',first_name,last_name),company,coalesce(email_1,email_2),source,deal_stage FROM clean_records
ON CONFLICT(account_id) DO UPDATE SET full_name=EXCLUDED.full_name,company=EXCLUDED.company,email=EXCLUDED.email,source=EXCLUDED.source,deal_stage=EXCLUDED.deal_stage
WHERE (final_leads.full_name,final_leads.company,final_leads.email,final_leads.source,final_leads.deal_stage)
IS DISTINCT FROM (EXCLUDED.full_name,EXCLUDED.company,EXCLUDED.email,EXCLUDED.source,EXCLUDED.deal_stage);
