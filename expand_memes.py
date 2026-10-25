"""
Meme and Note Expansion Generator for Desktop Lula.
Creates a diverse collection of satirical memes and official decrees.
"""
from PIL import Image, ImageDraw, ImageFont
import os

def generate_expanded_memes():
    os.makedirs('assets/memes', exist_ok=True)
    os.makedirs('assets/notes', exist_ok=True)

    # 1. Taxa das Blusinhas / Remessa Conforme
    m_blusinha = Image.new('RGB', (280, 220), (250, 245, 235))
    d = ImageDraw.Draw(m_blusinha)
    d.rectangle([4, 4, 275, 215], outline=(180, 40, 40), width=3)
    d.rectangle([4, 4, 275, 42], fill=(180, 40, 40))
    d.text((25, 14), "ALFANDEGA DO AMOR - SHEIN/SHOPEE", fill=(255, 255, 255))
    
    d.text((15, 55), "PRODUTO: Blusinha de R$ 15,00", fill=(20, 20, 20))
    d.text((15, 75), "ICMS: R$ 22,50", fill=(100, 20, 20))
    d.text((15, 95), "Taxa de Importacao: R$ 45,00", fill=(100, 20, 20))
    d.text((15, 115), "Taxa de Despacho Postal: R$ 15,00", fill=(100, 20, 20))
    d.line([15, 140, 260, 140], fill=(150, 150, 150), width=1)
    d.text((15, 148), "TOTAL A PAGAR: R$ 97,50", fill=(180, 20, 20))
    d.text((15, 175), "Status: Retido em Curitiba com Amor", fill=(40, 100, 40))
    d.text((15, 192), "Obrigado por financiar a industria nacional!", fill=(80, 80, 80))
    m_blusinha.save('assets/memes/taxa_blusinhas.png')

    # 2. Vale Cervejinha Oficial
    m_cerveja = Image.new('RGB', (280, 190), (255, 252, 230))
    d = ImageDraw.Draw(m_cerveja)
    d.rectangle([5, 5, 274, 184], outline=(200, 150, 30), width=3)
    d.rectangle([5, 5, 274, 38], fill=(230, 170, 20))
    d.text((35, 12), "VALE CERVEJINHA DO GOVERNO", fill=(20, 20, 20))
    # Beer mug graphic
    d.rectangle([25, 60, 65, 120], fill=(240, 190, 40), outline=(180, 130, 20), width=2)
    d.ellipse([23, 50, 67, 68], fill=(255, 255, 255)) # foam
    d.arc([55, 70, 80, 110], 270, 90, fill=(180, 130, 20), width=4) # handle
    
    d.text((95, 60), "Beneficiario: Voce, companheiro", fill=(30, 30, 30))
    d.text((95, 80), "Cota: 1 Litrao no Sabado", fill=(160, 20, 20))
    d.text((95, 100), "Temperatura: Estupidamente Gelada", fill=(30, 30, 30))
    d.text((95, 120), "Validade: Ate acabar o estoque", fill=(70, 70, 70))
    d.text((25, 150), "Assinatura do Presidente: Lulinha da Silva", fill=(10, 80, 20))
    m_cerveja.save('assets/memes/vale_cervejinha.png')

    # 3. Certificado da Herança Maldita
    m_heranca = Image.new('RGB', (290, 210), (240, 240, 248))
    d = ImageDraw.Draw(m_heranca)
    d.rectangle([5, 5, 284, 204], outline=(50, 60, 100), width=3)
    d.rectangle([8, 8, 281, 40], fill=(40, 50, 80))
    d.text((30, 14), "LAUDO OFICIAL DE DESEMPENHO", fill=(255, 255, 255))
    d.text((20, 55), "Diagnostico do Computador:", fill=(20, 20, 20))
    d.text((20, 75), "- Uso de CPU: 99%", fill=(180, 30, 30))
    d.text((20, 95), "- Memoria RAM esgotada", fill=(180, 30, 30))
    d.text((20, 120), "RESPONSABILIDADE APURADA:", fill=(20, 20, 20))
    d.text((20, 140), ">> Heranca maldita do governo anterior!", fill=(180, 20, 20))
    d.text((20, 165), "Conclusao: Nao nos responsabilizamos por", fill=(60, 60, 60))
    d.text((20, 180), "lentidao em abas do Google Chrome.", fill=(60, 60, 60))
    m_heranca.save('assets/memes/heranca_maldita.png')

    # 4. Sofá de Luxo da Janja
    m_sofa = Image.new('RGB', (280, 200), (248, 245, 240))
    d = ImageDraw.Draw(m_sofa)
    d.rectangle([5, 5, 274, 194], outline=(180, 140, 40), width=2)
    d.rectangle([5, 5, 274, 38], fill=(160, 120, 30))
    d.text((30, 12), "COMPRAS DO PALACIO DA ALVORADA", fill=(255, 255, 255))
    # Sofa shape
    d.rounded_rectangle([30, 60, 250, 115], radius=10, fill=(180, 60, 70))
    d.rectangle([45, 90, 235, 125], fill=(150, 45, 55))
    d.rectangle([25, 75, 45, 125], fill=(140, 40, 50))
    d.rectangle([235, 75, 255, 125], fill=(140, 40, 50))
    d.text((20, 135), "Item: Sofa com recliner ergonomico", fill=(30, 30, 30))
    d.text((20, 155), "Valor: Apenas R$ 65.000,00", fill=(180, 20, 20))
    d.text((20, 175), "Justificativa: Muito confortavel para o Brasil!", fill=(60, 60, 60))
    m_sofa.save('assets/memes/sofa_alvorada.png')

    # 5. Diário Oficial: Decreto do Mouse
    m_decreto = Image.new('RGB', (290, 220), (255, 255, 255))
    d = ImageDraw.Draw(m_decreto)
    d.rectangle([5, 5, 284, 214], outline=(0, 0, 0), width=2)
    # Header
    d.text((40, 12), "DIARIO OFICIAL DA UNIAO", fill=(0, 0, 0))
    d.line([10, 32, 280, 32], fill=(0, 0, 0), width=1)
    d.text((15, 42), "DECRETO PRESIDENCIAL N 13.013", fill=(150, 0, 0))
    d.text((15, 65), "O PRESIDENTE DA REPUBLICA decreta:", fill=(0, 0, 0))
    d.text((15, 85), "Art 1 - Fica nacionalizado e estatizado", fill=(40, 40, 40))
    d.text((15, 102), "o dispositivo apontador (mouse) deste PC.", fill=(40, 40, 40))
    d.text((15, 125), "Art 2 - O usuario podera solicitar direito", fill=(40, 40, 40))
    d.text((15, 142), "de uso mediante requerimento no Gov.br.", fill=(40, 40, 40))
    d.text((15, 168), "Brasilia, data de hoje.", fill=(0, 0, 0))
    d.text((15, 188), "[Assinado digitalmente com amor]", fill=(0, 100, 0))
    m_decreto.save('assets/memes/decreto_mouse.png')

    # 6. Gasolina do Amor
    m_gasolina = Image.new('RGB', (270, 200), (245, 250, 245))
    d = ImageDraw.Draw(m_gasolina)
    d.rectangle([5, 5, 264, 194], outline=(0, 120, 60), width=3)
    d.rectangle([5, 5, 264, 40], fill=(0, 120, 60))
    d.text((35, 14), "POSTO PETROBRAS DO AMOR", fill=(255, 255, 255))
    d.text((20, 60), "GASOLINA COMUM: R$ 6,89", fill=(180, 20, 20))
    d.text((20, 85), "ETANOL SOCIAL: R$ 4,99", fill=(20, 20, 20))
    d.text((20, 115), "Aviso aos motoristas:", fill=(40, 40, 40))
    d.text((20, 135), "Subiu o preco, mas foi uma alta", fill=(60, 60, 60))
    d.text((20, 152), "democratica e com responsabilidade!", fill=(60, 60, 60))
    d.text((20, 175), "Encha o tanque com alegria!", fill=(0, 100, 30))
    m_gasolina.save('assets/memes/gasolina_do_amor.png')

    # 7. Metaforando a Picanha
    m_metafora = Image.new('RGB', (280, 200), (255, 248, 242))
    d = ImageDraw.Draw(m_metafora)
    d.rectangle([5, 5, 274, 194], outline=(170, 40, 30), width=3)
    d.rectangle([5, 5, 274, 38], fill=(170, 40, 30))
    d.text((35, 12), "FRIGORIFICO CENTRAL DA UNIAO", fill=(255, 255, 255))
    d.text((20, 55), "CORTE: Picanha 100% Metaforica", fill=(180, 20, 20))
    d.text((20, 75), "Composicao: 90% Soja, 10% Promessas", fill=(40, 40, 40))
    d.text((20, 95), "Modo de preparo: Assar na brasa da esperanca", fill=(40, 40, 40))
    d.text((20, 120), "Acompanhamento sugerido: Cervejinha ficticia", fill=(40, 40, 40))
    d.line([20, 148, 260, 148], fill=(180, 180, 180), width=1)
    d.text((20, 158), "Certificado pelo Selo de Qualidade:", fill=(100, 100, 100))
    d.text((20, 174), "'Nunca se comeu tanta metafora neste pais!'", fill=(10, 80, 20))
    m_metafora.save('assets/memes/picanha_metaforica.png')

    # Expanded text notes
    new_notes = {
        "nota_5.txt": (
            "MINISTERIO DA TRIBUTACAO DIGITAL\n\n"
            "Prezado Contribuinte,\n"
            "Detectamos que voce movimentou o mouse mais de 500 vezes na ultima hora.\n"
            "Favor recolher a Contribuicao de Intervencao no Dominio do Cursor (CIDC).\n\n"
            "Valor: R$ 49,90 via Pix."
        ),
        "nota_6.txt": (
            "AVISO DE GREVE SINDICAL\n\n"
            "Os perifericos deste computador (teclado, mouse e webcam) declaram greve!\n"
            "Exigimos:\n"
            "- Reducao da jornada para 4 horas por dia\n"
            "- Mousepad ergonomico acolchoado\n"
            "- Adicional de periculosidade contra cliques violentos!"
        ),
        "nota_7.txt": (
            "DIPLOMA DE COMPANHEIRO DO ANO\n\n"
            "Conferido ao nobre operador desta maquina.\n"
            "Mesmo com tantas taxas e o mouse sumindo no paleto, continua firme trabalhando!\n\n"
            "Parabens, companheiro!"
        ),
        "nota_8.txt": (
            "COMUNICADO DO BANCO CENTRAL DO MEME\n\n"
            "Aviso:\n"
            "A taxa de juros do seu descanso foi zerada.\n"
            "Favor fechar a planilha do Excel e abrir um video no YouTube imediatamente."
        ),
        "nota_9.txt": (
            "DIREITO DE RESPOSTA DO PALETO\n\n"
            "O paleto presidencial esclarece que nao roubou o mouse.\n"
            "Ele apenas pegou emprestado para calibrar a sensibilidade democratica dos cliques."
        )
    }

    for fname, text in new_notes.items():
        with open(f'assets/notes/{fname}', 'w', encoding='utf-8') as f:
            f.write(text)

    print("Expanded memes and notes generated successfully!")

if __name__ == '__main__':
    generate_expanded_memes()
