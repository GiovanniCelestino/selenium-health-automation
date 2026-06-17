from selenium import webdriver
import os
import sys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
caminho_absoluto = os.path.abspath(os.curdir)
sys.path.insert(0, caminho_absoluto)
from senhas.login_hapvida import realizarLogin
import time
import json
import shutil
#Caso Edge:
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import openpyxl
#Excessoes Try/Except
from selenium.common.exceptions import NoSuchElementException

# MENU PRINCIPAL 
print('===== BEM VINDO AO GSYSTEM =====:\n')
print('===== BAIXA REFERENTE AOS DETALHES (AFFIX) =====:\n')
print('Responsável: Giovanni.Souza')

print("INFORME A DATA DE VENCIMENTO DESEJADA SEGUIDA DO DIA, MES E ANO:\n")
dia_venc = input('Dia(DD): ')
mes_venc = input('Mes(MM): ')
ano_venc = input('Ano(AAAA): ')

opc_copart = input("\nDIGITE UMA DAS OPÇÕES ABAIXO:\n[1]Copart\n[2]Mensalidade\n")
if opc_copart == "1":
    tipo_contrato = "S"

elif opc_copart == "2":
    tipo_contrato = "N"



#formato data venc
data_completa_venc = f"{dia_venc}/{mes_venc}/{ano_venc}"
#converter em data
data_completa_convert = datetime.strptime(data_completa_venc, "%d/%m/%Y").date()


#data atual
data_hoje = datetime.now().date()

print(data_completa_convert)
print(data_hoje)




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
pasta_download = os.path.join(os.getcwd(), "dados","download_principal")
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

tipo_arquivo = "hapvida_detalhe_affix"
cnpj = "Indefinido"




# REALIZA LOGIN USANDO FUNCAO DE FORA (realizarLogin())
#lista de contratos

# Carregr arquivo
caminho_arquivo = 'senhas/senhas_operadoras.xlsx'
wb = openpyxl.load_workbook(caminho_arquivo)
aba_hapvida = wb['teste']

        # MANIPULAÇÃO PLANILHA

