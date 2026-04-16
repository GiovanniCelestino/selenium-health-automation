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
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# MENU PRINCIPAL 
print('===== BEM VINDO AO GSYSTEM =====:\n')
print('===== BAIXA REFERENTE AS NOTAS FISCAIS HAPVIDA (AFFIX) =====:\n')
print('Responsável: Giovanni.Souza')

print("INFORME A DATA DE VENCIMENTO DESEJADA SEGUIDA DO DIA, MES E ANO:\n")
dia_venc = input('Dia(DD): ')
mes_venc = input('Mes(MM): ')
ano_venc = input('Ano(AAAA): ')

#formato data venc
data_completa_venc = f"{dia_venc}/{mes_venc}/{ano_venc}"


#lista de entidades
lista_entidades = [
    "UNEB1", "AFPU1", "FETR1", "ALT88", "09BGF"
]


""" "07RER", "07PFA", "07X23", "07X2S", "07X2C", "07X1Y", "07YNH",
    "07PH4", "07PFG", "07NDP", "07PHA", "07PHG", "07ND6", "07PHM", "07NDC",
    "07PFJ", "07PF4", "07YN2", "0CWY3", "08XJ0", "08XJM", "08YVL", "0CP9J",
    "08Z4M", "08Z4T", "0DY6X", "08Z4W", "08YHD", "0817C", "0814V", "0814Z",
    "0815C", "0818G", "08KM5", "08JZS", "0CMU1", "08JZP", "08NAX", "08NB4",
    "08NAW", "08NB1", "08NAS", "0CY3W", "0CY3M", "08IMZ", "08IUV", "07YPK",
    "07NED", "07NDX", "07PGK", "07PGR", "07PIF", "07PI3", "07NE7", "07NDV",
    "07PIL", "07PI9", "07X3D", "07PGU", "07YQ2", "07PGE", "07X31", "07X3J",
    "07X3T", "07NE1", "08YHG", "08XJ3", "08XJT", "08YVP", "0817F", "0815I",
    "0815L", "0815P", "0818J", "08KM8", "08K05", "08K02", "0CMU7", "08IN2",
    "08IUX"""


#lista de contratos
lista_contratos = [
    "0887M",
]


def salvar_arquivo(tipo_contrato):

        # --- RENOMEANDO ARQUIVO DA PASTA DOWNLOAD ENCAMINHANDO PARA PASTA DA OPERADORA ---

        # Lista todos os arquivos PDF na pasta

        pdfs = []

        for f in os.listdir(pasta_download):
            if f.endswith(".pdf"):
                pdfs.append(f)

        # Se houver pelo menos um PDF, renomeia o primeiro
        if pdfs:
            arquivo_antigo = os.path.join(pasta_download, pdfs[0])
            arquivo_novo = os.path.join(pasta_download, f"{dia_venc}.{mes_venc}.{ano_venc}-ALTER HAPVIDA {pCodigo} Nota Fiscal {tipo_contrato}.pdf")
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
        time.sleep(4)




