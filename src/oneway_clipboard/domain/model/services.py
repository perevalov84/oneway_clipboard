from oneway_clipboard.domain.model.model import ClipboardMessage
from oneway_clipboard.domain.model.adapter import ClipboardMessageTransfer


def save_message(msg: ClipboardMessage)-> None:
    clp = ClipboardMessageTransfer(msg)
    clp.transfer_msg()