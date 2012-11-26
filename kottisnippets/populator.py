from kotti import DBSession
from kotti.resources import Node
from resources import SnippetCollection

def populator():
    if DBSession.query(SnippetCollection).count() == 0:
        root = DBSession.query(Node).filter(Node.parent_id == None).one()
        storage = SnippetCollection('main-snippet-collection', title='All Snippets')
        DBSession.add(storage)
        root[storage.name] = storage
