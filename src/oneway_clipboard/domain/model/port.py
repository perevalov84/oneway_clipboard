from oneway_clipboard.domain.model.model import ClipboardMessage
from abc import ABC, abstractmethod


def save_clipboard_message(msg: ClipboardMessage) -> None:
    pass

class ClipboardMessageTransferInterface(ABC):
    @abstractmethod
    def __init__(self,msg: ClipboardMessage) -> None:
        raise NotImplementedError
    
    def transfer_msg(self) -> None:
        return self._transfer_msg()

    @abstractmethod
    def _transfer_msg(self) -> None:
        pass
    