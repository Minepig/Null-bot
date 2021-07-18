# -*- coding: utf-8 -*-
"""
Created on Tue Jul 13 15:51:14 2021

@author: hutr2
"""

import asyncio
import os
import traceback

from graia.saya import Saya, logger
from graia.broadcast import Broadcast
from graia.saya.builtins.broadcast import BroadcastBehaviour
from graia.application import GraiaMiraiApplication, Session

from utils import load_config

logger.warn = logger.warning

loop = asyncio.get_event_loop()
bcc = Broadcast(loop=loop)
saya = Saya(bcc)
saya.install_behaviours(BroadcastBehaviour(bcc))

configs = load_config()

app = GraiaMiraiApplication(
    broadcast=bcc,
    connect_info=Session(
        host=configs["miraiHost"],
        authKey=configs["authKey"],
        account=configs["BotQQ"],
        websocket=True
    ),
    logger=logger,
    enable_chat_log=False
)

ignore = ["__init__.py", "__pycache__"]

with saya.module_context():
    for module in os.listdir("modules"):
        if module in ignore:
            continue
        try:
            if os.path.isdir(module):
                saya.require(f"modules.{module}")
            else:
                saya.require(f"modules.{module.split('.')[0]}")
        except ModuleNotFoundError:
            pass

try:
    app.launch_blocking()
except KeyboardInterrupt:
    exit()
except:
    traceback.print_exc()
