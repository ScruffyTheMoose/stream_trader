import sys
import os # pull data from .env
import pytchat
chat = pytchat.create(video_id='l20Jiimi1Mc')

while ( chat.is_alive() ):
    for c in chat.get().sync_items():
        print(f"{c.datetime} [{c.author.name}]- {c.message}")

