from sqlalchemy import (
        Column,
        ForeignKey,
        ForeignKeyConstraint,
        Integer,
        String,
        UnicodeText,
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

class SnippetCollection(Content):
    id = Column('id', Integer, ForeignKey('contents.id'), primary_key = True)

    @classproperty
    def __mapper_args__(cls):
        return dict(polymorphic_identity=camel_case_to_name(cls.__name__))

    type_info = Content.type_info.copy(
            name = u'SnippetCollection',
            title = _(u'Snippet Collection'),
            add_view = u'add-snippet-collection',
            addable_to = ['SnippetCollection'],
            )
    _in_navigation = False

    @property
    def in_navigation(self):
        return False

    @in_navigation.setter
    def in_navigation(self, in_navigation):
        pass

    def __init__(self, name=None, title=None):
        super(SnippetCollection, self).__init__(name=name, title=title,
                in_navigation=False)

class Snippet(Content):
    id = Column('id', Integer, ForeignKey('contents.id'), primary_key = True)

    @classproperty
    def __mapper_args__(cls):
        return dict(polymorphic_identity=camel_case_to_name(cls.__name__))

    type_info = Content.type_info.copy(
            name = u'Snippet',
            title = _(u'Snippet'),
            add_view = None,
            addable_to = [],
            )
    _in_navigation = False

    @property
    def in_navigation(self):
        return False

    @in_navigation.setter
    def in_navigation(self, in_navigation):
        pass

    def __init__(self, **kwargs):
        kwargs['in_navigation'] = False
        super(Snippet, self).__init__(**kwargs)


class TextSnippet(Snippet):
    id = Column('id', Integer, ForeignKey('snippets.id'), primary_key = True)

    body = Column(UnicodeText())
    mime_type = Column(String(30))
    
    type_info = Snippet.type_info.copy(
            name = u'TextSnippet',
            title = _(u'Text Snippet'),
            add_view = u'add-snippet',
            addable_to=['SnippetCollection']
            )

    def __init__(self, body=u"", mime_type='text/html', **kwargs):
        super(TextSnippet, self).__init__(**kwargs)
        self.body = body
        self.mime_type = mime_type


class DocumentSlot(Base):
    document_id = Column(Integer, ForeignKey('documents.id'), primary_key=True)
    name = Column(String, primary_key=True)

    document = relation(Document,
            backref=backref("slots", 
                order_by=[name],
                cascade='all, delete-orphan',
                ))
    snippets = association_proxy('_snippets', 'snippet')
            

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
    snippet_id = Column(Integer, 
            ForeignKey('snippets.id', ondelete="CASCADE", onupdate="CASCADE"), 
            primary_key=True)
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

