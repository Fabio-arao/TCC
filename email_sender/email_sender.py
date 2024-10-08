import requests, os, urllib, mimetypes, random, string
from requests_toolbelt import MultipartEncoder
from sqlalchemy.orm import sessionmaker
import sqlalchemy


class SendEmail():
    def __init__(self, path, ends=[]) -> None:
        self.engine_prod = sqlalchemy.create_engine('mysql+pymysql://admin:30ProdTur2530##C#30MySQl@db-turn2c-prod.ccgj4tnt68yu.us-east-2.rds.amazonaws.com/turn2c_prod')
        self.path = path
        self.ends = ends
        self.url = 'http://20.55.45.88:/' # HOMOLOG - 'http://192.168.10.38:8082/'  
        self.signin = 'apibot/auth/signin'
        self.enviar_email = 'apibot/bots-email/enviar-email'
        self.adicionar_arquivo = 'apibot/bots-email/adicionar-arquivo'
        self.listar_tipos = 'apibot/bots-email/listar-tipos'
        #DADOS DE ACESSO EM PRODUÇÃO
        self.login_info = {
                          "password": "E#J49t4Fq8^f1bTygwLU!2H9k",
                          "username": "botpython@turn2c.com"
                          }
        
        #DADOS DE ACESSO EM HOMOLOG - ou acessar com outro acesso ativo
        '''self.login_info = {
                          "password": "bruno.duarte@turn2c.com",
                          "username": "12345@Senha1"
                          }'''
        
        self.token = self.get_token()          
        if self.listar() == 200:
            pass
        else:   
            self.token = self.login()             
    
    def get_token(self):
        Session = sessionmaker(bind=self.engine_prod)
        session = Session()
        result = session.execute(f"SELECT bearer FROM users WHERE email ='{self.login_info.get('username')}'")
        return result.first()[0]            
    
    def login(self):
        token = requests.post(self.url+self.signin,  json=self.login_info) 
        #print(token.content)       
        return str(token.json()['tokenType']) + ' ' + str(token.json()['accessToken'])       
    
    def send_email(self, assunto, conteudo, destino, tipoTemplateEmail, titulo, tipo_fila, ocultos=None, copiados=None):
        #FORMATO ARQUIVOS - ("arquivos", ('results.xlsx', open('results.xlsx', 'rb'), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')),
        
        fields  = [
                  ("destino", destino.split(';')[0]),         
                  ("assunto", assunto),
                  ("conteudo", conteudo),
                  ("processarFila", 'true'),
                  ("titulo",titulo),          
                  ("tipoTemplateEmail", tipoTemplateEmail),
                  ("tipoFila", tipo_fila),                  
                  ]
        
        self.add_files(fields, self.path, self.ends)
        
        if ocultos != None:
          fields.append(('ocultos', ocultos))

        if copiados != None:
          fields.append(('copiados', copiados))    

        if len(destino.split(';')) > 1:
            fields.append(('destinatarios', destino)) 
        
        boundary = '----WebKitFormBoundary' \
           + ''.join(random.sample(string.ascii_letters + string.digits, 16))
        headers = {                      
                  "Authorization" : self.token,                
                  "Content-Type": f'multipart/form-data; boundary={boundary}',                  
                  } 
        #print(fields)
        #files = self.adicionar_arquivos(self.path, self.ends) 
        m = MultipartEncoder(fields=fields, boundary=boundary)      
        res = requests.post(self.url+self.enviar_email, headers=headers, data=m)
        print(res.status_code)        

    def listar(self):           
        res = requests.post(self.url+self.listar_tipos, headers={"Authorization" : self.token} )        
        return res.status_code
    
    def get_mime(self, arquivo):
        url = urllib.request.pathname2url(arquivo)
        return mimetypes.guess_type(url)[0]
    
    def add_files(self, fields, path, ends):        
        for arquivo in os.listdir(path):          
            if str(arquivo).split('.')[-1] in ends:              
                file = ("arquivos", (arquivo, open(arquivo, 'rb'), self.get_mime(arquivo)))                
                fields.append(file)
        
       

'''assunto = 'Assunto de Teste'
conteudo = 'testanto api de emails'
destino = 'bruno.duarte@turn2c.com;fabio.arao@turn2c.com'
tipoTemplateEmail = 'COMUNICACAO_INTERNA'
titulo = 'Olá tester'
tipo_fila = 'COMUNICACAO_INTERNA'

SendEmail(os.getcwd(), ['xlsx']).send_mails(
                                            assunto=assunto,
                                            conteudo=conteudo,
                                            destino=destino,
                                            tipoTemplateEmail=tipoTemplateEmail,
                                            titulo=titulo,
                                            tipo_fila=tipo_fila
                                            )
'''
      








