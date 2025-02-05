from ._anvil_designer import AccountTemplate
from anvil.js.window import document
from ..._utils import fui, noop
from ..._utils.properties import (
    anvil_prop,
    color_property,
    innerText_property,
)


class Account(AccountTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)
        self._props = properties
        self._cleanup = noop
        self._menuNode = self.dom_nodes['account-menu-container']
        self._btnNode = self.dom_nodes['account-expand']
        self._open = False
        self._has_focus = False
        self._hoverIndex = None
        self._children = None
        
        self._btnNode.addEventListener('click', self._handle_click)
        
        self.add_event_handler("x-anvil-page-added", self._on_mount)
        self.add_event_handler("x-anvil-page-removed", self._on_cleanup)

    def _on_mount(self, **event_args):
        document.addEventListener('click', self._body_click)
        document.addEventListener('keydown', self._handle_keyboard_events)
        # Move menu to body to avoid container clipping
        document.body.append(self._menuNode)
        self._setup_fui()

    def _on_cleanup(self, **event_args):
        document.removeEventListener('click', self._body_click)
        document.removeEventListener('keydown', self._handle_keyboard_events)
        self._cleanup()
        self._menuNode.remove()

    def _setup_fui(self):
        if self._open:
            self._cleanup()
            self._cleanup = fui.auto_update(
                self._btnNode,
                self._menuNode,
                placement="bottom-start"
            )

    def _handle_click(self, event):
        self._toggle_menu_visibility()
        self.raise_event('click')

    def _toggle_menu_visibility(self, value=None):
        if value is None:
            value = not self._open
        
        self._open = value
        self._menuNode.classList.toggle('account-menu-hidden', not value)
        
        if value:
            self._setup_fui()
            icon = self._btnNode.querySelector('.material-icons')
            icon.innerText = 'expand_less'
            # Get children for keyboard navigation
            self._children = self.get_components()
            self._hoverIndex = 0 if self._children else None
            self._update_hover_styles()
        else:
            self._cleanup()
            icon = self._btnNode.querySelector('.material-icons')
            icon.innerText = 'expand_more'
            self._hoverIndex = None
            self._clear_hover_styles()

    def _body_click(self, event):
        if (self._btnNode.contains(event.target) or 
                self._menuNode.contains(event.target)):
            return
        self._toggle_menu_visibility(False)

    def _handle_keyboard_events(self, event):
        if not self._open:
            return
        action_keys = set(["ArrowUp", "ArrowDown", "Tab", "Escape", " ", "Enter"])
        if event.key not in action_keys:
            return

        if event.key in ["ArrowUp", "ArrowDown"]:
            self._iterate_hover(event.key == "ArrowDown")
            event.preventDefault()
            return

        if event.key in ["Tab", "Escape"]:
            self._toggle_menu_visibility(False)

        if event.key in [" ", "Enter"]:
            self._attempt_select(event)

    def _iterate_hover(self, inc=True):
        if not self._children:
            return
            
        if inc:
            if self._hoverIndex is None or self._hoverIndex >= len(self._children) - 1:
                self._hoverIndex = -1
            self._hoverIndex += 1
        else:
            if self._hoverIndex is None or self._hoverIndex == 0:
                self._hoverIndex = len(self._children)
            self._hoverIndex -= 1

        self._children[self._hoverIndex].dom_nodes[
            'anvil-m3-menuItem-container'
        ].scrollIntoView({'block': 'nearest'})
        self._update_hover_styles()

    def _attempt_select(self, event):
        if self._hoverIndex is not None and self._children:
            self._children[self._hoverIndex].raise_event(
                "click",
                event=event,
                keys={
                    "shift": event.shiftKey,
                    "alt": event.altKey,
                    "ctrl": event.ctrlKey,
                    "meta": event.metaKey,
                },
            )
        self._toggle_menu_visibility(False)

    def _clear_hover_styles(self):
        if self._children:
            for child in self._children:
                child.dom_nodes['anvil-m3-menuItem-container'].classList.toggle(
                    'anvil-m3-menuItem-container-keyboardHover', False
                )

    def _update_hover_styles(self):
        self._clear_hover_styles()
        if self._hoverIndex is not None and self._children:
            self._children[self._hoverIndex].dom_nodes[
                'anvil-m3-menuItem-container'
            ].classList.toggle('anvil-m3-menuItem-container-keyboardHover', True)

    username = innerText_property('account-username', 'username')
    plan = innerText_property('account-plan', 'plan')
    avatar_text = innerText_property('account-avatar', 'avatar_text')
    menu_background_color = color_property(
        'account-menu-container',
        'backgroundColor',
        'menu_background_color'
    )

    @anvil_prop
    def menu_items(self, value=[]):
        """A list of menu items to display in the dropdown"""
        self._props['menu_items'] = value
        # Clear existing items
        for c in self.get_components():
            self.remove_component(c)
        # Add new items
        for item in value:
            self.add_component(item, slot='account-menu-slot')
