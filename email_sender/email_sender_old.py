from bot.bot import BacenBot
import os, sqlalchemy, json, io, uuid
from sqlalchemy.orm import sessionmaker
from datetime import date, datetime
import pandas as pd
import boto3


class SendEmail():
    def __init__(self):
        self.engine_prod = sqlalchemy.create_engine('mysql+pymysql://admin:30ProdTur2530##C#30MySQl@db-turn2c-prod.ccgj4tnt68yu.us-east-2.rds.amazonaws.com/turn2c_prod')
        self.s3 = boto3.resource('s3')

    def get_columns(self, table_name):
        Session = sessionmaker(bind=self.engine_prod)
        session = Session()
        result = session.execute(f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = 'turn2c_prod' AND TABLE_NAME = '{table_name}'")
        columns = [str(i).replace("('", "").replace("',)", "")  for i in result.all()]
        return columns

    def get_fil_id(self, fil_id):
        Session = sessionmaker(bind=self.engine_prod)
        session = Session()
        result = session.execute(f"SELECT fil_id FROM sistema_fila WHERE fil_codigo = '{fil_id}'")
        return result.first()[0]
    
    def feed_sistema_fila(self, html, subject, worked=True):
        """alimenta a tabela turn2c_sistema_fila, para envio de email

        Args:
            html (string): arquivo html
            subject (string): assunto do email
            status_to_change (string): status da proposta a ser alterada
            email_vendedor (string): email do vendedor
            email_subgerente (string): email do subgerente
        """
        #self.df_sistema_fila_columns = pd.read_sql_table('sistema_fila',self.engine_prod)
        df_sistema_fila = pd.DataFrame(columns=self.get_columns('sistema_fila'))
        fil_id = None
        fil_assunto = subject
        self.fil_codigo = str(uuid.uuid4().hex)
        fil_conteudo = html
        fil_data_alt = None
        fil_data_fim = None
        fil_data_ini = datetime.today().strftime("%Y/%m/%d %H:%M:%S")
        if worked:
            fil_destino = 'vagner.lopes@turn2c.com' 
            fil_copiados = 'thiago.ramos@turn2c.com;fabio.arao@turn2c.com'
            fil_status = 'INATIVO' 
        else:
            fil_destino = 'fabio.arao@turn2c.com'
            fil_copiados = 'fabio.arao@turn2c.com'
            fil_status = 'ATIVO' 
        fil_enviado = 'NAO'
        fil_etapa = 'COMUNICACAO_INTERNA'
        fil_habilitado = 'HABILITADO'
        fil_instancia = 100
        fil_minutos = 1        
        fil_tentativas = 0
        fil_tipo = 'EMAIL'
        fil_user_id = None
        fil_tca_id = None
        fil_destinatarios = None
        fil_ocultos =  None 

        df_sistema_fila.loc[int(len(df_sistema_fila) + 1)] = fil_id, fil_assunto, self.fil_codigo, fil_conteudo, fil_data_alt, fil_data_fim, fil_data_ini, fil_destino, fil_enviado, fil_etapa, fil_habilitado, fil_instancia, fil_minutos, fil_status, fil_tentativas, fil_tipo, fil_user_id, fil_tca_id, fil_copiados, fil_destinatarios, fil_ocultos
           
        df_sistema_fila.to_sql(
            name = 'sistema_fila',
            con = self.engine_prod,
            index = False,
            if_exists ='append'
            )

        if worked:
            self.feed_sistema_fila_anexo(self.upload_files())
            self.change_email_status()  
        
    def feed_sistema_fila_anexo(self, key_list):
        """alimenta os anexos do sistema fila

        Args:
            key_list (lista): lista com os nomes dos arquivos a serem anexados no email
        """          
      
        df_sistema_fila_anexo_to_add = pd.DataFrame(columns=self.get_columns('sistema_fila_anexo'))
        for key in key_list:
            fia_id = None
            fia_arquivo = key
            fia_codigo = str(uuid.uuid4().hex)      
            fia_data_alt = None
            fia_data_fim = None
            fia_data_ini = datetime.today().strftime("%Y/%m/%d %H:%M:%S")        
            fia_habilitado = 'HABILITADO'
            fia_instancia = 100
            fia_nome_arquivo = key
            fia_status = 'ATIVO'
            fia_user_id = None          
            fia_fil_id = self.get_fil_id(self.fil_codigo)

            df_sistema_fila_anexo_to_add.loc[int(len(df_sistema_fila_anexo_to_add) + 1)] = fia_id, fia_arquivo, fia_codigo, fia_data_alt, fia_data_fim, fia_data_ini, fia_habilitado, fia_instancia, fia_nome_arquivo, fia_status, fia_user_id, fia_fil_id
             
        try:
            df_sistema_fila_anexo_to_add.to_sql(
                name = 'sistema_fila_anexo',
                con = self.engine_prod,
                index = False,
                if_exists ='append'
                )
        except:
            pass

    def change_email_status(self):
        """Altera o status do email para ATIVO - autoriza o envio
        """
        conn = self.engine_prod.connect()
        trans = conn.begin()
        conn.execute(f'UPDATE sistema_fila SET fil_status = "ATIVO" WHERE fil_codigo = "{self.fil_codigo}";')   
        trans.commit()

    def upload_files(self):  
        """sobe os arquivos para AWS

        Returns:
            list: lista com o nome dos aquivos que foram feito upload
        """
        key_list = []  
        for file in os.listdir(os.getcwd()):  
            if file.endswith('.xlsx') and len(pd.read_excel(os.getcwd() + '\\' + file)) > 0 and file != 'grupos.xlsx':
                self.key = file.replace('.xlsx', '_' + str(date.today()) + '_' + BacenBot.__name__ + '.xlsx' )
                key_list.append(self.key)
                data = open(os.getcwd() + '\\' + file, 'rb') 
                self.s3.Bucket('turn2c-dev').put_object(Key=self.key, Body=data)            
        return key_list



    
