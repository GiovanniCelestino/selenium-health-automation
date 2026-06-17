from selenium import webdriver
import os
import sys
import time
caminho_absoluto = os.path.abspath(os.curdir)
sys.path.insert(0, caminho_absoluto)
from Senhas.login_ccg import realizarLogin



#https://www.youtube.com/watch?v=spXh5vDKaZU
#Importando arquivos de hierarquias abaixo em Python




#abrir navevagor (instanciando)
navegador = webdriver.Chrome()

#acessar link nota fiscal hapvida
navegador.get("https://sigo.sh.srv.br/pls/webccg/pk_nota_fiscal.login")

# colocar o navegador em tela cheia
navegador.maximize_window()

#realizar login (Affix/Operadoras/Senhas/login.py)
realizarLogin(navegador)

time.sleep(100)