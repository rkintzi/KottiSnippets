from sqlalchemy import (
        Column,
        ForeignKey,
        ForeignKeyConstraint,
        Integer,
        String,
        )
from sqlalchemy.orm import (
        backref,
        relation,
        )
from sqlalchemy.ext.orderinglist import ordering_list
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.util import classproperty

from kotti import Base
from kotti.resources import Content, Document, TypeInfo
from kotti.util import camel_case_to_name

from . import _

class SnippetsStorage(Content):
    id = Column('id', Integer, ForeignKey('contents.id'), primary_key = True)

    @classproperty
    def __mapper_args__(cls):
        return dict(polymorphic_identity=camel_case_to_name(cls.__name__))

    type_info = Content.type_info.copy(
            name = u'SnippetsStorage',
            title = _(u'Snippets'),
            add_view = None,
            addable_to = [],
            edit_links=[],
            )
    _in_navigation = False

    @property
    def in_navigation(self):
        return False

    @in_navigation.setter
    def in_navigation(self, in_navigation):
        pass

    def __init__(self, name=None, title=None):
        super(SnippetsStorage, self).__init__(name=name, title=title,
                in_navigation=False)


class Snippet(Document):
    id = Column('id', Integer, ForeignKey('documents.id'), primary_key = True)

    type_info = Document.type_info.copy(
            name = u'Snippet',
            title = _(u'Snippet'),
            addable_to = [u'SnippetsStorage'],
            add_view = 'add-snippet',
            )

class DocumentSlot(Base):
    document_id = Column(Integer, ForeignKey('documents.id'), primary_key=True)
    name = Column(String, primary_key=True)

    document = relation(Document,
            backref=backref("slots", 
                order_by=[name],
                cascade='all, delete-orphan',
                ))
    snippets = association_proxy('_snippets', 'snippet')
#    _snippets = relation(
#            lambda:DocumentSlotToSnippet,
#            cascade='all, delete-orphan',
#            collection_class=ordering_list('position'),
#            order_by=[DocumentSlotToSnippet.position]
#            )
            

class DocumentSlotToSnippet(Base):
    __table_args__ = (
            ForeignKeyConstraint(['document_id', 'slot_name'],
                [DocumentSlot.document_id, DocumentSlot.name]),
            )
    __tablename__ = 'documents_slots_to_snippets'
    @classproperty
    def __mapper_args__(cls):
        return dict(polymorphic_identity=camel_case_to_name(cls.__name__))
    document_id = Column(Integer, primary_key=True)
    slot_name = Column(String, primary_key = True)
    snippet_id = Column(Integer, ForeignKey('snippets.id'), primary_key=True)
    position = Column(Integer, nullable=False)
    snippet = relation(Snippet)

    def __init__(self, snippet):
        self.snippet = snippet

    slot = relation(DocumentSlot,
            backref = backref(
                '_snippets',
                cascade='all, delete-orphan',
                collection_class=ordering_list('position'),
                order_by=[position],
                ))
