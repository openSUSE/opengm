import logging

from defrag.modules.helpers.sync_utils import as_async
from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    UnicodeText,
    UniqueConstraint,
    func,
)
from sqlalchemy.future import select

from opengm.plugins.sql import BASE, SESSION

LOGGER = logging.getLogger(__name__)


class Users(BASE):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True)
    username = Column(UnicodeText)

    def __init__(self, user_id, username=None):
        self.user_id = user_id
        self.username = username


#    def __repr__(self):
#        return "<User {} ({})>".format(self.username, self.user_id)


class Chats(BASE):
    __tablename__ = "chats"
    chat_id = Column(String(14), primary_key=True)
    chat_name = Column(UnicodeText, nullable=False)

    def __init__(self, chat_id, chat_name):
        self.chat_id = str(chat_id)
        self.chat_name = chat_name

    def __repr__(self):
        return "<Chat {} ({})>".format(self.chat_name, self.chat_id)


class ChatMembers(BASE):
    __tablename__ = "chat_members"
    priv_chat_id = Column(Integer, primary_key=True)
    # NOTE: Use dual primary key instead of private primary key?
    chat = Column(
        String(14),
        ForeignKey("chats.chat_id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
    )
    user = Column(
        Integer,
        ForeignKey("users.user_id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
    )
    __table_args__ = (
        UniqueConstraint("chat", "user", name="_chat_members_uc"),
    )

    def __init__(self, chat, user):
        self.chat = chat
        self.user = user

    def __repr__(self):
        return "<Chat user {} ({}) in chat {} ({})>".format(
            self.user.username,
            self.user.user_id,
            self.chat.chat_name,
            self.chat.chat_id,
        )


async def ensure_bot_in_db(id, username):
    bot = Users(id, username)
    await SESSION.merge(bot)
    await SESSION.commit()


async def update_user(user_id, username, chat_id=None, chat_name=None):
    user = (
        (await SESSION.execute(select(Users).where(Users.user_id == user_id)))
        .scalars()
        .first()
    )
    if user is None:
        user = Users(user_id, username)
        as_async(SESSION.add(user))
        await SESSION.flush()
    else:
        user.username = username

    if not chat_id or not chat_name:
        await SESSION.commit()
        return

    chat = (
        (
            await SESSION.execute(
                select(Chats).where(Chats.chat_id == str(chat_id))
            )
        )
        .scalars()
        .first()
    )
    if not chat:
        chat = Chats(str(chat_id), chat_name)
        as_async(SESSION.add(chat))
        await SESSION.flush()

    else:
        chat.chat_name = chat_name

    member = (
        (
            await SESSION.execute(
                select(ChatMembers)
                .where(ChatMembers.chat == chat.chat_id)
                .where(ChatMembers.user == user.user_id)
            )
        )
        .scalars()
        .first()
    )
    if not member:
        chat_member = ChatMembers(chat.chat_id, user.user_id)
        SESSION.add(chat_member)

    await SESSION.commit()


async def get_user_id_by_name(username):
    try:
        if username.startswith("@"):
            username = username[1:]
        id = (
            (
                await SESSION.execute(
                    select(Users).where(
                        func.lower(Users.username) == username.lower()
                    )
                )
            )
            .scalars()
            .all()
        )  # .where(func.lower(Users.username) == username.lower())
        print("Here")
        return id
    finally:
        await SESSION.close()
