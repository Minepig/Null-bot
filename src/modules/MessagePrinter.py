import sys

from graia.saya import Saya, Channel, logger
from graia.saya.builtins.broadcast.schema import ListenerSchema
from graia.application.event.messages import (
    FriendMessage, GroupMessage, TempMessage, 
    MessageChain, Group, Member, Friend
)


# 插件信息
__name__ = "MessagePrinter"
__description__ = "打印收到的消息"
__author__ = "SAGIRI-kawaii"
__usage__ = "发送消息即可触发"


saya = Saya.current()
channel = Channel.current()
logger.level("MESSAGE", no=0, color="<yellow>")
logger.add(sys.stdout, level="MESSAGE", 
           format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <level>{message}</level>",
           filter="MessagePrinter")

channel.name(__name__)
channel.description(f"{__description__}\n使用方法：{__usage__}")
channel.author(__author__)


@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def group_message_listener(
    message: MessageChain,
    sender: Member,
    group: Group
):
    msg = message.asSerializationString().replace("\n", " ")
    logger.log("MESSAGE", f"[{group.name}({group.id})|{sender.name}({sender.id})] - {msg}")


@channel.use(ListenerSchema(listening_events=[FriendMessage]))
async def friend_message_listener(
    message: MessageChain,
    sender: Friend
):
    msg = message.asSerializationString().replace("\n", " ")
    logger.log("MESSAGE", f"<{sender.nickname}({sender.id})> - {msg}")


@channel.use(ListenerSchema(listening_events=[TempMessage]))
async def temp_message_listener(
    message: MessageChain,
    sender: Member,
    group: Group
):
    msg = message.asSerializationString().replace("\n", " ")
    logger.log("MESSAGE", f"[{group.name}({group.id})]<{sender.name}({sender.id})> - {msg}")
