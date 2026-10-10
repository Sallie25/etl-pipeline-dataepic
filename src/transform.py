FIELDS=['account_id','lead_owner','first_name','last_name','company','phone_1','phone_2','email_1','email_2','website','source','deal_stage','notes']
def clean_record(raw):
    clean={key: (str(raw.get(key)).strip() or None) if raw.get(key) is not None else None for key in FIELDS}
    if not clean['account_id']: return None,'Missing account_id'
    for key in ('email_1','email_2'):
        if clean[key]:
            clean[key]=clean[key].lower()
            if '@' not in clean[key]: return None,'Invalid '+key
    return clean,None
