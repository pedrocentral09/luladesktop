"""
Generate meme for asking where the bank app is.
"""
from PIL import Image, ImageDraw
import os

def generate_bank_meme():
    os.makedirs('assets/memes', exist_ok=True)
    os.makedirs('assets/notes', exist_ok=True)

    # 1. Meme Gráfico: "Onde tá o App do Banco?"
    m_banco = Image.new('RGB', (290, 220), (245, 248, 255))
    d = ImageDraw.Draw(m_banco)
    d.rectangle([4, 4, 285, 215], outline=(20, 80, 160), width=3)
    d.rectangle([4, 4, 285, 42], fill=(20, 80, 160))
    d.text((25, 14), "RECEITA FEDERAL - REQUISICAO URGENTE", fill=(255, 255, 255))

    # Bank icon / safe graphic
    d.rounded_rectangle([20, 55, 65, 100], radius=5, fill=(40, 120, 210))
    d.text((32, 68), "R$", fill=(255, 255, 255))

    d.text((80, 55), "CADASTRO DO PIX SOLIDARIO", fill=(20, 20, 20))
    d.text((80, 75), "Companheiro, onde ta", fill=(180, 20, 20))
    d.text((80, 93), "o app do seu banco?", fill=(180, 20, 20))

    d.line([15, 115, 275, 115], fill=(200, 200, 200), width=1)
    d.text((15, 125), "Solicitacao de acesso:", fill=(40, 40, 40))
    d.text((15, 142), "1. Apenas para conferir o saldo com carinho;", fill=(60, 60, 60))
    d.text((15, 158), "2. Descontar a taxa de uso do Windows;", fill=(60, 60, 60))
    d.text((15, 174), "3. Nubank, Itau ou Inter aceitos!", fill=(60, 60, 60))

    d.text((15, 195), "Status: Aguardando o clique do usuario no app", fill=(10, 110, 30))
    m_banco.save('assets/memes/procura_app_banco.png')

    # 2. Text note
    with open('assets/notes/onde_ta_o_banco.txt', 'w', encoding='utf-8') as f:
        f.write(
            "NOTIFICACAO FISCAL DE AMIZADE\n\n"
            "Prezado Companheiro,\n\n"
            "Passei pela sua tela e reparei que o atalho do seu banco nao esta visivel.\n"
            "Ele esta escondido em alguma pasta?\n"
            "Favor abrir o aplicativo do banco para que possamos verificar\n"
            "se sobrou algum trocado para a picanha de sabado.\n\n"
            "Atenciosamente,\n"
            "Presidencia da Republica do Desktop"
        )

    print("Bank meme and note generated successfully!")

if __name__ == '__main__':
    generate_bank_meme()
