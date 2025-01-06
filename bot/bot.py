from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from page_element.page_element import PageElement
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pandas as pd
import os, zipfile
import time



class BacenBot(PageElement):
    """
    Classe que herda todos os métodos da classe PageElement.
    classe recebe todos os locators e métodos responsáveis pelo desenvolvimento do Bot.
    
    Args:
        PageElement(class): Classe abstrata
    """
    def download_database_cons(self):
        """
        Faz o Download da base de dados. 
        """
        self.wait_(30).until(EC.title_is('Banco de dados - consórcios'))
        self.wait_(30).until(EC.presence_of_element_located((By.ID,'framelegado')))  
        self.switch_to_frame('framelegado')  
        ini = 'Março/2024 (435 KB)'
        end = 'Março/2018 (426 KB)'
        all_selected_options = Select(self.find((By.ID, 'Consorcios'))).options    #Março/2018   

        for i, op in enumerate(all_selected_options):
            if ini in op.text:
                init = i

        for i, op in enumerate(all_selected_options):
            if end in op.text:
                finals = i

        for op in all_selected_options[init : finals+1]: 
            Select(self.find((By.ID, 'Consorcios'))).select_by_visible_text(op.text)
            self.find((By.ID, 'Consorcios')).send_keys(Keys.NULL)
            ActionChains(self.webdriver).send_keys(Keys.TAB + Keys.ENTER).perform() 
            time.sleep(1) 
                 
        zip_archive = [] 
        
        for file in os.listdir():     
            if file.endswith(".zip"): 
                zip_archive.append(file) 

        for zip_a in zip_archive:        
            with zipfile.ZipFile(zip_a) as thezip:
                for file in thezip.namelist(): 
                    if 'Imoveis' in thezip.getinfo(file).filename:
                        filename = thezip.getinfo(file).filename
                        thezip.extract(file) 

        csv_archive = []         
        for file in os.listdir():     
            if file.endswith(".csv"): 
                csv_archive.append(file) 

        df_new = pd.DataFrame(columns=pd.read_csv(csv_archive[0], encoding = 'LATIN-1', sep=';').columns)
        for csv in csv_archive:
            print(f'Estou no arquivo {csv}')
            df = pd.read_csv(csv, encoding = 'LATIN-1', sep=';')
            for i, line in df.iterrows():
                if str(line['Código_do_segmento']) == str(1):
                    df_new.loc[int(len(df_new) + 1)] = line 

        df_new.to_excel(os.getcwd() + '\\bacen_consorcio.xlsx', index=False)  
        self.remove_zip_csv()

    def download_database_cons_2(self):
        """
        Faz o Download da base de dados. 
        """
        self.open_url('https://www.bcb.gov.br/estabilidadefinanceira/consorciobd')
        self.wait_(30).until(EC.title_is('Banco de dados - consórcios'))
        self.wait_(30).until(EC.presence_of_element_located((By.ID,'framelegado')))  
        self.switch_to_frame('framelegado') 
        all_selected_options = Select(self.finds((By.ID, 'Consorcios'))[1]).options      
        
        ini = 'Março/2024 (95 KB)'
        end = 'Março/2018 (75 KB)'

        for i, op in enumerate(all_selected_options):
            if ini in op.text:
                init = i

        for i, op in enumerate(all_selected_options):
            if end in op.text:
                finals = i

        for op in all_selected_options[init : finals+1]:                                
            Select(self.finds((By.ID, 'Consorcios'))[1]).select_by_visible_text(op.text)
            self.finds((By.ID, 'Consorcios'))[1].send_keys(Keys.NULL)
            ActionChains(self.webdriver).send_keys(Keys.TAB + Keys.ENTER).perform() 
            time.sleep(1)        
        zip_archive = [] 
        
        for file in os.listdir():     
            if file.endswith(".zip"): 
                zip_archive.append(file) 

        for zip_a in zip_archive:        
            with zipfile.ZipFile(zip_a) as thezip:
                for file in thezip.namelist(): 
                    if 'Consorcios_UF' in thezip.getinfo(file).filename:
                        filename = thezip.getinfo(file).filename
                        thezip.extract(file) 

        csv_archive = []         
        for file in os.listdir():     
            if file.endswith(".csv"): 
                csv_archive.append(file) 

        df_new = pd.DataFrame(columns=pd.read_csv(csv_archive[0], encoding = 'LATIN-1', sep=';').columns)
        for csv in csv_archive:
            df = pd.read_csv(csv, encoding = 'LATIN-1', sep=';')
            for i, line in df.iterrows():
                if str(line['Código_do_segmento']) == str(1):
                    df_new.loc[int(len(df_new) + 1)] = line 

        df_new.to_excel(os.getcwd() + '\\bacen_consorcio_UF.xlsx', index=False)  
        self.remove_zip_csv()
              
    def remove_zip_csv(self):
        """
        Remove_zip_csv remove os arquivos .zip e .csv no diretório
        """
        archive = []
        for file in os.listdir():     
            if file.endswith(".zip") or file.endswith(".csv"): 
                archive.append(file)
        for i, item in enumerate(archive):
            os.remove(archive[i])
    
    def click_in_element(self, element, index):
        visible = False
        while not visible:
            time.sleep(0.9)
            self.webdriver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element[index])
            time.sleep(0.9)
            visible = element[index].is_displayed()
            time.sleep(0.9)
            if not visible:
                time.sleep(0.9)
        time.sleep(0.9)
        element[index].click()
        time.sleep(0.9)
        try:
            self.find((By.XPATH, "//*[contains(text(), 'Baixar arquivo CSV')]")).click()
        except:
            self.finds((By.CSS_SELECTOR, "li[class='highcharts-menu-item']"))[-2].click()
        time.sleep(2)

    def download_database_finan(self):
        try:
            time.sleep(2)
            self.find((By.XPATH, "//*[contains(text(), 'Prosseguir')]")).click()
            time.sleep(2)
            dados = self.finds((By.CSS_SELECTOR, "g[class='highcharts-exporting-group']"))
            time.sleep(10)
            self.click_in_element(dados, 8)
            self.click_in_element(dados, 10)
            self.click_in_element(dados, 12)
            self.click_in_element(dados, 14)
            self.click_in_element(dados, 26)
            self.click_in_element(dados, 30)
            time.sleep(2)
        except Exception as e:
            print(e)
            time.sleep(2)
    
    def convert_xlsx(self):
        path = os.getcwd()
        arq = os.listdir(path)
        for arquivo in arq:
            if arquivo.endswith('.csv'):
                arquivo = arquivo.split(".")[0]
                read_file = pd.read_csv(f'{arquivo}.csv', sep=';', encoding='utf-8')
                read_file.to_excel(f'{arquivo}.xlsx', index=0)
        self.df_convert()
        
    def convert_to_numeric(self, df, columns):
        for col in columns:
            try:
                df[col] = df[col].str.replace('.', '', regex=False)  
                df[col] = df[col].str.replace(',', '.', regex=False)  
            except:
                df[col] = df[col].replace('.', '', regex=False)  
                df[col] = df[col].replace(',', '.', regex=False) 
            df[col] = df[col].astype(float) 
        return df

    def create_colum_taxa_and_credit(self, new_df_finan, df, column):
        for i , v in df.iterrows():
            taxa = v[column]
            print(taxa)
            if 'Credito_medio_PF' in column:
                new_df_finan.loc[i, column] = f'{float(taxa):,.4f}'
            elif 'Credito_medio_PJ' in column:
                new_df_finan.loc[i, column] = f'{float(taxa) / 1000:,.4f}'
            else:
                new_df_finan.loc[i, column] = f'{float(taxa):,.2f}'

    def transform_df_corrent_date(self,df_pfis, df_pjur, df_pf, df_pj):
        dataframes = {
            'valor-contratado': df_pfis,
            'valor-contratado (1)': df_pjur,
            'chart': df_pf,
            'chart (1)': df_pj
        }

        for name, df in dataframes.items():
            df['DateTime'] = pd.to_datetime(df['DateTime'], format='%Y-%m-%d')
            start_date = pd.to_datetime('31/03/2018', format='%d/%m/%Y')
            filtered_df = df[df['DateTime'] >= start_date]
            filtered_df['DateTime'] = filtered_df['DateTime'].dt.strftime('%d/%m/%Y')
            filtered_df.to_excel(os.getcwd() + f"\\{name}.xlsx", index=False)

    def df_convert(self):
        df_valor = pd.read_excel(os.getcwd() + "\\valor.xlsx")
        df_tipo_imov = pd.read_excel(os.getcwd() + "\\tipo-de-imvel.xlsx")
        df_pfis = pd.read_excel(os.getcwd() + "\\valor-contratado.xlsx")
        df_pjur = pd.read_excel(os.getcwd() + "\\valor-contratado (1).xlsx")
        df_pf = pd.read_excel(os.getcwd() + "\\chart.xlsx")
        df_pj = pd.read_excel(os.getcwd() + "\\chart (1).xlsx")
        self.transform_df_corrent_date(df_pfis, df_pjur, df_pf, df_pj)
        colums = ['Data', 'Qtd_aquisições', 'Mediana_Valor_aquisições', 'Credito_medio_PF', 'Taxa_media_PF','Credito_medio_PJ','Taxa_media_PJ','Bem']
        new_df_finan = pd.DataFrame(columns=colums) 
        df_tipo_imov = self.convert_to_numeric(df_tipo_imov,['Apartamento', 'Casa'])
        for _, valor in df_tipo_imov.iterrows():
            valor_ok = float(valor['Apartamento']) + float(valor['Casa'])
            new_df_finan.loc[int(len(new_df_finan)) + 1] = valor['DateTime'], int(valor_ok), '', '', '', '', '', 'IMÓVEL'
        new_df_finan.to_excel(os.getcwd() + "\\bacen_financiamento.xlsx", index=False)

        #TRATAMENTO E CONVERSAO X 1000 POIS OS DADOS ESTAO EXPRESSADOS EM MILHARES DE R$
        new_df_finan = pd.read_excel(os.getcwd() + "\\bacen_financiamento.xlsx")
        for i, v_comp in enumerate(df_valor['Compra']):
            new_df_finan.loc[i, 'Mediana_Valor_aquisições'] = f'{float(v_comp.replace(",",".")) * 1000:,.2f}'
        new_df_finan.to_excel(os.getcwd() + "\\bacen_financiamento.xlsx", index=False)

        # FILTRAR O DATAFRAME PARA OBTER OS DADOS A PARTIR DA DATA ESPECIFICADA
        new_df_finan = pd.read_excel(os.getcwd() + "\\bacen_financiamento.xlsx")
        start_date = '2018-03-31'
        end_date = '2024-04-30'
        filtered_df = new_df_finan[(new_df_finan['Data'] >= start_date) & (new_df_finan['Data'] < end_date)]
        filtered_df.to_excel(os.getcwd() + "\\bacen_financiamento.xlsx", index=False)
        new_df_finan = pd.read_excel(os.getcwd() + "\\bacen_financiamento.xlsx")
        try:
            df_pf = self.convert_to_numeric(df_pf,['SFH','FGTS','Livre','Comercial','Home Equity'])
            df_pj = self.convert_to_numeric(df_pj,['SFH','FGTS','Livre','Comercial'])
            df_pf['Taxa_media_PF'] = df_pf['SFH']
            df_pj['Taxa_media_PJ'] = df_pj['SFH']

            #PESSOA FISICA
            df_pfis = self.convert_to_numeric(df_pfis, ['Comercial','Home Equity','Livre','FGTS','SFH'])
            df_pfis['Credito_medio_PF'] = df_pfis['SFH']

            #PESSOA JURIDICA FAZER / 1000 POIS ESTÁ EM MILHOES E TEMOS QUE TRANSFORMAR EM BILHOES
            df_pjur = self.convert_to_numeric(df_pjur, ['Comercial','FGTS','Livre','SFH'])
            df_pjur['Credito_medio_PJ'] = df_pjur['SFH']
            self.create_colum_taxa_and_credit(new_df_finan, df_pf,'Taxa_media_PF')
            self.create_colum_taxa_and_credit(new_df_finan, df_pj,'Taxa_media_PJ')
            self.create_colum_taxa_and_credit(new_df_finan, df_pfis,'Credito_medio_PF')
            self.create_colum_taxa_and_credit(new_df_finan, df_pjur,'Credito_medio_PJ')
            new_df_finan = new_df_finan.dropna()

            #TRATAMENTO DA COLUNA DATA PARA PADRAO NACIONAL
            new_df_finan['Data'] = pd.to_datetime(new_df_finan['Data'], format='%Y-%m-%d')
            new_df_finan['Data'] = new_df_finan['Data'].dt.strftime('%d/%m/%Y')
            new_df_finan.to_excel(os.getcwd() + "\\sheets\\bacen_financiamento.xlsx", index=False)
        except Exception as e:
            print(e)
        
    def distribute_trimestral_to_monthly(self, df):
        result = []
        for _, row in df.iterrows():
            year_month = row['#Data_base']
            year = int(str(year_month)[:4])
            month = int(str(year_month)[4:])
            # MAPEAMENTO DE TRIMESTRE PARA MESES CORRESPONDENTES
            if month == 3:
                months = [(year, 1), (year, 2), (year, 3)]
            elif month == 6:
                months = [(year, 4), (year, 5), (year, 6)]
            elif month == 9:
                months = [(year, 7), (year, 8), (year, 9)]
            elif month == 12:
                months = [(year, 10), (year, 11), (year, 12)]
            
            value = row['Quantidade_de_adesões_no_trimestre']
            base_value = value // 3
            remainder = value % 3
            
            # DISTRIBUI OS VALORES IGUALMENTE E AJUSTA O RESTO
            for i in range(3):
                month_year, month = months[i]
                # ADICIONA 1 AOS PRIMEIRO 'REMAINDER' MES PARA DISTRIBUIR O RESTO
                qtd_month = base_value + (1 if i < remainder else 0)
                
                result.append({
                    'Data': str(month_year) + "/" + str(month) + '/01',
                    'Quantidade_de_adesões_no_mês': qtd_month
                })
        df = pd.DataFrame(result)
        df['Data'] = pd.to_datetime(df['Data'], format='%Y/%m/%d')
        df_grouped = df.sort_values(by='Data').reset_index(drop=True)
        df_grouped = df.groupby(df['Data']) \
                        .agg({'Quantidade_de_adesões_no_mês': 'sum'}) \
                        .reset_index()
        df_grouped['Quantidade_de_adesões_no_mês'] = df_grouped['Quantidade_de_adesões_no_mês'].astype(int)
        return df_grouped

    def convert_to_numeric2(self, df, columns):
        for col in columns:
            try:
                df.loc[:, col] = df[col].str.replace('.', '', regex=False)  
                df.loc[:, col] = df[col].str.replace(',', '.', regex=False)  
            except:
                df.loc[:, col] = df[col].replace('.', '', regex=False) 
                df.loc[:, col] = df[col].replace(',', '.', regex=False)  
            df.loc[:, col] = df[col].astype(float)  
        return df

    def refactory_consorcio_ac(self):
        df_cons = pd.read_excel(os.getcwd() + "\\bacen_consorcio.xlsx")
        df_cons['Data_base'] = df_cons['Data_base'].astype(str).str[:4] + '/' + df_cons['Data_base'].astype(str).str[4:6] + '/01'
        df_cons['Data_base'] = pd.to_datetime(df_cons['Data_base'], format='%Y/%m/%d')
        df_cons = df_cons.drop(columns=['#Nome_da_Administradora', 
                                        'CNPJ_da_Administradora', 
                                        'Código_do_grupo',
                                        'Código_do_segmento', 
                                        'Número_da_assembléia_geral_ordinária',
                                        'Índice_de_correção',
                                        'Prazo_do_grupo_em_meses',
                                        'Quantidade_de_cotas_ativas_em_dia', 
                                        'Quantidade_de_cotas_ativas_contempladas_inadimplentes',
                                        'Quantidade_de_cotas_ativas_não_contempladas_inadimplentes',
                                        'Quantidade_de_cotas_ativas_contempladas_no_mês',
                                        'Quantidade_de_cotas_excluídas',
                                        'Quantidade_de_cotas_ativas_quitadas',
                                        'Quantidade_de_cotas_ativas_com_crédito_pendente_de_utilização'])

        #AJUSTA A BASE CONFORME O INTEVALO DE DATA PASSADO
        df_cons['Data_base'] = pd.to_datetime(df_cons['Data_base']).dt.date
        start_date = pd.to_datetime('2018-03-01').date()
        end_date = pd.to_datetime('2024-04-01').date()
        df_ = df_cons[(df_cons['Data_base'] >= start_date) & (df_cons['Data_base'] < end_date)]
        df_ = self.convert_to_numeric2(df_, ['Valor_médio_do_bem','Taxa_de_administração'])

        #DATAFRAME CALCULADO COM A SOMA DO VALOR MEDIO POR MES, E A MEDIA DAS TAXAS MEDIAS
        df= pd.read_excel(os.getcwd() + "\\bacen_consorcio_UF.xlsx")
        df_grouped = self.distribute_trimestral_to_monthly(df)
        df_ = df_.sort_values(by='Data_base').reset_index(drop=True)
        df_new = df_.groupby(df_['Data_base']) \
                        .agg({'Valor_médio_do_bem': 'sum',
                            'Taxa_de_administração': 'mean'}) \
                        .reset_index()

        df_grouped['Data'] = pd.to_datetime(df_grouped['Data']).dt.date
        df_new['Data_base'] = pd.to_datetime(df_new['Data_base']).dt.date

        # CRIANDO UM DICIONÁRIO PARA MAPEAR DATA PARA QUANTIDADE_DE_ADESÕES_NO_MÊS EM DF_GROUPED
        mapping = {row['Data']: row['Quantidade_de_adesões_no_mês'] for _, row in df_grouped.iterrows()}

        # ITERANDO SOBRE DF_ E ATUALIZANDO QUANTIDADE_DE_ADESÕES_NO_MÊS
        for i, valor in df_new.iterrows():
            data_base = valor['Data_base']
            if data_base in mapping:
                # ATUALIZANDO O VALOR NA COLUNA 'QUANTIDADE_DE_ADESÕES_NO_MÊS'
                df_new.at[i, 'Quantidade_de_adesões_no_mês'] = mapping[data_base]
                print(f"Correspondência encontrada para {data_base} com valor {mapping[data_base]}")
            else:
                print(f"Nenhuma correspondência encontrada para {data_base}")
        df_new['Data_base'] = pd.to_datetime(df_new['Data_base'], format='%Y-%m-%d %H:%M:%S')
        df_new['Data_base'] = df_new['Data_base'].dt.strftime('%d/%m/%Y')
        df_new.to_excel(os.getcwd() + "\\sheets\\bacen_consorcios_acumulado.xlsx", index=False)

    def delete_sheets(self, end, ends): 
        for file in os.listdir(os.getcwd()):
            print(file)
            try:
                if str(file).endswith(end):
                    os.remove(os.getcwd() + f'\\{file}')
                elif str(file).endswith(ends):
                    os.remove(os.getcwd() + f'\\{file}')
            except Exception as e:
                print(e)

    def collect_data_all(self):
        self.open_url('https://www.bcb.gov.br/estabilidadefinanceira/consorciobd')
        self.download_database_cons() 
        self.download_database_cons_2()
        self.open_url('https://www.bcb.gov.br/estatisticas/mercadoimobiliario') 
        self.download_database_finan()
        self.convert_xlsx()
        self.refactory_consorcio_ac()
                