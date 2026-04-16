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
#Caso Edge:
from selenium.webdriver.edge.options import Options



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
    "08GDV", "08GE1", "08GEU", "08GLQ", "08GMG", "0CY42",
    "08GFE", "08GFK", "08GFH", "08J1K", "08GEN", "08GF2",
    "08J1N", "08GFU",
    "07RHT", "07RG4", "07RG7", "07RGA", "07RGD", "07RGG",
    "07RI2", "07RIE",
    "07S56", "07S59", "07S5S", "07SKF", "07SUN", "07SVC",
    "07SVV", "07SW4",
    "080X8", "080XB", "080XE",
    "0835Z", "0886T", "0887Q",
    "08GE7", "08GED", "08GF8", "08GLU", "08GMJ",
    "08GFR", "08GFY"
]


for contrato in lista_contratos:

    # CONFIGURACOES PADROES:
    # Ajuste de caminho para importar funções personalizadas
    caminho_absoluto = os.path.abspath(os.curdir)

    # Identificacao de pastas na arquitetura do projeto (includes)
    sys.path.insert(0, caminho_absoluto)

    
    # CONFIGURAÇÃO DE IMPRESSÃO (Obrigatório vir antes de iniciar o Chrome)
     #PREFERENCIA NAVEGADOR
    #chrome_options = Options()
    #chrome_options.add_argument('--kiosk-printing') # Ativa a impressão sem perguntas
    edge_options = Options()
    edge_options.add_argument("--kiosk-printing")
    
    

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
    
    
    #PREFERENCIA NAVEGADOR
    #chrome_options.add_experimental_option('prefs', prefs)
    edge_options.add_experimental_option('prefs', prefs)
    

    # INSTANCIANDO O NAVEGADOR COM AS OPÇÕES
     #PREFERENCIA NAVEGADOR
    #navegador = webdriver.Chrome(options=chrome_options)
    navegador = webdriver.Edge(options=edge_options)



    # DEFININDO VARIAVEIS
    tipo_contrato = ""
    pCodigo = contrato
    tipo_arquivo = "hapvida_boleto"



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

    realizarLogin(navegador, contrato, tipo_arquivo)



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
        arquivo_novo = os.path.join(pasta_download, f"{dia_venc}.{mes_venc}.{ano_venc}-ALTER HAPVIDA {pCodigo} Boleto {tipo_contrato}.pdf")
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
    