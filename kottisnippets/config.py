import venusian
from kotti.views.slots import assign_slot
from pyramid.exceptions import PredicateMismatch
from kottisnippets import _

default_slots = [
        (u'left', _("Left Slot")),
        (u'right', _("Right Slot")),
        (u'abovecontent', _("Above Content Slot")),
        (u'belowcontent', _("Below Content Slot")),
        ]
registered_slots = {}

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
    
def view(context, request):
    name = request.POST['slot_name']
    if hasattr(context, 'slots'):
        for slot in context.slots:
            if slot.name == name and slot.snippets:
                return {
                        'slot_name': name,
                        'snippets': slot.snippets,
                        }
    raise PredicateMismatch()

def _register_slot(config, view_name, slots):
    if not slots:
        raise ConfigurationError("Parameter `slots' may not be empty")
    if view_name in registered_slots:
        raise ConfigurationError("There are slots already registerd "
            "for view `%s'" % view_name)
    for name, title in list(slots):
        params = dict(slot_name = name)
        assign_slot('kotti-snippets-view', name, params=params)
    registered_slots[view_name] = slots

def _register_default_slots_if_needed(config):
    if 'view' not in registered_slots:
        _register_slot(config, 'view', default_slots)

def _register_slot_directive(config, view_name, *slots):
    config.action('kotti_snippets', _register_slot, 
            (config, view_name, slots), order=0)

def includeme(config):
    config.add_view(view,
            name='kotti-snippets-view',
            renderer = 'kottisnippets:templates/snippets.pt',
            )
    config.action('kotti_snippets', _register_default_slots_if_needed, 
            (config, ), order=1)
    config.add_directive('register_slot', 'kottisnippets.config._register_slot_directive')
    config.include('.view')
