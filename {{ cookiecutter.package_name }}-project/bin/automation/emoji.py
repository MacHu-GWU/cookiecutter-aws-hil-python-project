# -*- coding: utf-8 -*-

"""
Enumerate useful, UTF8 emoji characters.

Full list is here: https://unicode.org/emoji/charts/full-emoji-list.html
"""


class Emoji:
    start_timer = "โฑ"
    end_timer = "โฐ"
    start = "โฏ"
    end = "โน"
    error = "๐ฅ"

    relax = "๐ด"

    test = "๐งช"
    install = "๐พ"
    build = "๐ช"
    deploy = "๐"
    delete = "๐"
    tada = "๐"

    cloudformation = "๐"
    awslambda = "ฮป"
    s3 = "๐ชฃ"

    template = "๐"
    computer = "๐ป"
    package = "๐ฆ"
    email = "๐ซ"
    factory = "๐ญ"
    no_entry = "๐ซ"
    warning = "โ"

    thumb_up = "๐"
    thumb_down = "๐"
    attention = "๐"

    happy_face = "๐"
    hot_face = "๐ฅต"
    anger = "๐ข"

    red_circle = "๐ด"
    green_circle = "๐ข"
    yellow_circle = "๐ก"
    blue_circle = "๐ต"

    red_square = "๐ฅ"
    green_square = "๐ฉ"
    yellow_square = "๐จ"
    blue_square = "๐ฆ"

    succeeded = "โ"
    failed = "โ"

    arrow_up = "โฌ"
    arrow_down = "โฌ"
    arrow_left = "โฌ"
    arrow_right = "โก"

    python = "๐"

    install_phase = "๐ฑ"
    pre_build_phase = "๐ฟ"
    build_phase = "๐"
    post_build_phase = "๐ฒ"

    technologist = "๐ง"


if __name__ == "__main__":
    chars = list()
    for k, v in Emoji.__dict__.items():
        if not k.startswith("_"):
            if len(v) != 1:
                print(f"{k} = {v}, len = {len(v)}")

            # if len(v) == 1:
            chars.append(v)

    print(" ".join(chars))