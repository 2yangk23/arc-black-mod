import os
import re
import fnmatch

def recolor(rgb):
    red = float(rgb[0])
    green = float(rgb[1])
    blue = float(rgb[2])

    # determine if recolor necessary
    if red == 0 or green == 0 or blue == 0:
        return rgb
    if not (red < green and green < blue):
        return rgb
    red_green_ratio = green / red
    if not (red_green_ratio >= 1.05 and red_green_ratio <= 1.15):
        return rgb
    green_blue_ratio = blue / green
    if not (green_blue_ratio >= 1.1 and green_blue_ratio <= 1.30):
        return rgb
    
    if red < 128:
        newColor = int(red * 0.75)
    else:
        newColor = int(red)
    return (newColor, newColor, newColor)

def sub_hex(hexMatch):
    match = hexMatch.group(0) # '#RRGGBB'
    match = match.lstrip('#')
    rgb = tuple(int(match[i:i+2], 16) for i in (0, 2 ,4))
    newColor = recolor(rgb)
    if newColor == rgb:
        return '#%s' % match
    return '#%02x%02x%02x' % newColor

def sub_rgb(rgbMatch):
    match = rgbMatch.group(2) # 'R, G, B'
    colors = re.split(r', *', match)
    rgb = tuple(map(int, colors))
    newColor = recolor(rgb)
    if newColor == rgb:
        result = match
    else:
        result = "%d, %d, %d" % (newColor[0], newColor[1], newColor[2])
    return rgbMatch.group(1) + result + (rgbMatch.group(3) or "") + rgbMatch.group(4)

def recolor_files(match, root):
    for path, dirs, files in os.walk(root):
        for filename in fnmatch.filter(files, match):
            filepath = os.path.join(path, filename)
            with open(filepath) as f:
                data = f.read()
            print("Recoloring: %s" % filepath)
            data = re.sub(r'#[0-9A-Fa-f]{6}', sub_hex, data)
            data = re.sub(r'(rgba?\()([0-9]{1,3}, *[0-9]{1,3}, *[0-9]{1,3})(, *[0-9.]+)?(\))', sub_rgb, data)
            data = re.sub(r'(\[ ?)([0-9]{1,3}, *[0-9]{1,3}, *[0-9]{1,3})(, *[0-9.]+)?( ?\])', sub_rgb, data)
            # Lighten the text color
            data = data.replace('#D3DAE3', '#F3F3F3')
            data = data.replace('#d3dae3', '#F3F3F3')
            with open(filepath, "w") as f:
                f.write(data)

recolor_files("*.svg", "ArcAurorae")
recolor_files("*rc", "ArcAurorae")

recolor_files("*.svg", "ArcGtk")

recolor_files("*.kvconfig", "ArcKvantum")
recolor_files("*.svg", "ArcKvantum")
