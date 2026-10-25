"""
Generate meme and notes dedicated to blaming Bolsonaro for everything.
"""
from PIL import Image, ImageDraw
import os

def generate_bolsonaro_blame_assets():
    os.makedirs('assets/memes', exist_ok=True)
    os.makedirs('assets/notes', exist_ok=True)

    # 1. Meme Gráfico: Gráfico de Pizza "De Quem É a Culpa?"
    m_pizza = Image.new('RGB', (290, 230), (255, 252, 245))
    d = ImageDraw.Draw(m_pizza)
    d.rectangle([4, 4, 285, 225], outline=(180, 30, 30), width=3)
    d.rectangle([4, 4, 285, 40], fill=(180, 30, 30))
    d.text((25, 12), "COMISSAO DA VERDADE DO WINDOWS", fill=(255, 255, 255))
    d.text((15, 50), "DE QUEM E A CULPA POR ESTE PC?", fill=(0, 0, 0))
    
    # Pie chart (100% red circle!)
    d.ellipse([30, 80, 130, 180], fill=(210, 30, 30), outline=(130, 10, 10), width=2)
    # Highlight
    d.text((62, 122), "100%", fill=(255, 255, 255))
    
    # Legend
    d.rectangle([150, 90, 162, 102], fill=(210, 30, 30))
    d.text((170, 88), "Bolsonaro (100%)", fill=(20, 20, 20))
    
    d.rectangle([150, 115, 162, 127], fill=(200, 200, 200))
    d.text((170, 113), "Outros (0%)", fill=(100, 100, 100))

    d.rectangle([150, 140, 162, 152], fill=(200, 200, 200))
    d.text((170, 138), "Minha culpa (0%)", fill=(100, 100, 100))

    d.line([15, 195, 275, 195], fill=(200, 200, 200), width=1)
    d.text((15, 203), "Laudo: Qualquer travamento e heranca dele!", fill=(160, 20, 20))
    m_pizza.save('assets/memes/grafico_culpa_bolsonaro.png')

    # 2. Meme Gráfico: Certificado Oficial de Culpa
    m_cert = Image.new('RGB', (280, 210), (245, 248, 255))
    d = ImageDraw.Draw(m_cert)
    d.rectangle([4, 4, 275, 205], outline=(30, 60, 120), width=3)
    d.rectangle([4, 4, 275, 38], fill=(30, 60, 120))
    d.text((35, 12), "CERTIFICADO DE CULPABILIDADE", fill=(255, 255, 255))
    d.text((15, 50), "Ouvidoria Geral da Republica:", fill=(0, 0, 0))
    d.text((15, 75), "- Mouse sumiu? Culpa do Bolsonaro.", fill=(180, 20, 20))
    d.text((15, 95), "- Windows atualizou sozinho? Bolsonaro.", fill=(180, 20, 20))
    d.text((15, 115), "- Bateria fraca? Claramente o Bolsonaro.", fill=(180, 20, 20))
    d.text((15, 135), "- Cafe esfriou? Heranca maldita dele.", fill=(180, 20, 20))
    d.line([15, 160, 265, 160], fill=(180, 180, 180), width=1)
    d.text((15, 172), "Status: 4 anos de desgoverno digital!", fill=(10, 100, 30))
    d.text((15, 188), "Assinado: Gabinete Presidencial", fill=(50, 50, 50))
    m_cert.save('assets/memes/certificado_heranca_maldita.png')

    # Notes
    new_notes = {
        "nota_cpi_bolsonaro.txt": (
            "RELATORIO DA CPI DO COMPUTADOR\n\n"
            "Apos rigorosa investigacao parlamentar, conclui-se que:\n"
            "1. A lentidao do Google Chrome decorre de 4 anos de desmonte;\n"
            "2. O mouse travado no meu paleto foi armado pelo Bolsonaro em Orlando;\n"
            "3. Se o usuario reiniciar a maquina, sera considerado ato antidemocratico!\n\n"
            "Assinado: Relatoria da CPI"
        ),
        "nota_orlando.txt": (
            "COMUNICADO DE SEGURANCA NACIONAL\n\n"
            "Informamos que a culpa deste seu problema atual nao e minha.\n"
            "E do Cid, do capitao, da minuta do golpe ou daquele pessoal na Florida!\n\n"
            "Eu apenas estou aqui passeando democraticamente com a faixa presidencial."
        )
    }

    for fname, content in new_notes.items():
        with open(f'assets/notes/{fname}', 'w', encoding='utf-8') as f:
            f.write(content)

    print("Bolsonaro blame assets generated successfully!")

if __name__ == '__main__':
    generate_bolsonaro_blame_assets()
