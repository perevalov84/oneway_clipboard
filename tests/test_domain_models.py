import uuid
from oneway_clipboard.domain.model.model import ClipboardMessage
from oneway_clipboard.domain.model.services import save_message
import json
from oneway_clipboard.config import DB_PATH
import tempfile
import pytest


def test_create_clipboard_message_valid_parameters():
    msg = ClipboardMessage(
        uuid = str(uuid.uuid4),
        author = "user",
        text = "klkjasdf",
        files = "jklj",
        src_ip= "127.0.0.1"
    )
    assert isinstance(msg, ClipboardMessage)
    

@pytest.mark.integration
def test_read_users_database():
    
    with open(DB_PATH,'r') as file:
        users_data = json.load(file)

@pytest.mark.integration
def test_send_clipboard_message_to_srv_via_ssh():

    msg = ClipboardMessage(
        uuid=str(uuid.uuid4()),
        author="user",
        text=str(uuid.uuid4()),
        files='',
        src_ip="127.0.0.1"
    )
    save_message(msg)
    

def test_flask_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.get_json() == {"status":"ok"}
    

@pytest.mark.integration
def test_flask_tx_clipboard(client):
    remote_addr = '10.0.0.68'
    r = client.post(
        "/api/tx_clipboard",
        json = {"text":remote_addr},
        environ_base={'REMOTE_ADDR':remote_addr}
    )
    assert r.status_code == 200
    assert r.get_json() == {"status":"ok"}
    
@pytest.mark.integration
def test_flask_tx_files(client):
    f = tempfile.NamedTemporaryFile(delete=False)
    f.write(b'hello!')
    f.close()
    r = client.post(
        "/api/tx_clipboard",
        data = {"files": [
            (open(f.name,"rb"),"hello0.txt"),
            (open(f.name,"rb"),"hello1.txt"),
            (open(f.name,"rb"),"hello2.txt"),
            (open(f.name,"rb"),"hello3.txt"),
            ]
        },
        content_type = "multipart/form-data"
    )
