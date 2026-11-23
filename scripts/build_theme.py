import colorsys, json, sys

def hsl(h, s, l):
    r, g, b = colorsys.hls_to_rgb(h / 360, l / 100, s / 100)
    return "#%02x%02x%02x" % tuple(round(x * 255) for x in (r, g, b))

def a(c, alpha):  # hex + alpha byte
    return c + "%02x" % round(alpha * 255)

# Shared Things palette (theme.css body{})
blue, pink, green, yellow, orange, red, purple = "#2e80f2", "#ff82b2", "#3eb4bf", "#e5b567", "#e87d3e", "#e83e3e", "#9e86c8"

def variant(name, appearance, base, text, muted, faint, accent, atom, sel_alpha):
    bg, code_bg, side_bg, line, border = base
    syntax = {
        # Markdown — mirrors Things' strong/em/quote/heading colours
        "title": {"color": text, "font_weight": 700},
        "emphasis": {"color": pink, "font_style": "italic"},
        "emphasis.strong": {"color": pink, "font_weight": 700},
        "text.literal": {"color": atom["red"]},
        "link_text": {"color": accent},
        "link_uri": {"color": accent},
        "punctuation.markup": {"color": faint},
        "punctuation.list_marker": {"color": faint},
        "punctuation.special": {"color": green},
        # Code — Things uses the Atom One palette for code blocks
        "comment": {"color": atom["gray1"], "font_style": "italic"},
        "keyword": {"color": atom["purple"]},
        "string": {"color": atom["green"]},
        "number": {"color": atom["orange"]},
        "boolean": {"color": atom["orange"]},
        "constant": {"color": atom["orange"]},
        "function": {"color": atom["blue"]},
        "type": {"color": atom["yellow"]},
        "property": {"color": atom["red"]},
        "attribute": {"color": atom["orange"]},
        "tag": {"color": atom["red"]},
        "variable": {"color": text},
        "operator": {"color": atom["aqua"]},
        "punctuation": {"color": muted},
        "embedded": {"color": text},
    }
    style = {
        "background": side_bg,
        "surface.background": side_bg,
        "elevated_surface.background": code_bg,
        "panel.background": side_bg,
        "title_bar.background": side_bg,
        "title_bar.inactive_background": side_bg,
        "status_bar.background": side_bg,
        "tab_bar.background": side_bg,
        "toolbar.background": bg,
        "tab.active_background": bg,
        "tab.inactive_background": side_bg,
        "editor.background": bg,
        "editor.foreground": text,
        "editor.gutter.background": bg,
        "editor.line_number": faint,
        "editor.active_line_number": muted,
        "editor.active_line.background": a(line, 0.5),
        "editor.wrap_guide": a(border, 0.6),
        "editor.indent_guide": a(border, 0.6),
        "editor.indent_guide_active": border,
        "text": text,
        "text.muted": muted,
        "text.placeholder": faint,
        "text.accent": accent,
        "icon": muted,
        "icon.muted": faint,
        "icon.accent": accent,
        "border": border,
        "border.variant": a(border, 0.6),
        "border.focused": accent,
        "element.background": code_bg,
        "element.hover": line,
        "element.selected": a(accent, 0.2),
        "ghost_element.hover": line,
        "ghost_element.selected": a(accent, 0.2),
        "scrollbar.thumb.background": a(muted, 0.25),
        "scrollbar.track.background": "#00000000",
        "search.match_background": a("#ffd000", 0.4),
        "link_text.hover": accent,
        "error": red, "warning": orange, "success": green, "info": blue,
        "hint": faint, "modified": yellow, "created": green, "deleted": red,
        # Status backgrounds/borders: unset ones come out as solid colour, which made
        # the selected "Preview" toggle (blue label on blue fill) unreadable.
        **{f"{k}.background": a(c, 0.15) for k, c in
           [("error", red), ("warning", orange), ("success", green), ("info", accent),
            ("hint", faint), ("modified", yellow), ("created", green), ("deleted", red)]},
        **{f"{k}.border": c for k, c in
           [("error", red), ("warning", orange), ("success", green), ("info", accent),
            ("hint", faint), ("modified", yellow), ("created", green), ("deleted", red)]},
        "element.active": a(accent, 0.25),
        "ghost_element.active": a(accent, 0.25),
        "players": [{"cursor": accent, "background": accent, "selection": a(accent, sel_alpha)}],
        "syntax": syntax,
    }
    return {"name": name, "appearance": appearance, "style": style}

dark = variant(
    "Things Dark", "dark",
    ("#1c2127", "#282c34", "#181c20", "#2c313c", "#35393e"),
    "#dadada", hsl(212, 15, 78), hsl(212, 15, 43), hsl(215, 75, 70),
    dict(gray1="#5c6370", red="#e06c75", orange="#d19a66", green="#98c379",
         aqua="#56b6c2", purple="#c678dd", blue="#61afef", yellow="#e5c07b"),
    0.25)
light = variant(
    "Things Light", "light",
    ("#ffffff", "#f6f7f8", "#f6f7f8", "#f0f0f0", "#ebedf0"),
    "#222222", hsl(212, 10, 37), hsl(212, 10, 67), hsl(215, 75, 60),
    dict(gray1="#a0a1a7", red="#e75545", orange="#986800", green="#4ea24c",
         aqua="#0084bc", purple="#a625a4", blue="#3d74f6", yellow="#c18401"),
    0.2)

json.dump({"$schema": "https://zed.dev/schema/themes/v0.2.0.json",
           "name": "Things", "author": "Dmytro Durach, ported from the Things theme for Obsidian by Colin Eckert",
           "themes": [light, dark]}, open(sys.argv[1], "w"), indent=2)
