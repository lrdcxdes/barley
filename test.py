from PIL import Image, ImageFont, ImageDraw


jobs = {'Страны': True, 'Фикс ферм и видеокарт': True,
        'Новые префиксы': True,
        'Функция автоматическая оплата налога с баланса банка': True,
        'Создание личных промокодов': True, 'Гривны / Евро': True,
        'Топ по рефералам ': True, 'Игра камень-ножницы-бумага': True, 'Видеокарты продаются вместе с фермой': True,
        'Префиксы будут повышать шанс выиграть в играх ': True, 'Игровые боссы': True,
        'Магазин предметов': True, 'Скины': True}


background = Image.open("assets/background.jpg")

font = ImageFont.truetype("assets/font.ttf", 42)
font2 = ImageFont.truetype("assets/font.ttf", 62)

z = (0, 0, 0)  # (0, 0, 0)
d = (255, 255, 255)
color = d
color2 = z
green, red = (0, 255, 0), (255, 0, 0)


poltora = (background.size[0] // 2, background.size[1] // 2)


def create_image():
    source = background.copy()
    draw = ImageDraw.Draw(source)

    y = poltora[1] - poltora[1] // 2
    text = list(jobs.keys())[3] + ' — В ПРОЦЕССЕ\n'
    text1 = '\n'.join(i + f' — В ПРОЦЕССЕ\n' for i in jobs.keys())

    w, h = font.getsize(text)[0] + 40, 785

    coords = [(10, y-10), (w, h)]

    draw.rounded_rectangle(coords, 20, (50, 50, 50))

    for txt, status in jobs.items():
        text = f'{txt} — '
        x = 30
        draw.text((x, y), text, color, font=font,
                  stroke_fill=color2, stroke_width=1, align='left')
        x += font.getsize(text)[0]
        colr = green if status else red
        text = f'{"СДЕЛАНО" if status else "В ПРОЦЕССЕ..."}'
        draw.text((x, y), text, colr, font=font,
                  stroke_fill=color2, stroke_width=1, align='left')
        y += font.size

    draw.text((1200, background.size[1]-70), f'{percent}% из 100% выполнено', font=font2)

    source.draft('RGB', (1008, 756))
    source.save('assets/output.jpg', 'JPEG', quality=100)
    source.show('OutPut')


xd = sum(1 for i in jobs.items() if i[1])
percent = round((xd / len(jobs)) * 100)


create_image()
