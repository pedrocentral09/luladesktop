"""
Generate MST (Movimento dos Sem Terra) assets:
- Meme image: Ocupação do Monitor / Reforma Agrária Digital
- Drop sprite: Barraca vermelha de acampamento do MST
- Decree text note
"""
from PIL import Image, ImageDraw
import os
import math

def generate_mst_assets():
    os.makedirs('assets/memes', exist_ok=True)
    os.makedirs('assets/drops', exist_ok=True)
    os.makedirs('assets/notes', exist_ok=True)

    # 1. Drop: Barraca Vermelha do MST (32x24 px)
    tent = Image.new('RGBA', (36, 28), (0, 0, 0, 0))
    d = ImageDraw.Draw(tent)
    # Triangular tent (Red canvas with black shadow)
    # Base shadow
    d.polygon([(4, 25), (32, 25), (34, 27), (2, 27)], fill=(20, 20, 20, 180))
    # Tent body (Red tarp)
    d.polygon([(18, 5), (4, 25), (32, 25)], fill=(215, 25, 25, 255), outline=(150, 10, 10, 255))
    # Tent entrance flap (Black tarp interior)
    d.polygon([(18, 12), (12, 25), (24, 25)], fill=(30, 30, 35, 255))
    # Support pole
    d.line([18, 5, 18, 25], fill=(180, 140, 60, 255), width=1)
    # Tiny MST flag on top of the tent!
    d.line([18, 1, 18, 5], fill=(120, 120, 120, 255), width=1)
    d.polygon([(18, 1), (26, 3), (18, 5)], fill=(230, 20, 20, 255))
    d.ellipse([21, 2, 23, 4], fill=(255, 255, 255, 255)) # tiny emblem
    tent.save('assets/drops/barraca_mst.png')

    # 2. Meme Gráfico: Invasão e Ocupação do MST (300x240 px)
    mst_meme = Image.new('RGB', (310, 245), (252, 248, 240))
    d = ImageDraw.Draw(mst_meme)
    # Red & Green bordered card
    d.rectangle([4, 4, 305, 240], outline=(180, 20, 20), width=3)
    d.rectangle([4, 4, 305, 42], fill=(200, 20, 20))
    d.text((20, 14), "MST - MOVIMENTO DOS SEM-TERRA DIGITAL", fill=(255, 255, 255))

    # Subtitle alert
    d.rectangle([10, 48, 300, 72], fill=(255, 235, 200), outline=(200, 120, 20))
    d.text((18, 53), "ALERTA DE OCUPACAO DEMOCRATICA!", fill=(160, 20, 20))

    # Little graphics of tents & flags
    # Draw two mini red tents in the graphic
    d.polygon([(40, 85), (20, 125), (60, 125)], fill=(210, 20, 20))
    d.polygon([(40, 98), (32, 125), (48, 125)], fill=(30, 30, 30))
    d.polygon([(75, 90), (55, 125), (95, 125)], fill=(190, 20, 20))

    # Main text details
    d.text((110, 80), "STATUS DO SEU MONITOR:", fill=(20, 20, 20))
    d.text((110, 98), ">> AREA 100% IMPRODUTIVA!", fill=(190, 20, 20))
    d.text((110, 116), "Laudo: O usuario so enrola", fill=(60, 60, 60))
    d.text((110, 132), "e nao produz picanha.", fill=(60, 60, 60))

    d.line([10, 155, 300, 155], fill=(200, 200, 200), width=1)
    
    # Agrarian reform demands
    d.text((15, 163), "PAUTA DE REIVINDICACOES DO ACAMPAMENTO:", fill=(10, 90, 20))
    d.text((15, 180), "1. Desapropriacao de 50GB do seu SSD", fill=(40, 40, 40))
    d.text((15, 196), "2. Cervejinha gelada garantida no sabado", fill=(40, 40, 40))
    d.text((15, 212), "3. Proibido fechar esta janela (sob pena de mais barracas)!", fill=(180, 20, 20))

    mst_meme.save('assets/memes/mst_ocupacao.png')

    # 3. Note: Notificação Oficial da Reforma Agrária
    with open('assets/notes/notificacao_mst.txt', 'w', encoding='utf-8') as f:
        f.write(
            "TERMO DE OCUPACAO E REFORMA AGRARIA DIGITAL\n\n"
            "Prezado Proprietario deste Computador,\n\n"
            "Informamos que sua tela foi desapropriada pelo MST.\n"
            "Constatou-se que esta area de trabalho nao cumpria sua funcao social,\n"
            "servindo apenas para acumular icones esquecidos e abas abertas.\n\n"
            "A partir de agora, o espaco sera redistribuido democraticamente!\n\n"
            "Viva a Reforma Agraria Digital!\n"
            "Assinado: Frente Parlamentar do Meme"
        )

    print("MST assets successfully generated!")

if __name__ == '__main__':
    generate_mst_assets()
