from pkg_resources import resource_filename
import colander
from deform import ZPTRendererFactory
from deform.widget import (
        RichTextWidget, 
        SequenceWidget, 
        MappingWidget, 
        FormWidget,
        TextInputWidget,
        SelectWidget,
        )
from sqlalchemy.sql import and_
from pyramid.httpexceptions import HTTPFound
from pyramid.exceptions import PredicateMismatch
from kotti.resources import Document, DBSession
from kotti.views.edit.actions import actions as kotti_actions
from kotti.views.edit import ContentSchema
from kotti.views.form import EditFormView, AddFormView, BaseFormView
from kotti.views.form import Form as KForm
from kotti.views.slots import assign_slot
from kotti.util import ViewLink

from . import _
from resources import (
        SnippetCollection,
        Snippet,
        TextSnippet,
        DocumentSlotToSnippet, 
        DocumentSlot,
        )

def actions(context, request):
    if isinstance(context, Document):
        acs = kotti_actions(context, request)
        acs['actions'].append(ViewLink('snippets', title=_(u'Snippets')))
        return acs
    else:
        return kotti_actions(context, request)

def view_collection(context, request):
    return { 'snippets': context.values() }

class TextSnippetSchema(colander.MappingSchema):
    title = colander.SchemaNode(
        colander.String(),
        title=_(u'Title'),
        )    
    body = colander.SchemaNode(
        colander.String(),
        title=_(u'Body'),
        widget=RichTextWidget(theme='advanced', width=790, height=500),
        )
class TextSnippetEditForm(EditFormView):
    schema_factory = TextSnippetSchema

class TextSnippetAddForm(AddFormView):
    schema_factory = TextSnippetSchema
    add = TextSnippet
    item_type = _(u"TextSnippet")

class Form(KForm):
    def __init__(self, *args, **kwargs):
        search_path = (
            resource_filename('kottisnippets', 'templates/forms'),
            ) + Form.default_renderer.loader.search_path
        renderer = ZPTRendererFactory(search_path)
        kwargs['renderer'] = renderer
        super(Form, self).__init__(*args, **kwargs)


def validate_list(node, snippets):
    ids = {}
    for snippet in snippets:
        snippet_id = snippet['snippet']
        ids[snippet_id] = ids.get(snippet_id, 0) + 1
    bad = filter(lambda n: n[1]>1, ids.items())
    if bad:
        raise colander.Invalid(node, 
                _('Snippet may occur only once in the slot'))

class SlotsEditView(BaseFormView):
    form_class = Form
    buttons = ('save',)

    available_slots=[
            (u'left', _("Left Slot")),
            (u'right', _("Right Slot")),
            (u'abovecontent', _("Above Content Slot")),
            (u'belowcontent', _("Below Content Slot")),
            ]

    def __init__(self, *args, **kwargs):
        super(SlotsEditView, self).__init__(*args, **kwargs)
        self.schema = colander.SchemaNode(colander.Mapping(), name="slots")
        for name, title in self.available_slots:
            choices = self._available_snippets(self.request.context, name)
            choices = map(lambda s: ("snippet-%d" % s.id, s.title), choices)
            snippet = colander.SchemaNode(colander.Mapping(), 
                    name="snippet-mapping", title=_(u'Snippet'))
            snippet.add(colander.SchemaNode(colander.String(),
                widget=SelectWidget(values=choices),
                name='snippet'))
            self.schema.add(colander.SchemaNode(colander.Sequence(), 
                snippet, name=name, title=title, missing=[],
                widget=SequenceWidget(orderable=True),
                validator=validate_list))

    def __call__(self, *args, **kwargs):
        return super(SlotsEditView, self).__call__(*args, **kwargs)


    def before(self, form):
        super(SlotsEditView, self).before(form)
        form.widget.item_template = 'form-item'

    def appstruct(self):
        context = self.request.context
        appstruct = {}
        for name, _ in self.available_slots:
            appstruct[name] = self._used_snippets(context, name)
        return appstruct

    def save_success(self, appstruct):
        appstruct.pop('csrf_token', None)
        context = self.request.context
        mapper = lambda snippet: ("snippet-%d" % snippet.id, snippet)
        slots_names = [name for name, title in self.available_slots]
        for slot in context.slots:
            if slot.name in slots_names:
                snippets = self._available_snippets(context, slot.name)
                snippets = dict(map(mapper, snippets))
                while slot.snippets:
                    slot.snippets.pop()
                for snippet in appstruct[slot.name]:
                    snippet_id = snippet['snippet']
                    if snippet_id in snippets:
                        s = snippets[snippet_id]
                        if s not in slot.snippets:
                            slot.snippets.append(snippets[snippet_id])
                del appstruct[slot.name]
        for slot_name in appstruct:
            snippets = self._available_snippets(context, slot_name)
            snippets = dict(map(mapper, snippets))
            slot = DocumentSlot()
            slot.document = context
            slot.name = slot_name
            for snippet in appstruct[slot_name]:
                snippet_id = snippet['snippet']
                if snippet_id in snippets:
                    s = snippets[snippet_id]
                    if s not in slot.snippets:
                        slot.snippets.append(snippets[snippet_id])
        for slot in context.slots:
            if slot.name not in slots_names:
                context.slots.remove(slot)
                DBSession.delete(slot)
        DBSession.flush()
        return HTTPFound(self.request.resource_url(context))

    def _available_snippets(self, context, slot):
        snippets = DBSession.query(Snippet).all()
        return snippets

    def _used_snippets(self, context, slot):
       snippets = DBSession.query(DocumentSlotToSnippet).filter(
               and_(DocumentSlotToSnippet.document_id == context.id,
                   DocumentSlotToSnippet.slot_name == slot))\
                           .order_by(DocumentSlotToSnippet.position).all()
       return [{"snippet": "snippet-%d" % snippet.snippet_id} for 
               snippet in snippets]

def mk_snippet_view(name):
    def view(context, request):
        if hasattr(context, 'slots'):
            for slot in context.slots:
                if slot.name == name and slot.snippets:
                    return {
                            'slot_name': name,
                            'snippets': slot.snippets,
                           }
        raise PredicateMismatch()
    return view

def includeme(config):
    config.add_view(
        actions,
        name='actions-dropdown',
        permission='view',
        renderer='kotti:templates/actions-dropdown.pt',
        )
    config.add_view(
            view_collection,
            context=SnippetCollection,
            name='view',
            permission='edit',
            renderer='kottisnippets:templates/snippet-list.pt',
            )
    config.add_view(
            TextSnippetEditForm,
            context=TextSnippet,
            name='edit',
            permission='edit',
            renderer='kotti:templates/edit/node.pt'
            )
    config.add_view(
            TextSnippetAddForm,
            name=TextSnippet.type_info.add_view,
            permission='add',
            renderer='kotti:templates/edit/node.pt',
            )
    config.add_view(
            SlotsEditView,
            context=Document,
            name='snippets',
            permission='edit',
            renderer='kottisnippets:templates/document-snippets.pt'
            )

    for name, title in SlotsEditView.available_slots:
        config.add_view(mk_snippet_view(name),
                name = '%s-slot-snippets' % name,
                renderer = 'kottisnippets:templates/snippets.pt',
                )
        assign_slot('%s-slot-snippets' % name, name)

