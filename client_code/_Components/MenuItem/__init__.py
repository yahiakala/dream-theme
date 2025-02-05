from ._anvil_designer import MenuItemTemplate
from anvil import *
from anvil import HtmlTemplate

from ..._utils.properties import (
    anvil_prop,
    bold_property,
    color_property,
    font_family_property,
    font_size_property,
    italic_property,
    spacing_property,
    tooltip_property,
    underline_property,
)


class MenuItem(MenuItemTemplate):
    def __init__(self, **properties):
        self.tag = ComponentTag()
        self._props = properties
        self._tooltip_node = None
        self.init_components(**properties)
        self.dom_nodes['anvil-m3-menuItem-container'].addEventListener(
            "click", self._handle_click
        )

    italic = italic_property('anvil-m3-menuItem-labelText')
    bold = bold_property('anvil-m3-menuItem-labelText')
    underline = underline_property('anvil-m3-menuItem-labelText')
    font_size = font_size_property('anvil-m3-menuItem-labelText')
    leading_icon_size = font_size_property(
        'anvil-m3-menuItem-leadingIcon', 'leading_icon_size'
    )
    trailing_icon_size = font_size_property(
        'anvil-m3-menuItem-trailingIcon', 'trailing_icon_size'
    )
    font_family = font_family_property('anvil-m3-menuItem-labelText', 'font_family')
    text_color = color_property('anvil-m3-menuItem-labelText', 'color', 'text_color')
    trailing_icon_color = color_property(
        'anvil-m3-menuItem-trailingIcon', 'color', 'trailing_icon_color'
    )
    leading_icon_color = color_property(
        'anvil-m3-menuItem-leadingIcon', 'color', 'leading_icon_color'
    )
    background_color = color_property(
        'anvil-m3-menuItem-container', 'backgroundColor', 'background'
    )
    visible = HtmlTemplate.visible
    spacing = spacing_property('anvil-m3-menuItem-container')
    tooltip = tooltip_property('anvil-m3-menuItem-container')

    @anvil_prop
    def text(self, value):
        self.dom_nodes['anvil-m3-menuItem-labelText'].innerText = value

    @anvil_prop
    def leading_icon(self, value):
        self.dom_nodes["anvil-m3-menuItem-leadingIcon"].innerHTML = value[3:] or " "
        if value:
            self.dom_nodes["anvil-m3-menuItem-leadingIcon"].classList.add(
                "anvil-m3-menuItem-showLeadingIcon"
            )
        elif not value and not self.add_icon_space:
            self.dom_nodes["anvil-m3-menuItem-leadingIcon"].classList.remove(
                "anvil-m3-menuItem-showLeadingIcon"
            )

    @anvil_prop
    def trailing_icon(self, value):
        self.dom_nodes["anvil-m3-menuItem-trailingIcon"].innerText = value[3:]

    @anvil_prop
    def trailing_text(self, value):
        self.dom_nodes["anvil-m3-menuItem-trailingText"].innerText = value

    @anvil_prop
    def add_icon_space(self, value):
        if value:
            self.dom_nodes["anvil-m3-menuItem-leadingIcon"].classList.add(
                "anvil-m3-menuItem-showLeadingIcon"
            )
        elif not self.leading_icon and not value:
            self.dom_nodes["anvil-m3-menuItem-leadingIcon"].classList.remove(
                "anvil-m3-menuItem-showLeadingIcon"
            )

    @anvil_prop
    def enabled(self, value):
        self.dom_nodes["anvil-m3-menuItem-container"].classList.toggle(
            "anvil-m3-menuItem-disabled", not value
        )

    def _handle_click(self, event):
        event.preventDefault()
        self.raise_event(
            "click",
            event=event,
            keys={
                "shift": event.shiftKey,
                "alt": event.altKey,
                "ctrl": event.ctrlKey,
                "meta": event.metaKey,
            },
        )

    def _anvil_get_interactions_(self):
        return [
            {
                "type": "whole_component",
                "title": "Edit text",
                "icon": "edit",
                "default": True,
                "callbacks": {
                    "execute": lambda: anvil.designer.start_inline_editing(
                        self, "text", self.dom_nodes['anvil-m3-menuItem-labelText']
                    )
                },
            }
        ]
