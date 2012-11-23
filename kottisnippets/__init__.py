
from pyramid.i18n import TranslationStringFactory

_ = TranslationStringFactory('KottiSnippets')

def kotti_configure(settings):
    settings['pyramid.includes'] += ' kottisnippets.view'
    settings['kotti.available_types'] += ' kottisnippets.resources.Snippet'
    settings['kotti.populators'] += ' kottisnippets.populator.populator'

