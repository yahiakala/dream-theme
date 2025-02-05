from ._anvil_designer import AccountTemplate
class Account(AccountTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)
