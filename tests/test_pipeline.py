from src.extract import make_batches
from src.transform import clean_record

def test_batches(): assert [len(b) for b in make_batches(list(range(105)),50)]==[50,50,5]
def test_clean():
    item,reason=clean_record({'account_id':' A1 ','email_1':' A@B.COM '})
    assert reason is None and item['account_id']=='A1' and item['email_1']=='a@b.com'
def test_reject(): assert clean_record({'account_id':' '})[1]=='Missing account_id'
