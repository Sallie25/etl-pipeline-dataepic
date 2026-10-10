from psycopg.types.json import Jsonb

from .transform import FIELDS


def save_batch(conn,run_id,batch_no,raw_records):
    from .transform import clean_record
    loaded=0;rejected=0
    with conn.cursor() as c:
        for raw in raw_records:
            c.execute('INSERT INTO staging_records(run_id,batch_no,source_row,account_id,payload) VALUES (%s,%s,%s,%s,%s)',(run_id,batch_no,str(raw.get('source_row','')),raw.get('account_id'),Jsonb(raw)))
            good,reason=clean_record(raw)
            if reason:
                rejected+=1
                c.execute('INSERT INTO rejected_records(run_id,source_row,reason) VALUES (%s,%s,%s)',(run_id,str(raw.get('source_row','')),reason))
                continue
            cols=FIELDS
            colnames=','.join(cols)
            placeholders=','.join(['%s']*len(cols))
            updates=','.join(f'{key}=EXCLUDED.{key}' for key in cols if key!='account_id')
            changed=' OR '.join(f'clean_records.{key} IS DISTINCT FROM EXCLUDED.{key}' for key in cols if key!='account_id')
            c.execute(f'INSERT INTO clean_records({colnames}) VALUES ({placeholders}) ON CONFLICT(account_id) DO UPDATE SET {updates},updated_at=now() WHERE {changed} RETURNING account_id',[good[k] for k in cols])
            if c.fetchone(): loaded+=1
    return loaded,rejected
