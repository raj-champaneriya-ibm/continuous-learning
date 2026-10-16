"""Protect keyboard access, decorative icons, and escaped workflow details."""
from html.parser import HTMLParser

import pytest
from acme.ui_bits import icon, pipeline


class Elements(HTMLParser):
    def __init__(self, markup):
        super().__init__()
        self.elements = []
        self.feed(markup)

    def handle_starttag(self, tag, attrs):
        self.elements.append((tag, dict(attrs)))


def test_pipeline_keyboard_order_and_untrusted_details():
    markup = pipeline([{"step": "5", "status": "ok", "detail": '<script>alert("x")</script>'}])
    nodes = Elements(markup).elements
    buttons = [attrs for tag, attrs in nodes if tag == 'button']
    assert [a['data-step'] for a in buttons] == ['1','2','3','4','5','6','7','H','8','9']
    assert all(a['type'] == 'button' for a in buttons)
    assert not any(tag == 'script' for tag, _ in nodes)
    assert buttons[4]['title'] == '<script>alert("x")</script>'


def test_icons_have_no_network_or_accessible_name():
    for name in ['review','play','cases','knowledge','score','settings','save','check','close','back','next']:
        markup = str(icon(name))
        svg = next(a for tag, a in Elements(markup).elements if tag == 'svg')
        assert svg['aria-hidden'] == 'true'
        assert svg['focusable'] == 'false'
        assert 'href=' not in markup
    with pytest.raises(ValueError):
        icon('../unknown')
