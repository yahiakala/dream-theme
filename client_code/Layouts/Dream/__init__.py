from ._anvil_designer import DreamTemplate
class Dream(DreamTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)
