from dataclasses import dataclass


@dataclass
class ClipboardMessage:
    """
    Contains clipboard data
    """
    uuid: str
    author: str
    text: str
    files: str
    src_ip: str
