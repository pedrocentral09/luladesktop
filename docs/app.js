/* ==========================================================================
   Desktop Lula: Edição Presidencial — Interactive Scripts & Sound Player
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {

  // 1. Comical Hero Rotating Quotes
  const quotes = [
    "\"Companheiro, onde fica o app do Nubank nessa tela? É só pra uma conferida solidária!\"",
    "\"O mouse deu uma travadinha aí? Sem dúvida nenhuma é culpa do Bolsonaro!\"",
    "\"Guardei seu cursor do mouse no paletó! Não vi nada, companheiro!\"",
    "\"A bateria descarregou? Claramente uma sabotagem da herança maldita!\"",
    "\"Segura essa notinha fiscal com muito amor e picanha!\"",
    "\"O café esfriou enquanto você digitava? Culpa dos 4 anos de desgoverno!\"",
    "\"Tô só passeando aqui pelo seu monitor, tá tudo regularizado!\""
  ];

  const heroPhrase = document.getElementById('hero-phrase');
  let quoteIndex = 0;

  if (heroPhrase) {
    setInterval(() => {
      heroPhrase.style.opacity = '0';
      heroPhrase.style.transform = 'translateY(5px)';
      setTimeout(() => {
        quoteIndex = (quoteIndex + 1) % quotes.length;
        heroPhrase.textContent = quotes[quoteIndex];
        heroPhrase.style.opacity = '1';
        heroPhrase.style.transform = 'translateY(0)';
      }, 300);
    }, 5000);
  }

  // 2. Soundboard Player
  let currentAudio = null;
  const soundCards = document.querySelectorAll('.sound-card');

  soundCards.forEach(card => {
    const btn = card.querySelector('.sound-play-btn');
    const soundFile = card.getAttribute('data-sound');

    btn.addEventListener('click', () => {
      if (currentAudio) {
        currentAudio.pause();
        currentAudio.currentTime = 0;
      }

      // Reset all buttons text
      soundCards.forEach(c => {
        const b = c.querySelector('.sound-play-btn');
        b.textContent = '▶️ Ouvir';
        b.style.background = 'rgba(255, 214, 0, 0.1)';
      
  // Copiar chave PIX da seção da página
  const btnCopyPagePix = document.getElementById('btn-copy-page-pix');
  const pagePixKey = document.getElementById('page-pix-key');
  if (btnCopyPagePix && pagePixKey) {
    btnCopyPagePix.addEventListener('click', () => {
      navigator.clipboard.writeText(pagePixKey.value).then(() => {
        btnCopyPagePix.textContent = '✅ Copiado!';
        btnCopyPagePix.style.background = '#00c853';
        setTimeout(() => {
          btnCopyPagePix.textContent = '📋 Copiar Chave';
          btnCopyPagePix.style.background = '';
        }, 2500);
      });
    });
  }

});

      const audio = new Audio(`sounds/${soundFile}`);
      currentAudio = audio;

      btn.textContent = '🔊 Tocando...';
      btn.style.background = 'var(--color-yellow)';
      btn.style.color = '#000';

      audio.play().catch(e => {
        console.warn('Audio play prevented by browser policy:', e);
        btn.textContent = '▶️ Ouvir';
      
  // Copiar chave PIX da seção da página
  const btnCopyPagePix = document.getElementById('btn-copy-page-pix');
  const pagePixKey = document.getElementById('page-pix-key');
  if (btnCopyPagePix && pagePixKey) {
    btnCopyPagePix.addEventListener('click', () => {
      navigator.clipboard.writeText(pagePixKey.value).then(() => {
        btnCopyPagePix.textContent = '✅ Copiado!';
        btnCopyPagePix.style.background = '#00c853';
        setTimeout(() => {
          btnCopyPagePix.textContent = '📋 Copiar Chave';
          btnCopyPagePix.style.background = '';
        }, 2500);
      });
    });
  }

});

      audio.onended = () => {
        btn.textContent = '▶️ Ouvir';
        btn.style.background = 'rgba(255, 214, 0, 0.1)';
        btn.style.color = 'var(--color-yellow)';
      };
    
  // Copiar chave PIX da seção da página
  const btnCopyPagePix = document.getElementById('btn-copy-page-pix');
  const pagePixKey = document.getElementById('page-pix-key');
  if (btnCopyPagePix && pagePixKey) {
    btnCopyPagePix.addEventListener('click', () => {
      navigator.clipboard.writeText(pagePixKey.value).then(() => {
        btnCopyPagePix.textContent = '✅ Copiado!';
        btnCopyPagePix.style.background = '#00c853';
        setTimeout(() => {
          btnCopyPagePix.textContent = '📋 Copiar Chave';
          btnCopyPagePix.style.background = '';
        }, 2500);
      });
    });
  }

});
  
  // Copiar chave PIX da seção da página
  const btnCopyPagePix = document.getElementById('btn-copy-page-pix');
  const pagePixKey = document.getElementById('page-pix-key');
  if (btnCopyPagePix && pagePixKey) {
    btnCopyPagePix.addEventListener('click', () => {
      navigator.clipboard.writeText(pagePixKey.value).then(() => {
        btnCopyPagePix.textContent = '✅ Copiado!';
        btnCopyPagePix.style.background = '#00c853';
        setTimeout(() => {
          btnCopyPagePix.textContent = '📋 Copiar Chave';
          btnCopyPagePix.style.background = '';
        }, 2500);
      });
    });
  }

});

  // 3. Interactive Web Simulator Sandbox
  const arena = document.getElementById('arena');
  const simPet = document.getElementById('sim-pet');
  const simBubble = document.getElementById('sim-bubble');
  const simImg = document.getElementById('sim-img');

  if (arena && simPet) {
    let petX = 100;
    let petY = 220;
    let targetX = 100;
    let targetY = 220;
    let isTracking = false;

    // Track mouse within the arena bounds
    arena.addEventListener('mousemove', (e) => {
      const rect = arena.getBoundingClientRect();
      targetX = e.clientX - rect.left - 45; // center on pet
      targetY = e.clientY - rect.top - 60;
      isTracking = true;

      // Flip sprite based on movement direction
      if (targetX < petX) {
        simImg.style.transform = 'scaleX(1)';
      } else {
        simImg.style.transform = 'scaleX(-1)';
      }
    
  // Copiar chave PIX da seção da página
  const btnCopyPagePix = document.getElementById('btn-copy-page-pix');
  const pagePixKey = document.getElementById('page-pix-key');
  if (btnCopyPagePix && pagePixKey) {
    btnCopyPagePix.addEventListener('click', () => {
      navigator.clipboard.writeText(pagePixKey.value).then(() => {
        btnCopyPagePix.textContent = '✅ Copiado!';
        btnCopyPagePix.style.background = '#00c853';
        setTimeout(() => {
          btnCopyPagePix.textContent = '📋 Copiar Chave';
          btnCopyPagePix.style.background = '';
        }, 2500);
      });
    });
  }

});

    arena.addEventListener('mouseleave', () => {
      isTracking = false;
    
  // Copiar chave PIX da seção da página
  const btnCopyPagePix = document.getElementById('btn-copy-page-pix');
  const pagePixKey = document.getElementById('page-pix-key');
  if (btnCopyPagePix && pagePixKey) {
    btnCopyPagePix.addEventListener('click', () => {
      navigator.clipboard.writeText(pagePixKey.value).then(() => {
        btnCopyPagePix.textContent = '✅ Copiado!';
        btnCopyPagePix.style.background = '#00c853';
        setTimeout(() => {
          btnCopyPagePix.textContent = '📋 Copiar Chave';
          btnCopyPagePix.style.background = '';
        }, 2500);
      });
    });
  }

});

    // Smooth physics loop
    function updateSimulator() {
      if (isTracking) {
        petX += (targetX - petX) * 0.08;
        petY += (targetY - petY) * 0.08;

        // Keep inside bounds
        petX = Math.max(10, Math.min(arena.clientWidth - 100, petX));
        petY = Math.max(45, Math.min(arena.clientHeight - 130, petY));

        simPet.style.left = `${petX}px`;
        simPet.style.top = `${petY}px`;
      }
      requestAnimationFrame(updateSimulator);
    }
    requestAnimationFrame(updateSimulator);

    // Interactive Buttons inside Sandbox
    const btnPhrase = document.getElementById('btn-phrase');
    const btnSoundGrab = document.getElementById('btn-sound-grab');
    const btnSoundXandao = document.getElementById('btn-sound-xandao');
    const btnSoundMst = document.getElementById('btn-sound-mst');

    function setBubble(text, duration = 3000) {
      simBubble.textContent = text;
      simBubble.style.opacity = '1';
      simBubble.style.transform = 'scale(1.05)';
      setTimeout(() => {
        simBubble.style.transform = 'scale(1)';
      }, 200);
    }

    if (btnPhrase) {
      btnPhrase.addEventListener('click', (e) => {
        e.stopPropagation();
        const rand = quotes[Math.floor(Math.random() * quotes.length)].replace(/^"|"$/g, '');
        setBubble(rand);
      
  // Copiar chave PIX da seção da página
  const btnCopyPagePix = document.getElementById('btn-copy-page-pix');
  const pagePixKey = document.getElementById('page-pix-key');
  if (btnCopyPagePix && pagePixKey) {
    btnCopyPagePix.addEventListener('click', () => {
      navigator.clipboard.writeText(pagePixKey.value).then(() => {
        btnCopyPagePix.textContent = '✅ Copiado!';
        btnCopyPagePix.style.background = '#00c853';
        setTimeout(() => {
          btnCopyPagePix.textContent = '📋 Copiar Chave';
          btnCopyPagePix.style.background = '';
        }, 2500);
      });
    });
  }

});
    }

    if (btnSoundGrab) {
      btnSoundGrab.addEventListener('click', (e) => {
        e.stopPropagation();
        new Audio('sounds/grab.wav').play().catch(() => {
  // Copiar chave PIX da seção da página
  const btnCopyPagePix = document.getElementById('btn-copy-page-pix');
  const pagePixKey = document.getElementById('page-pix-key');
  if (btnCopyPagePix && pagePixKey) {
    btnCopyPagePix.addEventListener('click', () => {
      navigator.clipboard.writeText(pagePixKey.value).then(() => {
        btnCopyPagePix.textContent = '✅ Copiado!';
        btnCopyPagePix.style.background = '#00c853';
        setTimeout(() => {
          btnCopyPagePix.textContent = '📋 Copiar Chave';
          btnCopyPagePix.style.background = '';
        }, 2500);
      });
    });
  }

});
        setBubble("🥷 Guardei seu mouse no paletó!");
      
  // Copiar chave PIX da seção da página
  const btnCopyPagePix = document.getElementById('btn-copy-page-pix');
  const pagePixKey = document.getElementById('page-pix-key');
  if (btnCopyPagePix && pagePixKey) {
    btnCopyPagePix.addEventListener('click', () => {
      navigator.clipboard.writeText(pagePixKey.value).then(() => {
        btnCopyPagePix.textContent = '✅ Copiado!';
        btnCopyPagePix.style.background = '#00c853';
        setTimeout(() => {
          btnCopyPagePix.textContent = '📋 Copiar Chave';
          btnCopyPagePix.style.background = '';
        }, 2500);
      });
    });
  }

});
    }

    if (btnSoundXandao) {
      btnSoundXandao.addEventListener('click', (e) => {
        e.stopPropagation();
        new Audio('sounds/xandao_gavel.wav').play().catch(() => {
  // Copiar chave PIX da seção da página
  const btnCopyPagePix = document.getElementById('btn-copy-page-pix');
  const pagePixKey = document.getElementById('page-pix-key');
  if (btnCopyPagePix && pagePixKey) {
    btnCopyPagePix.addEventListener('click', () => {
      navigator.clipboard.writeText(pagePixKey.value).then(() => {
        btnCopyPagePix.textContent = '✅ Copiado!';
        btnCopyPagePix.style.background = '#00c853';
        setTimeout(() => {
          btnCopyPagePix.textContent = '📋 Copiar Chave';
          btnCopyPagePix.style.background = '';
        }, 2500);
      });
    });
  }

});
        setBubble("⚖️ Prisão preventiva decretada pelo Xandão!");
      
  // Copiar chave PIX da seção da página
  const btnCopyPagePix = document.getElementById('btn-copy-page-pix');
  const pagePixKey = document.getElementById('page-pix-key');
  if (btnCopyPagePix && pagePixKey) {
    btnCopyPagePix.addEventListener('click', () => {
      navigator.clipboard.writeText(pagePixKey.value).then(() => {
        btnCopyPagePix.textContent = '✅ Copiado!';
        btnCopyPagePix.style.background = '#00c853';
        setTimeout(() => {
          btnCopyPagePix.textContent = '📋 Copiar Chave';
          btnCopyPagePix.style.background = '';
        }, 2500);
      });
    });
  }

});
    }

    if (btnSoundMst) {
      btnSoundMst.addEventListener('click', (e) => {
        e.stopPropagation();
        new Audio('sounds/mst_invasion.wav').play().catch(() => {
  // Copiar chave PIX da seção da página
  const btnCopyPagePix = document.getElementById('btn-copy-page-pix');
  const pagePixKey = document.getElementById('page-pix-key');
  if (btnCopyPagePix && pagePixKey) {
    btnCopyPagePix.addEventListener('click', () => {
      navigator.clipboard.writeText(pagePixKey.value).then(() => {
        btnCopyPagePix.textContent = '✅ Copiado!';
        btnCopyPagePix.style.background = '#00c853';
        setTimeout(() => {
          btnCopyPagePix.textContent = '📋 Copiar Chave';
          btnCopyPagePix.style.background = '';
        }, 2500);
      });
    });
  }

});
        setBubble("🚩 Ocupação do MST: Esse monitor é improdutivo!");
      
  // Copiar chave PIX da seção da página
  const btnCopyPagePix = document.getElementById('btn-copy-page-pix');
  const pagePixKey = document.getElementById('page-pix-key');
  if (btnCopyPagePix && pagePixKey) {
    btnCopyPagePix.addEventListener('click', () => {
      navigator.clipboard.writeText(pagePixKey.value).then(() => {
        btnCopyPagePix.textContent = '✅ Copiado!';
        btnCopyPagePix.style.background = '#00c853';
        setTimeout(() => {
          btnCopyPagePix.textContent = '📋 Copiar Chave';
          btnCopyPagePix.style.background = '';
        }, 2500);
      });
    });
  }

});
    }
  }

  // ==========================================================================
  // 4. Configuração do PIX e Modal de Doação
  // ==========================================================================
  const PIX_CONFIG = {
    // Insira aqui sua chave PIX real (e-mail, celular, CPF/CNPJ ou chave aleatória):
    chavePix: "a0e9dba9-a948-4ddb-abc4-04b74224f15b",
    // Link opcional para Livepix, Apoia.se ou Mercado Pago:
    linkApoio: "https://livepix.gg/"
  };

  const donationModal = document.getElementById('donation-modal');
  const modalCloseBtn = document.getElementById('modal-close');
  const btnModalContinue = document.getElementById('btn-modal-continue');
  const pixKeyInput = document.getElementById('pix-key-input');
  const pixQrImg = document.getElementById('pix-qr-img');
  const btnCopyPix = document.getElementById('btn-copy-pix');
  const copyPixText = document.getElementById('copy-pix-text');
  const donationPills = document.querySelectorAll('.donation-pill');

  // Inicializa a chave e QR Code nos elementos
  if (pixKeyInput && pixQrImg) {
    pixKeyInput.value = PIX_CONFIG.chavePix;
    pixQrImg.src = `https://api.qrserver.com/v1/create-qr-code/?size=140x140&data=${encodeURIComponent(PIX_CONFIG.chavePix)}`;
  }

  function openDonationModal() {
    if (donationModal) {
      donationModal.classList.add('active');
      document.body.style.overflow = 'hidden';
    }
  }

  function closeDonationModal() {
    if (donationModal) {
      donationModal.classList.remove('active');
      document.body.style.overflow = '';
    }
  }

  // Intercepta todos os botões de download para abrir o modal de apoio solidário
  const allDownloadLinks = document.querySelectorAll('a[download]');
  allDownloadLinks.forEach(link => {
    link.addEventListener('click', (e) => {
      // Abre o modal
      openDonationModal();

      // Inicia o download automaticamente após 400ms para não bloquear o usuário
      const downloadUrl = link.getAttribute('href') || 'https://github.com/pedrocentral09/luladesktop/releases/latest/download/DesktopLula.exe';
      setTimeout(() => {
        const tempLink = document.createElement('a');
        tempLink.href = downloadUrl;
        tempLink.setAttribute('download', 'DesktopLula.exe');
        document.body.appendChild(tempLink);
        tempLink.click();
        document.body.removeChild(tempLink);
      }, 400);

      // Previne navegação padrão duplicada
      e.preventDefault();
    
  // Copiar chave PIX da seção da página
  const btnCopyPagePix = document.getElementById('btn-copy-page-pix');
  const pagePixKey = document.getElementById('page-pix-key');
  if (btnCopyPagePix && pagePixKey) {
    btnCopyPagePix.addEventListener('click', () => {
      navigator.clipboard.writeText(pagePixKey.value).then(() => {
        btnCopyPagePix.textContent = '✅ Copiado!';
        btnCopyPagePix.style.background = '#00c853';
        setTimeout(() => {
          btnCopyPagePix.textContent = '📋 Copiar Chave';
          btnCopyPagePix.style.background = '';
        }, 2500);
      });
    });
  }

});
  
  // Copiar chave PIX da seção da página
  const btnCopyPagePix = document.getElementById('btn-copy-page-pix');
  const pagePixKey = document.getElementById('page-pix-key');
  if (btnCopyPagePix && pagePixKey) {
    btnCopyPagePix.addEventListener('click', () => {
      navigator.clipboard.writeText(pagePixKey.value).then(() => {
        btnCopyPagePix.textContent = '✅ Copiado!';
        btnCopyPagePix.style.background = '#00c853';
        setTimeout(() => {
          btnCopyPagePix.textContent = '📋 Copiar Chave';
          btnCopyPagePix.style.background = '';
        }, 2500);
      });
    });
  }

});

  // Fechar modal
  if (modalCloseBtn) modalCloseBtn.addEventListener('click', closeDonationModal);
  if (btnModalContinue) btnModalContinue.addEventListener('click', closeDonationModal);

  // Fechar ao clicar fora do card
  if (donationModal) {
    donationModal.addEventListener('click', (e) => {
      if (e.target === donationModal) {
        closeDonationModal();
      }
    
  // Copiar chave PIX da seção da página
  const btnCopyPagePix = document.getElementById('btn-copy-page-pix');
  const pagePixKey = document.getElementById('page-pix-key');
  if (btnCopyPagePix && pagePixKey) {
    btnCopyPagePix.addEventListener('click', () => {
      navigator.clipboard.writeText(pagePixKey.value).then(() => {
        btnCopyPagePix.textContent = '✅ Copiado!';
        btnCopyPagePix.style.background = '#00c853';
        setTimeout(() => {
          btnCopyPagePix.textContent = '📋 Copiar Chave';
          btnCopyPagePix.style.background = '';
        }, 2500);
      });
    });
  }

});
  }

  // Tecla ESC fecha o modal
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && donationModal && donationModal.classList.contains('active')) {
      closeDonationModal();
    }
  
  // Copiar chave PIX da seção da página
  const btnCopyPagePix = document.getElementById('btn-copy-page-pix');
  const pagePixKey = document.getElementById('page-pix-key');
  if (btnCopyPagePix && pagePixKey) {
    btnCopyPagePix.addEventListener('click', () => {
      navigator.clipboard.writeText(pagePixKey.value).then(() => {
        btnCopyPagePix.textContent = '✅ Copiado!';
        btnCopyPagePix.style.background = '#00c853';
        setTimeout(() => {
          btnCopyPagePix.textContent = '📋 Copiar Chave';
          btnCopyPagePix.style.background = '';
        }, 2500);
      });
    });
  }

});

  // Copiar chave PIX
  if (btnCopyPix && pixKeyInput) {
    btnCopyPix.addEventListener('click', () => {
      navigator.clipboard.writeText(pixKeyInput.value).then(() => {
        const originalText = copyPixText.textContent;
        copyPixText.textContent = "✅ Chave Copiada!";
        btnCopyPix.style.background = "#00c853";
        setTimeout(() => {
          copyPixText.textContent = originalText;
          btnCopyPix.style.background = "";
        }, 2500);
      }).catch(err => {
        // Fallback para seleção de texto
        pixKeyInput.select();
        document.execCommand('copy');
        copyPixText.textContent = "✅ Copiado!";
        setTimeout(() => { copyPixText.textContent = "📋 Copiar Chave"; }, 2500);
      
  // Copiar chave PIX da seção da página
  const btnCopyPagePix = document.getElementById('btn-copy-page-pix');
  const pagePixKey = document.getElementById('page-pix-key');
  if (btnCopyPagePix && pagePixKey) {
    btnCopyPagePix.addEventListener('click', () => {
      navigator.clipboard.writeText(pagePixKey.value).then(() => {
        btnCopyPagePix.textContent = '✅ Copiado!';
        btnCopyPagePix.style.background = '#00c853';
        setTimeout(() => {
          btnCopyPagePix.textContent = '📋 Copiar Chave';
          btnCopyPagePix.style.background = '';
        }, 2500);
      });
    });
  }

});
    
  // Copiar chave PIX da seção da página
  const btnCopyPagePix = document.getElementById('btn-copy-page-pix');
  const pagePixKey = document.getElementById('page-pix-key');
  if (btnCopyPagePix && pagePixKey) {
    btnCopyPagePix.addEventListener('click', () => {
      navigator.clipboard.writeText(pagePixKey.value).then(() => {
        btnCopyPagePix.textContent = '✅ Copiado!';
        btnCopyPagePix.style.background = '#00c853';
        setTimeout(() => {
          btnCopyPagePix.textContent = '📋 Copiar Chave';
          btnCopyPagePix.style.background = '';
        }, 2500);
      });
    });
  }

});
  }

  // Seleção de valores nas pílulas de doação
  donationPills.forEach(pill => {
    pill.addEventListener('click', () => {
      donationPills.forEach(p => p.classList.remove('active'));
      pill.classList.add('active');
    
  // Copiar chave PIX da seção da página
  const btnCopyPagePix = document.getElementById('btn-copy-page-pix');
  const pagePixKey = document.getElementById('page-pix-key');
  if (btnCopyPagePix && pagePixKey) {
    btnCopyPagePix.addEventListener('click', () => {
      navigator.clipboard.writeText(pagePixKey.value).then(() => {
        btnCopyPagePix.textContent = '✅ Copiado!';
        btnCopyPagePix.style.background = '#00c853';
        setTimeout(() => {
          btnCopyPagePix.textContent = '📋 Copiar Chave';
          btnCopyPagePix.style.background = '';
        }, 2500);
      });
    });
  }

});
  
  // Copiar chave PIX da seção da página
  const btnCopyPagePix = document.getElementById('btn-copy-page-pix');
  const pagePixKey = document.getElementById('page-pix-key');
  if (btnCopyPagePix && pagePixKey) {
    btnCopyPagePix.addEventListener('click', () => {
      navigator.clipboard.writeText(pagePixKey.value).then(() => {
        btnCopyPagePix.textContent = '✅ Copiado!';
        btnCopyPagePix.style.background = '#00c853';
        setTimeout(() => {
          btnCopyPagePix.textContent = '📋 Copiar Chave';
          btnCopyPagePix.style.background = '';
        }, 2500);
      });
    });
  }

});


  // Copiar chave PIX da seção da página
  const btnCopyPagePix = document.getElementById('btn-copy-page-pix');
  const pagePixKey = document.getElementById('page-pix-key');
  if (btnCopyPagePix && pagePixKey) {
    btnCopyPagePix.addEventListener('click', () => {
      navigator.clipboard.writeText(pagePixKey.value).then(() => {
        btnCopyPagePix.textContent = '✅ Copiado!';
        btnCopyPagePix.style.background = '#00c853';
        setTimeout(() => {
          btnCopyPagePix.textContent = '📋 Copiar Chave';
          btnCopyPagePix.style.background = '';
        }, 2500);
      });
    });
  }

});
