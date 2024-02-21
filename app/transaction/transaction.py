from datetime import datetime
import uuid

def generate_transaction_id():
    tahun_sekarang = datetime.now().year
    angka_unik = uuid.uuid4().int & (1<<64)-1
    return f'SUK-{tahun_sekarang}-{angka_unik:013d}'[:20]