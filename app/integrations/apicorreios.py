from zeep import Client
import zeep.exceptions
 
def consultaCEP(cep):
    try:
        #Link direto dos Correios -> Homologação/Produção
        client = Client('https://apphom.correios.com.br/SigepMasterJPA/AtendeClienteService/AtendeCliente?wsdl')
        #client = Client('https://apps.correios.com.br/SigepMasterJPA/AtendeClienteService/AtendeCliente?wsdl')
        result = client.service.consultaCEP(cep)
        return result
        
    except (zeep.exceptions.Fault, zeep.exceptions.Error) as e:
        return e.message
 
def calculoFrete(servico, cepOrigem, cepDestino):
    try: 
        client = Client('http://ws.correios.com.br/calculador/CalcPrecoPrazo.asmx?WSDL')
        
        #criarcodificação
        #result = client.service.consultaCEP(cep)
        #return result
        
    except (zeep.exceptions.Fault, zeep.exceptions.Error) as e:
        return e.message