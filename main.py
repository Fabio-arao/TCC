from page_element.page_element import ConfigWebDriver
from selenium.webdriver import Chrome
from bot.bot import BacenBot
from bot.config import *
import os


class Application():
    """
    Classse principal do Bot
    """
    def __init__(self):
        """
        Método construtor que inicia a aplicação.
        """
        self.start, self.max = TRYS.get('start'), TRYS.get('max')  
        self.run_bot()   
    
    def execute_bot(self):
        """
        Inicia a execuçao do Bot.
        """
        self.config = ConfigWebDriver() 
        self.webdriver = Chrome(service=self.config.s, options=self.config.opt) 
        self.bot = BacenBot(self.webdriver)     
        
    def run_bot(self):
        """
        Contabiliza a execução do bot, 
        e envia um  email de advertência caso o bot nao consiga ser finalizado. 
        """    
        while self.start <= self.max: 
            try: 
                print_log(f'Rodando o bot pela {self.start}a vez') 
                self.execute_bot()   
                self.bot.collect_data_all()
                self.bot.delete_sheets('.xlsx', '.csv') 
                self.webdriver.close()   
                break 
            except:       
                self.bot.remove_zip_csv()   
                self.bot.delete_sheets('.xlsx', '.csv')               
                self.start += 1 
                self.webdriver.quit()  
                if self.start <= self.max:                                
                    self.run_bot() 
                else:                                   
                    self.webdriver.close()  
                    print_log(f'Erro na coleta dos dados {self.start}a vez')

if __name__ == "__main__":
    setup_log(os.getcwd())
    Application()
    exit()
