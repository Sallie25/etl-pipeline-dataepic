import os
import sys
from pathlib import Path

from .config import BATCH_SIZE
from .db import connect
from .extract import make_batches, read_records
from .load import save_batch
from .metadata import bookmark, checkpoint, finish_run, start_run

ROOT=Path(__file__).resolve().parents[1]
def run(mode):
    if mode not in ('full','incremental'): raise ValueError('Use full or incremental')
    path=ROOT/'data'/'raw'/('source_full.json' if mode=='full' else 'source_incremental.json')
    records=read_records(path); batches=make_batches(records,BATCH_SIZE)
    conn=connect(); run_id=None; loaded=0;rejected=0
    try:
        run_id=start_run(conn,path.name,mode); conn.commit()
        last=bookmark(conn,path.name)
        print(f'RUN {run_id}: {mode}; {len(records)} source records; resume after batch {last}')
        for number,batch in enumerate(batches,1):
            if number<=last: continue
            try:
                n,r=save_batch(conn,run_id,number,batch)
                checkpoint(conn,path.name,number)
                conn.commit()
                loaded+=n;rejected+=r
                print(f'Batch {number}/{len(batches)} committed: upserted={n}, rejected={r}')
                if os.getenv('FAIL_AT_BATCH')==str(number): raise RuntimeError('Simulated failure after committed batch '+str(number))
            except Exception:
                conn.rollback();raise
        with conn.cursor() as c:
            c.execute((ROOT/'sql'/'04_transform.sql').read_text())
        finish_run(conn,run_id,'SUCCESS',len(records),loaded,rejected)
        checkpoint(conn,path.name,0) # successful file finished; replay safe via upserts
        conn.commit()
        print(f'SUCCESS: extracted={len(records)} upserted={loaded} rejected={rejected}')
    except Exception as exc:
        conn.rollback()
        if run_id is not None:
            finish_run(conn,run_id,'FAILED',len(records),loaded,rejected,str(exc));conn.commit()
        print('FAILED:',exc);raise
    finally: conn.close()
if __name__=='__main__': run(sys.argv[1] if len(sys.argv)>1 else 'full')
