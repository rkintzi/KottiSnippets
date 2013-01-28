from pyramid.view import render_view_to_response
import venusian
from kotti.views.slots import assign_slot
from pyramid.exceptions import PredicateMismatch
from kottisnippets import _
from resources import TextSnippet, Snippet

default_slots = [
        (u'left', _("Left Slot")),
        (u'right', _("Right Slot")),
        (u'abovecontent', _("Above Content Slot")),
        (u'belowcontent', _("Below Content Slot")),
        ]
registered_slots = {}
registered_slots_names = set()

def get_registered_slots(name):
    return registered_slots.get(name,[])

class provides_slots(object):
    def __init__(self, name, *slots):
        self.name = name
        self.slots = slots

    def __call__(self, view):
        def callback(context, name, ob):
            config = context.config
            config.kotti_snippets(self.name, self.slots)
        info = venusian.attach(view, callback, category='kotti_snippets')
        return view

def render_list(context, request):
    request.orig_context = context
    name = request.POST['slot_name']
    if hasattr(context, 'slots'):
        for slot in context.slots:
            if slot.name == name and slot.snippets:
                view_name = 'kotti_snippets-view-%s-list' % name
                response = render_view_to_response(context, request,
                        name=view_name)
                if response is None:
                    view_name = 'kotti_snippets-view-list'
                    response = render_view_to_response(context, request,
                            name=view_name)
                if response is None:
                    request.snippets = slot.snippets
                    return {
                            'slot_name': name,
                            'snippets': slot.snippets,
                           }
                return response
    raise PredicateMismatch()

def render_snippet(context, request):
    name = request.POST['slot_name']
    view_name = 'kotti_snippets-view-%s-snippet' % name
    response = render_view_to_response(context, request,
            name=view_name)
    if response is None:
        view_name = 'kotti_snippets-view-snippet'
        response = render_view_to_response(context, request,
                name=view_name)
    if response is None:
        raise PredicateMismatch()
    return response

def render_text_snippet(context, request):
    return { 
            'slot_name': name,
            'snippet': context 
            }

def _register_slot(config, view_name, slots):
    if not slots:
        raise ConfigurationError("Parameter `slots' may not be empty")
    if view_name in registered_slots:
        raise ConfigurationError("There are slots already registerd "
            "for view `%s'" % view_name)
    for name, title in list(slots):
        if name not in registered_slots_names:
            params = dict(slot_name = name)
            assign_slot('kotti_snippets-render-list', name, params=params)
            registered_slots_names.add(name)
    registered_slots[view_name] = slots

def _register_default_slots_if_needed(config):
    if 'view' not in registered_slots:
        _register_slot(config, 'view', default_slots)

def _register_slot_directive(config, view_name, *slots):
    config.action('kotti_snippets', _register_slot, 
            (config, view_name, slots), order=0)

def includeme(config):
    config.add_view(render_list,
            name='kotti_snippets-render-list',
            renderer = 'kottisnippets:templates/render-list.pt',
            )
    config.add_view(render_text_snippet,
            context=TextSnippet,
            name='kotti_snippets-view-snippet',
            renderer = 'kottisnippets:templates/render-snippet.pt',
            )
    config.add_view(render_snippet,
            context=Snippet,
            name='kotti_snippets-render-snippet',
            )
    config.action('kotti_snippets', _register_default_slots_if_needed, 
            (config, ), order=1)
    config.add_directive('register_slot', 'kottisnippets.config._register_slot_directive')
    config.include('.view')
