from ._anvil_designer import AccountTemplate
from anvil.js import window
from ..._utils.properties import innerHTML_property

class Account(AccountTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)
        self.dom_nodes['account-expand'].addEventListener('click', self._handle_click)

    def _handle_click(self, e):
        self.raise_event('click')

    @property
    def username(self):
        return self.dom_nodes['account-username'].innerText

    @username.setter
    def username(self, value):
        self.dom_nodes['account-username'].innerText = value

    @property
    def plan(self):
        return self.dom_nodes['account-plan'].innerText

    @plan.setter
    def plan(self, value):
        self.dom_nodes['account-plan'].innerText = value

    @property
    def avatar_text(self):
        return self.dom_nodes['account-avatar'].innerText

    @avatar_text.setter
    def avatar_text(self, value):
        self.dom_nodes['account-avatar'].innerText = value
