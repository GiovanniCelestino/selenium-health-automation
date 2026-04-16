from selenium import webdriver
from selenium.webdriver.common.by import By
import time


def realizarLogin(navegador):
    #preencher campos login
    navegador.find_element("name", "pCodigoEmpresa").send_keys("0DGYF")
    navegador.find_element("name", "pSenha").send_keys("072024")
    time.sleep(5)
    #logar
    botao = navegador.find_element(By.ID, "bt_entrar")
    botao.click()
    