for row in range(1, aba_hapvida.max_row + 1):
    contrato = str(aba_hapvida.cell(row=row, column=1).value)
    #input(f"Valor Celula:{valor_celula}\nContrato Procurado:{contrato_procurado}")
    
    #Checa se vencimento tem 1 caractere. Caso sim, acrescenta 0 na frente
    if len(str(aba_hapvida[f'G{row}'].value)) == 1:
        plan_venc = str(f"0{aba_hapvida[f'G{row}'].value}")
        plan_admn = str(aba_hapvida[f'C{row}'].value)
        plan_admn_edit = plan_admn.replace(" ", "")
        plan_tipo_cont = str(f"{aba_hapvida[f'F{row}'].value}")

    else:
        plan_venc = str(aba_hapvida[f'G{row}'].value)
        plan_admn = str(aba_hapvida[f'C{row}'].value)
        plan_admn_edit = plan_admn.replace(" ", "")
        plan_tipo_cont = str(aba_hapvida[f'F{row}'].value)

    
    if dia_venc == plan_venc and plan_admn_edit == "AFFIX" and tipo_contrato == plan_tipo_cont:
        cnpj = aba_hapvida[f'D{row}'].value
        
        
            # FLUXO DE NAVEGACAO
        # Acessar link nota fiscal hapvida affix
        navegador.get("https://www.hapvida.com.br/pls/webhap/webNewTrocaArquivo.login")

        # Tempo para carregar a página
        time.sleep(3)

        # Maximixar página
        navegador.maximize_window()
        
        realizarLogin(navegador, contrato, tipo_arquivo, "entidade", cnpj)

        if data_completa_convert <= data_hoje:
            arquivo_anterior = navegador.find_element(By.XPATH, "//a[text()='BAIXAR ARQUIVOS - DOWNLOAD (Anterior)']")
            arquivo_anterior.click()

            if tipo_contrato == "S":

                campo_pesquisa = navegador.find_element(By.XPATH, "//input[@type='search']")
                
                #limpa registros do campo 
                campo_pesquisa.clear()

                campo_pesquisa.send_keys(contrato)
                #procurar pelo contrato específico:
                linhas = navegador.find_elements(By.XPATH, "//tbody/tr")               

                for linha in linhas:
                    texto_da_linha = linha.text

                    try:
                        #Tenta pegar o período da linha atual
                        observacao = linha.find_element(By.XPATH, "./td[4]").text  
                        data_periodo_contrato = linha.find_element(By.XPATH, "./td[2]").text   
                        data_inicio = data_periodo_contrato[0:10]
                        data_fim = data_periodo_contrato[15:25]

                        if "/" in data_fim and data_inicio: 
                            data_inicio_convert = datetime.strptime(data_inicio, "%d/%m/%Y").date()
                            data_fim_convert = datetime.strptime(data_fim, "%d/%m/%Y").date()
            

                        if (data_completa_convert >= data_inicio_convert and data_completa_convert <= data_fim_convert) and ("Remessa" in observacao):
                            
                            continuar_paginacao_csv = True
                            continuar_paginacao_pdf = True



                            #OBSERVAÇÃO. ASSIM QUE ENTRAR NA PRÓXIMA PÁGINA, ELE DEVE RETORNAR AO PRIMEIRO FOR, PARA CHECAR SE EXISTE A DATA E A OBSERVAÇÃO.


                            # --- TRATAMENTO DO CSV ---
                            while continuar_paginacao_csv:
                                id_proximo = navegador.find_element(By.ID, "table_id_next")
                                classe_proximo = id_proximo.get_attribute("class")

                                if "CSV" in texto_da_linha:
                                    # Trocamos 'navegador' por 'linha' e adicionamos o '.' no início do XPath
                                    
                                    arquivo_csv = linha.find_element(By.XPATH, "./td[1]/small/a")
                                    arquivo_csv.click()
                                    time.sleep(2)
                                    baixar_csv = navegador.find_element(By.XPATH, ".//a[text()='clique aqui']")
                                    baixar_csv.click()
                                    navegador.find_element(By.XPATH, ".//a[text()='Voltar']").click()
                                    continuar_paginacao_csv = False
                                
                                elif classe_proximo == "paginate_button next":
                                    navegador.find_element(By.ID, "table_id_next").click()

                                elif classe_proximo == "paginate_button next disabled":
                                    navegador.find_element(By.XPATH, ".//*[@id='table_id_paginate']/span/a[1]").click()
                                    continuar_paginacao_csv = False




                            while continuar_paginacao_pdf:
                                id_proximo = navegador.find_element(By.ID, "table_id_next")
                                classe_proximo = id_proximo.get_attribute("class")
                                campo_pesquisa = navegador.find_element(By.XPATH, "//input[@type='search']")
                                #limnpa registros do campo 
                                campo_pesquisa.clear()
                                campo_pesquisa.send_keys(contrato)

                                if "PDF" in texto_da_linha:
                                    # Trocamos 'navegador' por 'linha' e adicionamos o '.' no início do XPath
                                    
                                    arquivo_csv = linha.find_element(By.XPATH, "./td[1]/small/a")
                                    arquivo_csv.click()
                                    time.sleep(2)
                                    baixar_csv = navegador.find_element(By.XPATH, ".//a[text()='clique aqui']")
                                    baixar_csv.click()
                                    navegador.find_element(By.XPATH, ".//a[text()='Voltar']").click()
                                
                                elif classe_proximo == "paginate_button next":
                                    navegador.find_element(By.ID, "table_id_next").click()

                                elif classe_proximo == "paginate_button next disabled":
                                    navegador.find_element(By.XPATH, ".//*[@id='table_id_paginate']/span/a[1]").click()
                                    continuar_paginacao_pdf = False
                                    


                            # --- TRATAMENTO DO PDF ---
                            if "PDF" in texto_da_linha:
                                # Trocamos 'navegador' por 'linha' e adicionamos o '.' no início do XPath
                                arquivo_pdf = linha.find_element(By.XPATH, ".//a[text()='PDF']")
                                arquivo_pdf.click()
                                time.sleep(2)

                    except NoSuchElementException:
                        print("Linha ignorada(não possui a coluna de período).")
                        continue


        else:
            arquivo_novo = navegador.find_element(By.XPATH, "//a[text()='BAIXAR ARQUIVOS - DOWNLOAD (Novo)']")
            arquivo_novo.click()
    
            
            #próxima página:
            if tipo_contrato == "S":
                #Com copart:
                
                campo_pesquisa = navegador.find_element(By.XPATH, "//input[@type='search']")
                
                #limnpa registros do campo 
                campo_pesquisa.clear()

                campo_pesquisa.send_keys(contrato)
                #procurar pelo contrato específico:
                linhas = navegador.find_elements(By.XPATH, "//tbody/tr")

                for linha in linhas:
                    texto_da_linha = linha.text

                    if data_completa_venc in texto_da_linha and "COPART" in texto_da_linha:
                        
                        # --- TRATAMENTO DO CSV ---
                        if "CSV" in texto_da_linha:
                            # Trocamos 'navegador' por 'linha' e adicionamos o '.' no início do XPath
                            arquivo_csv = linha.find_element(By.XPATH, ".//a[text()='CSV']")
                            arquivo_csv.click()
                            time.sleep(2) # Pausa curta para o navegador processar o download antes do próximo clique
  
                        # --- TRATAMENTO DO PDF ---
                        if "PDF" in texto_da_linha:
                            # Trocamos 'navegador' por 'linha' e adicionamos o '.' no início do XPath
                            arquivo_pdf = linha.find_element(By.XPATH, ".//a[text()='PDF']")
                            arquivo_pdf.click()
                            time.sleep(2)




        























"""
    # Seleciona a nota fiscal de acordo com vencimento e empresa
    time.sleep(3) # Espera carregar após login
    opcoes_elementos = navegador.find_elements(By.XPATH, f"//a[contains(@href, 'pCd_Empresa={contrato}') and contains(text(), '{dia_venc}/{mes_venc}/{ano_venc[-2:]}')]")
    total_contratos = len(opcoes_elementos)
    
    contagem = 0
    contagem_pag = 0

    
    while True:
        contagem_pag +=1
        confere_data = navegador.find_element(By.XPATH, f"/html/body/div[2]/div/div/table/tbody/tr[1]/td[4]/a")
        valor_data = confere_data.text
        data_convertida_site = datetime.strptime(valor_data, "%d/%m/%y")
        data_convertida_user = datetime.strptime(f'{dia_venc}/{mes_venc}/{ano_venc[-2:]}', "%d/%m/%y")

        if data_convertida_site < data_convertida_user:
            print(f"{data_convertida_site} + Vencimentos anteriores")
            navegador.quit()
            break

        if total_contratos == 0:
            print(f"Página {contagem_pag}: Contem {total_contratos} para contrato: {contrato}.")
            proxima_pagina = navegador.find_element(By.LINK_TEXT, "Próxima »")
            proxima_pagina.click()
            
            
        else:
            for i in range(total_contratos):
                print(f"Página {contagem_pag}: Contem {total_contratos} para contrato: {contrato}.")
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

                contagem +=1

                if contagem == 2:
                    print("Dois contratos encontrados. Encerrando navegador.")
                    navegador.quit()
                    break

        if contagem == 2:
            break

"""



    
