from PIL import Image, ImageFilter, ImageDraw, ImageFont, ImageEnhance

class Effects():

    @staticmethod
    def rounded(im, rad=5, width=None, height=None, _scale=1):
        im = Image.open(im)

        if width is None and height is None: width, height = im.size[0], im.size[1]
        im = im.resize((int(width / _scale), int(height / _scale)), Image.ANTIALIAS)

        circle = Image.new('L', (rad * 2, rad * 2), 0)

        draw = ImageDraw.Draw(circle)
        draw.ellipse((0, 0, rad * 2, rad * 2), fill=255)

        alpha = Image.new('L', im.size, 255)
        w, h = im.size

        alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
        alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, h - rad))
        alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0))
        alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (w - rad, h - rad))

        im.putalpha(alpha)

        return im

    @staticmethod
    def text(image, name='Name', artist='Artist'):
        draw = ImageDraw.Draw(image)

        f1, s1, l1, c1 = 528, 40, 0, 0
        f2, s2, l2, c2 = 535, 40, 0, 0

        font = ImageFont.truetype("Data/Ultralight.ttf", s1)
        font1 = ImageFont.truetype("Data/Heavy.ttf", s2)
        font2 = ImageFont.truetype("Data/Heavy.ttf", 20)

        font_size = font.getsize(name)
        font_size1 = font1.getsize(artist)

        if font_size[0] > f1:
            temp = s1
            while font_size[0] > f1:
                font = ImageFont.truetype("Data/Ultralight.ttf", temp)
                font_size = font.getsize(name)
                temp, l1 = temp - 1, l1 + 1

        if font_size1[0] > f2:
            temp = s2
            while font_size1[0] > f2:
                font1 = ImageFont.truetype("Data/Heavy.ttf", temp)
                font_size1 = font1.getsize(artist)
                temp, l2 = temp - 1, l2 + 1

        c1, c2 = (f1 - font_size[0]) / 2, (f2 - font_size1[0]) / 2

        draw.text((520 + c1, 150 + l1 * 2), name, (255,255,255), font=font)
        draw.text((520 + c2, 250), artist, (255,255,255), font=font1)
        draw.text((665, 365), 'Spotify Music Downloader', (255,255,255), font=font2)

        return image

    @staticmethod
    def createPoster(image, name='Name', artist='Artist', file='image.png'):
        original = Image.open(image)
        logo = Image.open('Data/logo-w.png')
        logo = logo.resize((20, 20), Image.ANTIALIAS)

        rounded = Effects.rounded(image, rad=30)
        rounded = rounded.resize((440, 440), Image.ANTIALIAS)

        image = Image.open(image)
        image = image.resize((1080, 1080), Image.ANTIALIAS)
        width, height = image.size

        left, right, top, bottom = 0,  width, height/4, 3 * height/4
        cropped = image.crop((left, top, right, bottom))
        blurred = cropped.filter(ImageFilter.GaussianBlur(radius=40))
        enhancer = ImageEnhance.Brightness(blurred)
        enhanced_im = enhancer.enhance(.6)
        enhanced_im.paste(rounded, (50, 50), rounded)
        enhanced_im.paste(logo, (635, 368), logo)
        enhanced_im = Effects.text(enhanced_im, name, artist)
        enhanced_im.save(file)


if __name__ == "__main__":
    Effects.createPoster('image.jpg', name='Hard EP', artist='The Neighbourhood', file='Downloads/image.png')
