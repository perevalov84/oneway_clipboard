from oneway_clipboard.domain.model.model import ClipboardMessage
from oneway_clipboard.domain.model.port import ClipboardMessageTransferInterface
from oneway_clipboard.config import DB_PATH, KEY_PATH
from typing import List
import json

from paramiko.client import SSHClient, AutoAddPolicy


def get_user_data(msg: ClipboardMessage)-> List:
  with open(DB_PATH,'r') as file:
    user_data = json.load(file)
  dst_info=[]
  for record in user_data:
    if record['src_ip'] == msg.src_ip:
       dst_info.append(record)
  return dst_info


class ClipboardMessageTransfer(ClipboardMessageTransferInterface):
    def __init__(self, msg):
      self.msg = msg 
      
    def _transfer_msg(self):
       """
       Transfer clipboard message to rdp user
        - Connect to server with proper private ssh key
        - Transfer files to temp directory to server
        - Place text, or files to clipboard in rdp user session
       """
       
       user_dst_info = get_user_data(self.msg)
       if len(user_dst_info) > 0:
        for record in user_dst_info:
          client = SSHClient()
          client.set_missing_host_key_policy(AutoAddPolicy())
          username = record['username']
          hostname = record['dst_ip']
          privkey = str(KEY_PATH)+"/"+record['privkey']
          text = self.msg.text
          files = self.msg.files
          client.connect(username=username,hostname=hostname,key_filename=privkey)
          if text:
            stdin, stdout, sdterr = client.exec_command(f'"c:\\Program Files\\CopyQ\\copyq.exe" copy - ')
            stdin.write(text)
            stdin.close()
            

          if files:
            stdin, stdout, stderr = client.exec_command('echo %USERPROFILE%')
            user_profile_win = stdout.read().decode("cp866").strip()
            remote_filelist = []
            sftp_client = client.open_sftp()
            
            for path, filename in files:
              remote_path = user_profile_win+"\\AppData\\Local\\Temp\\"+filename
              sftp_client.put(path,remote_path)
              remote_filelist.append('file:///'+str.replace(remote_path,'\\','/'))

            sftp_client.close()
            stdin, stdout, stderr = client.exec_command(f'"c:\\Program Files\\CopyQ\\copyq.exe" copy text/uri-list -')
            stdin.write("\n\r".join( _ for _ in remote_filelist))
            stdin.close()

          client.close()
