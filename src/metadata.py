def start_run(conn,path,mode):
    with conn.cursor() as c:
        c.execute('INSERT INTO pipeline_runs(source_file,load_type,status) VALUES (%s,%s,%s) RETURNING run_id',(path,mode,'RUNNING'))
        return c.fetchone()[0]
def finish_run(conn,run_id,status,extracted,loaded,rejected,error=None):
    with conn.cursor() as c:
        c.execute('UPDATE pipeline_runs SET ended_at=now(),status=%s,records_extracted=%s,records_loaded=%s,records_rejected=%s,error_message=%s WHERE run_id=%s',(status,extracted,loaded,rejected,error,run_id))
def bookmark(conn,path):
    with conn.cursor() as c:
        c.execute('SELECT last_batch_done FROM pipeline_checkpoint WHERE source_file=%s',(path,))
        result=c.fetchone()
        return result[0] if result else 0
def checkpoint(conn,path,batch):
    with conn.cursor() as c:
        c.execute('INSERT INTO pipeline_checkpoint(source_file,last_batch_done) VALUES (%s,%s) ON CONFLICT(source_file) DO UPDATE SET last_batch_done=EXCLUDED.last_batch_done,updated_at=now()',(path,batch))
