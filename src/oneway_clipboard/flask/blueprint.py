import os
import uuid
from flask import (
    Blueprint, g, request, jsonify
)
from oneway_clipboard.domain.model.model import ClipboardMessage
from oneway_clipboard.domain.model.adapter import ClipboardMessageTransfer
import shutil


bp = Blueprint('api',__name__,url_prefix='/api')

@bp.route('/tx_clipboard', methods=('GET','POST'))
def tx_clipboard():
    UPLOAD_DIR = os.path.join('/tmp/upload',str(uuid.uuid4()))
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    text = ''
    paths = []
    if request.method == 'POST':
        if request.mimetype == "application/json":
            payload = request.get_json()
            text = payload['text']
        elif request.mimetype == "multipart/form-data":
            files = request.files.getlist("files")
            paths = []
            for f in files:
                filename = f.filename
                path = os.path.join(UPLOAD_DIR, filename)
                f.save(path)
                paths.append((path, filename))

        if text or paths:
            msg = ClipboardMessage(
                    uuid=str(uuid.uuid4()),
                    author='',
                    text = text,
                    files=paths,
                    src_ip=request.remote_addr,
                )
                
            tx_msg = ClipboardMessageTransfer(msg)
            tx_msg.transfer_msg()
            shutil.rmtree(UPLOAD_DIR)
            return jsonify({'status':'ok'})
    return jsonify({'status':'failure'})
    
