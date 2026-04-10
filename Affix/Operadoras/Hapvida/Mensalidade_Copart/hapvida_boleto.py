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
import shutil




# MENU PRINCIPAL 
print('===== BEM VINDO AO GSYSTEM =====:\n')
print('===== BAIXA REFERENTE AOS BOLETOS HAPVIDA (AFFIX) =====:\n')
print('Responsável: Giovanni.Souza')

print("INFORME A DATA DE VENCIMENTO DESEJADA SEGUIDA DO DIA, MES E ANO:\n")
dia_venc = input('Dia(DD): ')
mes_venc = input('Mes(MM): ')
ano_venc = input('Ano(AAAA): ')

#formato data venc
data_completa_venc = f"{dia_venc}/{mes_venc}/{ano_venc}"

#lista de contratos
lista_contratos = [
    "07ND9", "07NDI", "07PFA", "07X23", "07X2S", "07X2C", "07X1Y", "07YNH",
    "07PH4", "07PFG", "07NDP", "07PHA", "07PHG", "07ND6", "07PHM", "07NDC",
    "07PFJ", "07PF4", "07YN2", "0CWY3", "08XJ0", "08XJM", "08YVL", "0CP9J",
    "08Z4M", "08Z4T", "0DY6X", "08Z4W", "08YHD", "0817C", "0814V", "0814Z",
    "0815C", "0818G", "08KM5", "08JZS", "0CMU1", "08JZP", "08NAX", "08NB4",
    "08NAW", "08NB1", "08NAS", "0CY3W", "0CY3M", "08IMZ", "08IUV", "07YPK",
    "07NED", "07NDX", "07PGK", "07PGR", "07PIF", "07PI3", "07NE7", "07NDV",
    "07PIL", "07PI9", "07X3D", "07PGU", "07YQ2", "07PGE", "07X31", "07X3J",
    "07X3T", "07NE1", "08YHG", "08XJ3", "08XJT", "08YVP", "0817F", "0815I",
    "0815L", "0815P", "0818J", "08KM8", "08K05", "08K02", "0CMU7", "08IN2",
    "08IUX"
]
for contrato in lista_contratos:

    # CONFIGURACOES PADROES:
    # Ajuste de caminho para importar funções personalizadas
    caminho_absoluto = os.path.abspath(os.curdir)

    # Identificacao de pastas na arquitetura do projeto (includes)
    sys.path.insert(0, caminho_absoluto)

    # CONFIGURAÇÃO DE IMPRESSÃO (Obrigatório vir antes de iniciar o Chrome)
    chrome_options = Options()
    chrome_options.add_argument('--kiosk-printing') # Ativa a impressão sem perguntas

    # Configura o destino como "Salvar como PDF" e cria pasta download na pasta projeto
    pasta_download = os.path.join(os.getcwd(), "Download")
    os.makedirs(pasta_download, exist_ok=True)

    prefs = {
        "printing.print_preview_sticky_settings.appState": json.dumps({
            "recentDestinations": [{"id": "Save as PDF", "origin": "local", "account": ""}],
            "selectedDestinationId": "Save as PDF",
            "version": 2
        }),
        "savefile.default_directory": pasta_download
    }
    chrome_options.add_experimental_option('prefs', prefs)

    # INSTANCIANDO O NAVEGADOR COM AS OPÇÕES
    navegador = webdriver.Chrome(options=chrome_options)



    # DEFININDO VARIAVEIS
    tipo_contrato = ""
    pCodigo = contrato



    # FLUXO DE NAVEGACAO

    # Acessar link boleto hapvida
    navegador.get("https://webhap.hapvida.com.br/pls/webhap/webNewBoletoEmpresa.Login")

    # Tempo para carregar a página
    time.sleep(5)

    # Fechar pop-up tela de login
    botao = navegador.find_element(By.CLASS_NAME, "ui-button-text")
    botao.click()

    time.sleep(1)
    navegador.maximize_window()

    # REALIZA LOGIN USANDO FUNCAO DE FORA (realizarLogin())

    #lista de contratos

    realizarLogin(navegador, contrato)



    # Seleciona o boleto de acordo com vencimento
    time.sleep(3) # Espera carregar após login
    opcao_vencimento = navegador.find_element(By.XPATH, f"//option[contains(text(), '{data_completa_venc}-MENSALIDADE')]")


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

    # --- COMANDO FINAL PARA SALVAR ---
    # Como foi ativado o Modo Kiosk, ele salva o PDF na pasta sem abrir a janela de impressão
    time.sleep(2)
    navegador.execute_script("window.print();")


    # --- RENOMEANDO ARQUIVO DA PASTA DOWNLOAD ENCAMINHANDO PARA PASTA DA OPERADORA ---

    # Lista todos os arquivos PDF na pasta

    pdfs = []

    for f in os.listdir(pasta_download):
        if f.endswith(".pdf"):
            pdfs.append(f)

    # Se houver pelo menos um PDF, renomeia o primeiro
    if pdfs:
        arquivo_antigo = os.path.join(pasta_download, pdfs[0])
        arquivo_novo = os.path.join(pasta_download, f"{dia_venc}.{mes_venc}.{ano_venc}-AFFIX HAPVIDA {pCodigo} Boleto {tipo_contrato}.pdf")
        os.rename(arquivo_antigo, arquivo_novo)
        #print("Arquivo renomeado com sucesso!")
    else:
        print("Nenhum arquivo PDF encontrado.")
        exit()


    # Mover arquivo renomeado para a pasta de vencimento da operadora (Hapvida Arquivo)
    # Caso nao existir, cria
    pasta_destino = os.path.join("Affix", "Operadoras", "Hapvida", "Mensalidade_Copart", "Hapvida Arquivo",f"{dia_venc}_{mes_venc}_{ano_venc}") 
    os.makedirs(pasta_destino, exist_ok=True)

    shutil.move(arquivo_novo, pasta_destino)
    print(f"BAIXADO: {arquivo_novo}")
    # Fim da operacao
    navegador.quit()
    time.sleep(2)
    