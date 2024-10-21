from abc import ABC, abstractmethod
from typing import Any, Optional, Tuple


class IActorConnector(ABC):
    """
    An abstract base class that defines the interface for actor connectors.
    Actor connectors are responsible for sending and receiving messages between actors.
    """

    @abstractmethod
    def send_txt_msg(self, msg: str) -> None:
        """
        Send a text message.

        Args:
            msg (str): The text message to be sent.
        """
        pass

    @abstractmethod
    def send_bin_msg(self, msg_type: str, msg: bytes) -> None:
        """
        Send a binary message.

        Args:
            msg_type (str): The type of the binary message.
            msg (bytes): The binary message to be sent.
        """
        pass

    @abstractmethod
    def send_proto_msg(self, msg: Any) -> None:
        """
        Send a protocol buffer message.

        Args:
            msg (Any): The protocol buffer message to be sent.
        """
        pass

    @abstractmethod
    def send_recv_proto_msg(
        self, msg: Any, num_attempts: int = 5
    ) -> Tuple[Optional[str], Optional[str], Optional[bytes]]:
        """
        Send a protocol buffer message and receive a response.

        Args:
            msg (Any): The protocol buffer message to be sent.
            num_attempts (int, optional): The number of attempts to send and receive the message. Defaults to 5.

        Returns:
            Tuple[Optional[str], Optional[str], Optional[bytes]]: A tuple containing the topic, message type, and message content of the response.
        """
        pass

    @abstractmethod
    def send_recv_msg(
        self, msg_type: str, msg: bytes, num_attempts: int = 5
    ) -> Tuple[Optional[str], Optional[str], Optional[bytes]]:
        """
        Send a binary message and receive a response.

        Args:
            msg_type (str): The type of the binary message.
            msg (bytes): The binary message to be sent.
            num_attempts (int, optional): The number of attempts to send and receive the message. Defaults to 5.

        Returns:
            Tuple[Optional[str], Optional[str], Optional[bytes]]: A tuple containing the topic, message type, and message content of the response.
        """
        pass

    @abstractmethod
    def close(self) -> None:
        """
        Close the actor connector and release any resources.
        """
        pass