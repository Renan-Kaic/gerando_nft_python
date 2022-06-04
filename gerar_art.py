from PIL import Image, ImageDraw, ImageChops
import os
from random import randint, random
import colorsys
os.system("cls")


def gerar_cor():
    h = random()
    s = 1
    v = 1

    float_rgb = colorsys.hsv_to_rgb(h, s, v)
    rgb = [int(x*255) for x in float_rgb]
    return tuple(rgb)


def interpolate(corInicio, corFim, fator: float):
    recip = 1 - fator

    return(
        int(corInicio[0] * recip + corFim[0] * fator),
        int(corInicio[1] * recip + corFim[1] * fator),
        int(corInicio[2] * recip + corFim[2] * fator)
    )


def gerar_art(path: str):

    target_size_px = 250
    factor_size = 2

    tam_image = target_size_px * factor_size
    padding = 16 * factor_size
    cor_imagem = (0, 0, 0)
    cor_inicial = gerar_cor()
    cor_final = gerar_cor()
    image = Image.new("RGB",
                      size=(tam_image, tam_image),
                      color=cor_imagem)

    # Desenhando as linhas

    draw = ImageDraw.Draw(image)
    pontos = []

    # Gerando os pontos
    for _ in range(15):
        ponto = (
            randint(padding, tam_image-padding),
            randint(padding, tam_image-padding)
        )

        pontos.append(ponto)

    min_x = min([p[0] for p in pontos])
    max_x = max([p[0] for p in pontos])
    min_y = min([p[1] for p in pontos])
    max_y = max([p[1] for p in pontos])
    #draw.rectangle((min_x, min_y, max_x, max_y), outline=(255, 0, 0))

    delta_x = min_x - (tam_image - max_x)
    delta_y = min_y - (tam_image - max_y)

    for i, point in enumerate(pontos):
        pontos[i] = (point[0] - delta_x // 2, point[1] - delta_y // 2)

    min_x = min([p[0] for p in pontos])
    max_x = max([p[0] for p in pontos])
    min_y = min([p[1] for p in pontos])
    max_y = max([p[1] for p in pontos])
    #draw.rectangle((min_x, min_y, max_x, max_y), outline=(0, 128, 0))

    # Desenhando os pontos
    ness = 0
    n_pontos = len(pontos) - 1
    for i, point in enumerate(pontos):
        overlay_image = Image.new("RGB",
                                  size=(tam_image, tam_image),
                                  color=cor_imagem)
        overlay_draw = ImageDraw.Draw(overlay_image)

        p1 = point

        if i == n_pontos:
            p2 = pontos[0]
        else:
            p2 = pontos[i + 1]

        linha_xy = ((p1), (p2))

        color_fact = i / n_pontos
        cor_linha = interpolate(cor_inicial, cor_final, color_fact)
        #cor_linha = (randint(0, 255), randint(0, 255), randint(0, 255))
        ness += factor_size
        overlay_draw.line(linha_xy, fill=cor_linha, width=ness)
        image = ImageChops.add(image, overlay_image)

    image = image.resize((target_size_px, target_size_px),
                         resample=Image.Resampling.LANCZOS)
    image.save(path)
    print("Arte gerada com sucesso!")


if __name__ == "__main__":
    # for i in range(1, 25):
    #  gerar_art(f"arts/art{i}.png")
    gerar_art("art.png")
