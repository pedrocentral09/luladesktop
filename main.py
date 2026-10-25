"""
Desktop Lula - Main Application Entrypoint.
Presidential Edition.
"""
import sys
import os
import subprocess

# Handle PyInstaller one-file extraction directory
if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    os.chdir(sys._MEIPASS)

from PyQt6.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QMessageBox
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtCore import Qt

from config import load_config
from pet_window import LulaPetWindow
from meme_window import clear_all_memes
from drops import clear_all_drops
from plane_window import clear_all_planes
from police_window import clear_all_police
from bolsonaro_window import clear_all_bolsonaro
from puc_window import clear_all_protests
from xandao_window import clear_all_xandao
from mst_window import clear_all_mst_invasions

def open_folder(path):
    if getattr(sys, 'frozen', False):
        exe_dir = os.path.dirname(sys.executable)
        ext_path = os.path.join(exe_dir, path)
        if os.path.exists(ext_path):
            subprocess.Popen(f'explorer "{os.path.abspath(ext_path)}"')
            return
    abs_path = os.path.abspath(path)
    if os.path.exists(abs_path):
        subprocess.Popen(f'explorer "{abs_path}"')

def main():
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    config = load_config()

    # Create Pet Window
    pet = LulaPetWindow(config)

    # Setup System Tray
    tray_icon = QSystemTrayIcon()
    
    icon_path = "assets/sprites/idle_r_0.png"
    if os.path.exists(icon_path):
        tray_icon.setIcon(QIcon(icon_path))
    tray_icon.setToolTip("Desktop Lula - Edição Presidencial")

    # Tray Menu
    tray_menu = QMenu()
    tray_menu.setStyleSheet("""
        QMenu {
            background-color: #1e1e1e;
            color: #ffffff;
            font-size: 12px;
            padding: 5px;
        }
        QMenu::item:selected {
            background-color: #008037;
        }
    """)

    # Expressões do Presidente
    menu_emotes = tray_menu.addMenu("🎭 Expressões do Lula")
    act_em_angel = menu_emotes.addAction("😇 Cara de Santo / Anjo Inocente")
    act_em_angel.triggered.connect(lambda: (pet.show_emote("anjo", 3.5), pet.say("Vi nada, companheiro! Sou um anjinho! 😇", 2.5)))
    act_em_picanha = menu_emotes.addAction("🥩 Sonhar com Picanha e Cerveja")
    act_em_picanha.triggered.connect(lambda: (pet.show_emote("picanha", 3.5), pet.say("Uma picanha com cervejinha gelada... Que beleza!", 3.0)))
    act_em_idea = menu_emotes.addAction("💡 Ideia Genial / Esquema")
    act_em_idea.triggered.connect(lambda: (pet.show_emote("ideia", 3.0), pet.say("Tive uma ideia genial pro Brasil!", 2.5)))
    act_em_shock = menu_emotes.addAction("❗ Levar um Susto")
    act_em_shock.triggered.connect(lambda: (pet.show_emote("susto", 2.5), pet.say("Opa! Que susto, companheiro!", 2.0)))
    act_em_pix = menu_emotes.addAction("💸 Procurar o Pix")
    act_em_pix.triggered.connect(pet.ask_for_bank_app)
    act_em_blame = menu_emotes.addAction("👉 Culpar o Capitão")
    act_em_blame.triggered.connect(pet.blame_bolsonaro)
    act_em_angry = menu_emotes.addAction("💢 Indignação Presidencial")
    act_em_angry.triggered.connect(pet.start_angry)
    act_em_love = menu_emotes.addAction("❤️ Paz e Amor")
    act_em_love.triggered.connect(lambda: (pet.show_emote("amor", 3.0), pet.say("O amor venceu o odio, companheiro! ❤️", 3.0)))
    tray_menu.addSeparator()

    # Quick test actions
    act_steal = QAction("🥷 Furto Sutil do Mouse Agora", tray_menu)
    act_steal.triggered.connect(pet.start_sneak_mouse)
    tray_menu.addAction(act_steal)

    act_icon = QAction("🗂️ Roubar Ícone da Barra / Desktop", tray_menu)
    act_icon.triggered.connect(pet.start_steal_icon)
    tray_menu.addAction(act_icon)

    act_blame = QAction("📢 Pronunciamento: Culpar o Bolsonaro", tray_menu)
    act_blame.triggered.connect(pet.blame_bolsonaro)
    tray_menu.addAction(act_blame)

    act_bank = QAction("🏦 Perguntar: Onde tá o App do Banco?", tray_menu)
    act_bank.triggered.connect(pet.ask_for_bank_app)
    tray_menu.addAction(act_bank)

    act_plane = QAction("✈️ Passar Avião da Janja", tray_menu)
    act_plane.triggered.connect(pet.summon_janja_plane)
    tray_menu.addAction(act_plane)

    act_police = QAction("🚨 Viatura da Federal (Moro e Deltan)", tray_menu)
    act_police.triggered.connect(pet.summon_police_raid)
    tray_menu.addAction(act_police)

    act_bolso = QAction("👉 Bolsonaro: Fazer a Arminha", tray_menu)
    act_bolso.triggered.connect(pet.summon_bolsonaro_peek)
    tray_menu.addAction(act_bolso)

    act_puc = QAction("📢 Protesto Estudantil da PUC (Pró-Lula)", tray_menu)
    act_puc.triggered.connect(pet.summon_puc_protest)
    tray_menu.addAction(act_puc)

    act_xandao = QAction("⚖️ Xandão: Prisão Preventiva do Mouse", tray_menu)
    act_xandao.triggered.connect(pet.summon_xandao_arrest)
    tray_menu.addAction(act_xandao)

    act_mst = QAction("🚩 Invasão do MST na Tela", tray_menu)
    act_mst.triggered.connect(pet.summon_mst_invasion)
    tray_menu.addAction(act_mst)

    act_meme = QAction("📜 Trazer Meme / Boleto Agora", tray_menu)
    act_meme.triggered.connect(pet.start_bring_meme)
    tray_menu.addAction(act_meme)

    act_shower = QAction("💥 Chuva de Memes (Trazer 3 Memes)", tray_menu)
    act_shower.triggered.connect(lambda: pet.summon_meme_shower(3))
    tray_menu.addAction(act_shower)

    act_clear = QAction("🧹 Limpar Janelas e Rastros", tray_menu)
    act_clear.triggered.connect(lambda: (clear_all_memes(), clear_all_drops(), clear_all_planes(), clear_all_police(), clear_all_bolsonaro(), clear_all_protests(), clear_all_xandao(), clear_all_mst_invasions()))
    tray_menu.addAction(act_clear)

    tray_menu.addSeparator()

    # Toggle Pause
    def toggle_pause():
        pet.paused = not pet.paused
        if pet.paused:
            pet._restore_cursor_safety()
            pet.say("Pausa presidencial!", duration_sec=2)
            act_pause.setText("▶️ Retomar")
        else:
            pet.say("De volta ao trabalho!", duration_sec=2)
            act_pause.setText("⏸️ Pausar")

    act_pause = QAction("⏸️ Pausar", tray_menu)
    act_pause.triggered.connect(toggle_pause)
    tray_menu.addAction(act_pause)

    # Toggle Sound
    def toggle_sound():
        pet.sound.enabled = not pet.sound.enabled
        act_sound.setText("🔇 Ativar Som" if not pet.sound.enabled else "🔊 Silenciar Sons")

    act_sound = QAction("🔊 Silenciar Sons", tray_menu)
    act_sound.triggered.connect(toggle_sound)
    tray_menu.addAction(act_sound)

    tray_menu.addSeparator()

    # Open Asset folders
    act_open_memes = QAction("📂 Abrir Pasta de Memes", tray_menu)
    act_open_memes.triggered.connect(lambda: open_folder("assets/memes"))
    tray_menu.addAction(act_open_memes)

    act_open_sounds = QAction("🎵 Abrir Pasta de Sons", tray_menu)
    act_open_sounds.triggered.connect(lambda: open_folder("assets/sounds"))
    tray_menu.addAction(act_open_sounds)

    # Sobre e Termo de Isenção Legal
    def show_about_disclaimer():
        msg = QMessageBox()
        msg.setWindowTitle("Desktop Lula — Termo Legal e Paródia")
        msg.setText("<b>Desktop Lula: Edição Presidencial</b><br><i>Obra Artística de Humor, Paródia e Sátira Política</i>")
        msg.setInformativeText(
            "<b>1. Natureza Humorística e Paródica:</b><br>"
            "Este software é uma criação artística e satírica independente, desenvolvida exclusivamente para fins de entretenimento, humor e paródia da cultura da internet brasileira.<br><br>"
            "<b>2. Amparo Constitucional e Legal:</b><br>"
            "As manifestações e caricaturas aqui presentes são amparadas pelos incisos IV e IX do Art. 5º da Constituição Federal do Brasil (Livre manifestação do pensamento e atividade artística), pelo Art. 47 da Lei nº 9.610/1998 (Livre exercício da paródia) e pela jurisprudência pacífica do Supremo Tribunal Federal (ADI 4451), que protege o direito ao humor sobre figuras e temas públicos.<br><br>"
            "<b>3. Isenção de Vínculo:</b><br>"
            "Não há qualquer afiliação, endosso, patrocínio ou vínculo partidário ou governamental com personalidades, instituições públicas, partidos ou movimentos retratados.<br><br>"
            "<b>4. Segurança e Privacidade:</b><br>"
            "O aplicativo é de código aberto/local, não coleta nenhum dado pessoal, não monitora digitação e não acessa a internet nem contas bancárias."
        )
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.exec()

    act_about = QAction("⚖️ Sobre & Termo de Isenção (Paródia)", tray_menu)
    act_about.triggered.connect(show_about_disclaimer)
    tray_menu.addAction(act_about)

    tray_menu.addSeparator()

    # Exit
    def exit_app():
        pet._restore_cursor_safety()
        clear_all_memes()
        clear_all_drops()
        clear_all_planes()
        clear_all_police()
        clear_all_bolsonaro()
        clear_all_protests()
        clear_all_xandao()
        clear_all_mst_invasions()
        app.quit()

    act_exit = QAction("❌ Fechar Desktop Lula", tray_menu)
    act_exit.triggered.connect(exit_app)
    tray_menu.addAction(act_exit)

    tray_icon.setContextMenu(tray_menu)
    tray_icon.show()

    # Run application
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
