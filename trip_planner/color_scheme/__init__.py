def _represent_palette(palette, prefix=''):
    prefix = prefix + '-' if prefix else ''
    return {f'{prefix}{name}'.replace('_', '-'): color
            for name, color in palette.items()}


base_colors = dict(
    rich_black='hsl(216, 100%, 4%)',
    crayola_green='hsl(94, 69%, 73%)',
    denim_blue='hsl(214, 70%, 43%)',
    fiery_rose='hsl(356, 82%, 66%)'
    )

# === Palettes ===
# Generated with https://fffuel.co/pppalette/

crayola_green_earth = [
    'hsl(94, 40%, 66%)',
    'hsl(94, 40%, 60%)',
    'hsl(94, 40%, 54%)',
    'hsl(94, 40%, 47%)',
    'hsl(94, 40%, 42%)',
    'hsl(94, 40%, 36%)',
    ]

crayola_green_cooler = [
    'hsl(94, 69%, 73%)',
    'hsl(141, 71%, 73%)',
    'hsl(166, 74%, 65%)',
    'hsl(181, 73%, 61%)',
    'hsl(190, 85%, 67%)',
    'hsl(201, 89%, 74%)',
    ]

fiery_rose_analogous = [
    'hsl(356, 81%, 36%)',
    'hsl(356, 81%, 66%)',
    'hsl(356, 81%, 79%)',
    'hsl(328, 81%, 79%)',
    'hsl(328, 81%, 66%)',
    'hsl(328, 81%, 34%)',
    ]

denim_blue_neon = [
    'hsl(214, 90%, 70%)',
    'hsl(214, 90%, 65%)',
    'hsl(214, 90%, 60%)',
    'hsl(214, 90%, 55%)',
    'hsl(214, 90%, 50%)',
    'hsl(214, 90%, 45%)',
    ]

# "Brand" palettes

_primary = {
    'main': base_colors['crayola_green'],
    'text': 'white',
    'border': crayola_green_earth[5]
    }

_accent = {
    'main': base_colors['denim_blue'],
    'text': 'white',
    'border': denim_blue_neon[4]
    }

brand_palettes = dict(primary=_represent_palette(_primary),
                      accent=_represent_palette(_accent))

# Exposed colors

exposed = _represent_palette({**base_colors})
