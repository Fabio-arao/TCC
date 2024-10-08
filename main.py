from page_element.page_element import ConfigWebDriver
from selenium.webdriver import Chrome
from bot.bot import BacenBot
from bot.config import *
import os


class Application():
    """
    Classse principal do Bot
    """
    def __init__(self, 
                 i=1, 
                 max=10            
                 ):
        """
        Método construtor que inicia a aplicação.
        Args:
            i (integer): valor inicial será utilizado pelo método run_bot, sendo incrementado a cada execução.
            max (integer): valor final será utilizado pelo método run_bot, 
                como referência máxima no total de tentativas de execução.
        """
        self.i, self.max  = i, max
        self.run_bot()   
    
    def execute_bot(self):
        """
        Inicia a execuçao do Bot.
        """
        self.config = ConfigWebDriver() 
        self.webdriver = Chrome(service=self.config.s, options=self.config.options) 
        self.bot = BacenBot(self.webdriver)     
        
    def run_bot(self):
        """
        Contabiliza a execução do bot, 
        e envia um  email de advertência caso o bot nao consiga ser finalizado. 
        """    
        while self.i <= self.max: 
            try: 
                print_log(f'Rodando o bot pela {self.i}a vez') 
                self.execute_bot()   
                self.bot.collect_data_all()
                self.bot.delete_sheets('.xlsx', '.csv') 
                self.webdriver.close()   
                break 
            except:       
                self.bot.remove_zip_csv()                  
                self.i += 1 
                self.webdriver.quit()  
                if self.i <= self.max:                                
                    self.run_bot() 
                else:                                   
                    self.webdriver.close()  
                    print_log(f'Erro na coleta dos dados {self.i}a vez')

if __name__ == "__main__":
    setup_log(os.getcwd())
    Application()
    exit()
