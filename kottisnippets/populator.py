from kotti import DBSession
from kotti.resources import Node
from resources import SnippetsStorage

def populator():
    if DBSession.query(SnippetsStorage).count() == 0:
        root = DBSession.query(Node).filter(Node.parent_id == None).one()
        storage = SnippetsStorage('snippet-storage', title='Snippets')
        DBSession.add(storage)
        root[storage.name] = storage
