# 🌐 Landing Page Oficial — Desktop Lula: Edição Presidencial

Esta é a landing page completa, responsiva e otimizada para SEO criada para distribuir o aplicativo **Desktop Lula**.

---

## 🚀 Como Visualizar Agora no Seu Computador
Basta dar dois cliques no arquivo:
- `visualizar_landing_page.bat` (ou abrir diretamente o `index.html` no Chrome / Edge / Firefox).

---

## 🏆 Recursos de SEO & Otimização Implementados

1. **Schema.org Rich Snippets (JSON-LD)**:
   - Tipo `SoftwareApplication` / `EntertainmentApplication`.
   - Sistema operacional especificado: Windows 10 e Windows 11.
   - Preço R$ 0,00 (Gratuito).
   - Avaliação e contagem de reviews estruturadas para o Google exibir estrelas nos resultados de busca.
2. **Open Graph & Redes Sociais**:
   - Cards automáticos prontos para **WhatsApp**, **Telegram**, **Twitter/X** e **Facebook**.
   - Inclui imagens em alta definição, título dinâmico e descrição atraente.
3. **Performance Ultra-Rápida**:
   - Construída em HTML5 + CSS3 + Vanilla JavaScript puro.
   - Sem bibliotecas pesadas (100/100 no Google PageSpeed).
4. **Interatividade para Conversão**:
   - **Simulador Web**: O visitante pode mover o mouse na caixa de teste e o Lula segue o cursor na tela com balões de fala dinâmicos.
   - **Soundboard Integrado**: Prévia interativa dos efeitos de som originais (Martelada do Xandão, Sirene da Federal, Ocupação do MST, etc.).
   - **Aviso Legal & Sátira Política**: Seção de transparência jurídica citando o Art. 5º da Constituição Federal sobre livre manifestação e humor.

---

## ☁️ Opções para Hospedar Grátis na Internet

### Opção 1: GitHub Pages (Recomendado & 100% Gratuito)
1. Crie um repositório no seu GitHub (ex: `desktop-lula`).
2. Suba o conteúdo desta pasta `landing_page`.
3. Vá em **Settings** > **Pages** e selecione a branch `main`.
4. Seu site estará no ar em `https://seu-usuario.github.io/desktop-lula/` com certificado SSL HTTPS automático!

### Opção 2: Netlify ou Vercel
1. Acesse [netlify.com](https://www.netlify.com) ou [vercel.com](https://vercel.com).
2. Arraste e solte a pasta `landing_page` no painel.
3. O site é publicado instantaneamente com domínio gratuito `.netlify.app` ou `.vercel.app`.

---

## 💰 Como Configurar sua Chave PIX e Link de Doação

No arquivo `landing_page/app.js` (logo nas primeiras linhas), você encontrará o bloco de configuração:

```javascript
const PIX_CONFIG = {
  // Insira aqui sua chave PIX real (e-mail, celular, CPF/CNPJ ou chave aleatória):
  chavePix: "a0e9dba9-a948-4ddb-abc4-04b74224f15b",
  // Link opcional para Livepix, Apoia.se ou Mercado Pago:
  linkApoio: "https://livepix.gg/"
};
```

Basta substituir `"a0e9dba9-a948-4ddb-abc4-04b74224f15b"` pela sua chave PIX real.
- O campo de cópia e o **QR Code oficial** se atualizarão sozinhos instantaneamente na tela!
- O usuário que clicar no botão de download verá o modal com o Pix da Picanha, enquanto o download do `.exe` inicia automaticamente em segundo plano.

---

## 📥 Observação sobre o Download do `.exe`

Na pasta `landing_page/downloads/DesktopLula.exe`, o arquivo executável já está incluído para download direto via link local ou servidor estático.

> **Dica para plataformas com limite de upload:**
> Caso hospede em serviços com limite de tamanho de repositório, você pode subir o arquivo `DesktopLula.exe` na aba **Releases** do GitHub (que suporta até 2 GB por arquivo) e simplesmente atualizar o `href` do botão de download no `index.html` para o link do Release!
