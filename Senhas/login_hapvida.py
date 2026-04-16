from selenium import webdriver
from selenium.webdriver.common.by import By
import time


def realizarLogin(navegador, contrato, tipo_arquivo, entidade):
    x = navegador
    contratos = contrato
    empresa = entidade
    #preencher campos login
    if tipo_arquivo == "hapvida_boleto":
        x.find_element("name", "pCodigo").send_keys(contratos)
        x.find_element("name", "pSenha").send_keys("")
        time.sleep(5)
        botao = navegador.find_element(By.ID, "btn_reajuste1")
        botao.click()

    if tipo_arquivo == "hapvida_nota":
        #"UNEB1", "AFPU1", "FETR1", "ALT88", "09BGF"

        x.find_element("name", "pCodigoEmpresa").send_keys(contratos)
        x.find_element("name", "pSenha").send_keys("")
        time.sleep(5)
        botao = navegador.find_element(By.ID, "bt_entrar")
        botao.click()



    