#PASSA POR CADA ENTIDADE DA LISTA DE ENTIDADES:
for entidade in lista_entidades:

    #PASSA POR CADA CONTRATO DA LISTA DE CONTRATOS
    for contrato in lista_contratos:

        # CONFIGURACOES PADROES:
        # Ajuste de caminho para importar funções personalizadas
        caminho_absoluto = os.path.abspath(os.curdir)

        # Identificacao de pastas na arquitetura do projeto (includes)
        sys.path.insert(0, caminho_absoluto)

        # CONFIGURAÇÃO DE IMPRESSÃO (Obrigatório vir antes de iniciar o Chrome)
        #chrome_options = Options()
        #chrome_options.add_argument('--kiosk-printing') # Ativa a impressão sem perguntas
        edge_options = Options()
        #edge_options.add_argument("--kiosk-printing")

        # Configura o destino como "Salvar como PDF" e cria pasta download na pasta projeto
        pasta_download = os.path.join(os.getcwd(), "Download")
        os.makedirs(pasta_download, exist_ok=True)

        prefs = {
            "download.default_directory": pasta_download, # Onde o arquivo vai cair
            "download.prompt_for_download": False,                # Desativa a pergunta "Onde deseja salvar"
            "download.directory_upgrade": True,
            "plugins.always_open_pdf_externally": True,           # Força o PDF a baixar em vez de abrir no navegador
            "safebrowsing.enabled": True
        }
        
        #PREFERENCIA NAVEGADOR
        #chrome_options.add_experimental_option('prefs', prefs)
        edge_options.add_experimental_option('prefs', prefs)


        # INSTANCIANDO O NAVEGADOR COM AS OPÇÕES
        #PREFERENCIA NAVEGADOR
        #navegador = webdriver.Chrome(options=chrome_options)
        navegador = webdriver.Edge(options=edge_options)


        # DEFININDO VARIAVEIS
        pCodigo = contrato
        tipo_arquivo = "hapvida_nota"



        # FLUXO DE NAVEGACAO

        # Acessar link boleto hapvida
        navegador.get("http://webhap.hapvida.com.br/pls/webhap/pk_nota_fiscal.login")

        # Tempo para carregar a página
        time.sleep(3)

        # Maximixar página
        navegador.maximize_window()


        # REALIZA LOGIN USANDO FUNCAO DE FORA (realizarLogin())
        #lista de contratos

        realizarLogin(navegador, contrato, tipo_arquivo, entidade)
        





        # Seleciona a nota fiscal de acordo com vencimento e empresa
        time.sleep(3) # Espera carregar após login

        opcoes_elementos = navegador.find_elements(By.XPATH, f"//a[contains(@href, 'pCd_Empresa={contrato}') and contains(text(), '{dia_venc}/{mes_venc}/{ano_venc[-2:]}')]")
        total_contratos = len(opcoes_elementos)
        print(f"Contem {total_contratos} para contrato: {contrato}.")

        for i in range(total_contratos):
            
            atualizados = navegador.find_elements(By.XPATH, f"//a[contains(@href, 'pCd_Empresa={contrato}') and contains(text(), '{dia_venc}/{mes_venc}/{ano_venc[-2:]}')]")

            atualizados[i].click()

            # Aguarda o id modal aparecer:
            wait = WebDriverWait(navegador, 10)
            modal_corpo = wait.until(EC.visibility_of_element_located((By.ID, "dialog-modal")))

            # Acessa todo o texto de dentro de <p>
            texto_modal = modal_corpo.find_element(By.TAG_NAME, "p").text

            # Extrai as variaveis com slpit
            cnpj_prestador = texto_modal.split("CNPJ do Prestador*:")[1].split("\n")[0].strip()
            valor_nota = texto_modal.split("Valor total da nota*:")[1].split("\n")[0].strip()
            numero_nfse = texto_modal.split("Número da NFS-e*:")[1].split(":")[0].strip()
            cod_verificacao = texto_modal.split("Código de Verificação*:")[1].split(":")[0].strip()





            # ACESSO AO LINK EMISSÂO DE CONTRATO
            #procura pelo id dialog-modal, vai até a tag p, logo em seguida tag a
            time.sleep(3)
            link_nota = navegador.find_element(By.CSS_SELECTOR, "#dialog-modal p a")
            link_nota.click()



            # Acessa a aba iss.fortaleza
            time.sleep(2)
            aba_nota = navegador.window_handles
            navegador.switch_to.window(aba_nota[-1])


            time.sleep(2)
            #Acessar link para vaidar NFS-e (por Número/RPS)
            link_validar_nfs = navegador.find_element(By.XPATH, "//*[contains(text(), 'Validar NFS-e (por Número/RPS)')]")
            link_validar_nfs.click()


            #Preencher campos para acessar nota fiscal eletrônica:
            navegador.find_element("id", "validarNotaForm:numNfse").send_keys(numero_nfse)
            navegador.find_element("id", "validarNotaForm:numCodVerificacao").send_keys(cod_verificacao)
            navegador.find_element("id", "validarNotaForm:nfseCnpjPrestador").send_keys(cnpj_prestador)
            time.sleep(3)
            # Clica no botao "Consultar" nota
            bnt_consultar = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="validarNotaForm:panelAcoes"]/tbody/tr/td[1]/input')))
            bnt_consultar.click()

            # Checagem se nota é copart ou mensalidade:
            copart_mensal = navegador.find_element(By.XPATH, '//*[@id="div_visualizacao_normal_id"]/div[2]/div[13]/div')

            # captura o texto
            texto_copart_mensal = copart_mensal.text

            if "COPART" in texto_copart_mensal:
                baixa_copart = navegador.find_element(By.XPATH, '//*[@id="j_id32:panelAcoes"]/tbody/tr/td[1]/input')
                baixa_copart.click()
                time.sleep(3)
                tipo_contrato = "Copart"
                salvar_arquivo(tipo_contrato)
                time.sleep(2)
                aba_nota = navegador.window_handles
                navegador.switch_to.window(aba_nota[0])
                time.sleep(2)
                botao_fechar_pop = navegador.find_element(By.XPATH, "/html/body/div[3]/div[3]/div/button")
                botao_fechar_pop.click()  
                time.sleep(2)
        
            else:
                baixa_mensalidade = navegador.find_element(By.XPATH, '//*[@id="j_id32:panelAcoes"]/tbody/tr/td[1]/input')
                baixa_mensalidade.click()
                time.sleep(3)
                tipo_contrato = ""
                salvar_arquivo(tipo_contrato)
                time.sleep(2)
                aba_nota = navegador.window_handles
                navegador.switch_to.window(aba_nota[0])
                time.sleep(2)
                botao_fechar_pop = navegador.find_element(By.XPATH, "/html/body/div[3]/div[3]/div/button")
                botao_fechar_pop.click()
                time.sleep(2)
    navegador.quit()



    