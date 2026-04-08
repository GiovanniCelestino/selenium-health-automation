from selenium import webdriver
import os
import sys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
caminho_absoluto = os.path.abspath(os.curdir)
sys.path.insert(0, caminho_absoluto)
from Senhas.login_hapvida import realizarLogin
import time
import json
# Ajuste de caminho para importar funções personalizadas
caminho_absoluto = os.path.abspath(os.curdir)

# Identificacao de pastas na arquitetura do projeto (includes)
sys.path.insert(0, caminho_absoluto)

# CONFIGURAÇÃO DE IMPRESSÃO (Obrigatório vir antes de iniciar o Chrome)
chrome_options = Options()
chrome_options.add_argument('--kiosk-printing') # Ativa a impressão sem perguntas

# Configura o destino como "Salvar como PDF" e define a pasta atual como destino
caminho_download = os.path.abspath(os.curdir)
prefs = {
    "printing.print_preview_sticky_settings.appState": json.dumps({
        "recentDestinations": [{"id": "Save as PDF", "origin": "local", "account": ""}],
        "selectedDestinationId": "Save as PDF",
        "version": 2
    }),
    "savefile.default_directory": caminho_download
}
chrome_options.add_experimental_option('prefs', prefs)

# INSTANCIANDO O NAVEGADOR COM AS OPÇÕES
navegador = webdriver.Chrome(options=chrome_options)




# FLUXO DE NAVEGACAO

# Acessar link nota fiscal hapvida
navegador.get("https://webhap.hapvida.com.br/pls/webhap/webNewBoletoEmpresa.Login")

# Tempo para carregar a página
time.sleep(5)

# Fechar pop-up tela de login
botao = navegador.find_element(By.CLASS_NAME, "ui-button-text")
botao.click()

time.sleep(1)
navegador.maximize_window()

# Realizar login (usando sua função externa)
realizarLogin(navegador)

# Seleciona o boleto de acordo com vencimento
time.sleep(3) # Espera carregar após login
opcao_vencimento = navegador.find_element(By.XPATH, "//option[contains(text(), '20/02/2026-MENSALIDADE')]")
opcao_vencimento.click()

# Clica no botão continuar
time.sleep(3)
continuar_contrato = navegador.find_element(By.CSS_SELECTOR, "[value='Continuar'][class='botao']")
continuar_contrato.click()

# Acessa a aba de boletos (Aba 1)
time.sleep(2)
aba_boleto = navegador.window_handles
navegador.switch_to.window(aba_boleto[1])

# Gerar boleto:
time.sleep(3)
gerar_boleto = navegador.find_element(By.ID, "bt_continuar")
gerar_boleto.click()

# Muda para a aba onde o PDF é exibido (Aba 2)
time.sleep(3)
aba_final = navegador.window_handles
navegador.switch_to.window(aba_final[2])

# --- 4. COMANDO FINAL PARA SALVAR ---
# Como ativamos o Modo Kiosk, ele salva o PDF na pasta sem abrir a janela de impressão
time.sleep(2)
navegador.execute_script("window.print();")

print(f"Sucesso! O boleto deve aparecer na pasta: {caminho_download}")

# Pausa para você conferir antes de fechar
input("Confira a pasta e pressione Enter para fechar o navegador...")
navegador.quit()