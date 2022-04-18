from __future__ import annotations

from aiogram.types import Chat as OChat
import asyncio
from threading import Thread
from utils.main.db import sql


all_chats_ = [i[0] for i in sql.get_all_data('chats')]


def all_chats():
    return all_chats_


class Chat:
    def __init__(self, chat: OChat | int = None, source=None):
        if source is None:
            if isinstance(chat, OChat):
                self.source = sql.select_data(chat.id, 'id', True, 'chats')

                self.id: int = chat.id
                self.title: str = chat.title
                try:
                    self.photo: str = chat.photo.big_file_id
                except:
                    pass
                self.photo = None
                try: self.invite_link: str = chat.invite_link or self.source[3]
                except: self.invite_link: str = chat.invite_link
                self.username: str = chat.username
            else:
                self.source = sql.select_data(chat, 'id', True, 'chats')

                self.id: int = self.source[0]
                self.title: str = self.source[1]
                self.photo: str = self.source[2]
                self.invite_link: str = self.source[3]
                self.username: str = self.source[4]
            if self.source is None:
                self.source = Chat.create(chat)
            elif isinstance(chat, OChat):
                Thread(target=self.check, args=(chat,)).start()
        else:
            self.source: tuple = source
            self.id: int = self.source[0]
            self.title: str = self.source[1]
            self.photo: str = self.source[2]
            self.invite_link: str = self.source[3]
            self.username: str = self.source[4]
    
    def check(self, chat: OChat = None):
        _, title, phot, invite_link, username = self.source
        query = ''
        if title != self.title and self.title:
            query += f' title = "{self.title}",'
        if phot != self.photo and self.photo:
            photo = f'"{self.photo}"' if self.photo else 'NULL'
            query += f' photo = {photo},'
        if invite_link != self.invite_link and self.invite_link:
            link = f'"{self.invite_link}"' if self.invite_link else 'NULL'
            query += f' invite_link = {link},'
        if username != self.username and self.username:
            u = f'"{self.username}"' if self.username else 'NULL'
            query += f' username = {u},'
        if query:
            if query[-1] == ',':
                query = query[:-1]
            sql.execute(f'UPDATE chats SET {query} WHERE id = {self.id};')

    @staticmethod
    def create(chat: OChat | int):
        global all_chats_
        if isinstance(chat, OChat):
            res = (chat.id, chat.title, chat.photo.big_file_id if chat.photo else None, chat.invite_link,
                   chat.username)
        else:
            res = (chat, None, None, None, None)
        sql.insert_data([res], 'chats')
        all_chats_.append(res[0])
        return res
