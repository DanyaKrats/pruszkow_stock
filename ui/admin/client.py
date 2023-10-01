from src.database.tables.cargo import Client, Sender, Recipient
from sqladmin import ModelView


class ClientView(ModelView, model = Client):
    # icon =
    column_list =[
        Client.id,
        Client.name
    ]
    # column_exclude_list = [Client.senders]

class SenderView(ModelView,  model = Sender):
    # icon =
    column_list =[
        Sender.id,
        Sender.name,
    ]

class RecipientView(ModelView,  model = Recipient):
    # icon =
    column_list =[
        Recipient.id,
        Recipient.name,
    ]