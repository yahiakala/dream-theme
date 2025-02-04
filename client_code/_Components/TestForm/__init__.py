from ._anvil_designer import TestFormTemplate
class TestForm(TestFormTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)
