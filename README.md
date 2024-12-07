<h1 align="center" width="100%"> Backend Web com FastAPI para gestão de doações para causas solidárias com criptoativos da Ethereum </h1>

<p align="center" width="90%">

<img src="https://github.com/user-attachments/assets/53aaff0b-de99-40b5-a1da-1a88e3a7af2e" alt="" width="65%">
  
</p>

<h3 align="center" width="60%"> Python + FastAPI + PostgreSQL</h3>

<p align="center" width="50%">

<img src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54" alt="python"/>
<img src="https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi" alt="fastapi"/>
<img src="https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white" alt="postgres"/>

</p>

<h1 align="center" width="100%"> Descrição </h1>

<p>
  O seguinte projeto backend realiza a gestão de doações em criptoativos para causas solidárias e humanitárias, neste caso, as doações são feitas em ETH, criptomoeda da rede blockchain Ethereum, conhecida pelo suporte aos contratos inteligentes e pela criptografia de curva elíptica, e os valores doados são convertidos em dólar americano. Como regras de negócio, ficou estabelecido que a exclusão de uma causa só pode ser realizada após ter recebido um valor em doação, por mínimo que seja e esse montante doado tenha sido utilizado para a sua proposta de fato, ou seja, o status do montante foi atualizado de "stored" para "applied" (armazenado para aplicado) e claramente essa atualização só pode acontecer após ter ocorrido pelo menos uma doação para esta causa e mais doações só podem ser realizadas a uma causa se esta ainda não tiver aplicado seu montante recebido. Cada causa possui um código de certificação que valida sua veracidade e cada valor em ETH é simbólico (décimos ou centésimos que representam muitas vezes cumprimento de contratos inteligentes ou apenas um gas fee desse tipo de tecnologia de sistema distribuído) e quando convertidos para o dólar representam valores consideráveis. Como exemplo, usei uma causa solidária que ajuda vítimas humanas e outros animais de desastres ambientais e incêndios florestais.
</p>

<h1 align="center" width="100%"> Como criar o projeto na sua máquina? </h1>

<p> Abra o terminal e digite :
  
  ```bash
  mkdir fastapi_project
 ```
  ```bash
  cd fastapi_project
 ```

Crie e ative o ambiente virtual :
  ```bash
  python -m venv venv
 ```
Para Windows : 
  ```bash
  venv\Scripts\activate
 ```

Para Linux/macOS : 
  ```bash
  source venv/bin/activate
 ```

Instale o framework FastAPI e o servidor Uvicorn :
  ```bash
  pip install fastapi uvicorn
 ```

Abra o Visual Studio Code :
  ```bash
  code .
 ```

Crie um arquivo main.py dentro do diretório app que possua o arquivo __init__.py, escreva o código e execute o servidor com : 
  ```bash
  uvicorn main:app --reload
 ```
Você pode criar o arquivo __init__.py com o seguinte comando no terminal:

  ```bash
  touch project/package/__init__.py
 ```
Trocando "project" e "package" pelos respectivos nomes de seus diretórios.

Ou se preferir, apenas faça o git clone deste projeto :

  ```bash
  git@github.com:Doug16Yanc/fastapi_project.git
 ```
Utilize o PostgreSQL como banco de dados e coloque suas credenciais de uso.
<h1 align="center" width="100%"> Rotas no Postman </h1>

<p>Link das coleções no Postman:
https://www.postman.com/winter-capsule-897611/workspace/python-backend/collection/28494279-d6b7875d-1255-4cce-b809-d82f5c581756?action=share&creator=28494279</p>

<h2 align="center" width="50%"> CAUSES </h2>

<p> POST /causes </p>

Cria uma causa.

Response (Se não já houver uma causa com mesmo ID) :

 ```bash
{
   "status" : "Success",
   "message" : "Cause created successfully.",
   "data" : {
        "cause_id" : 1,
        "cause_name" : "Man Against Fire",
        "description" : "Assist human and other animal victims of environmental disasters and forest fires.",
        "certification_code" : "0x563373",
        "amount" : 0.0,
        "status_amount" : "stored"
    }
}
 ```
<p> GET /causes/{cause_id} </p>

Encontra uma causa por ID.

Response (se encontrado)

 ```bash
{
   "status" : "Success",
   "message" : "Cause processed successfully.",
   "data" : {
        "cause_id" : 1,
        "cause_name" : "Man Against Fire",
        "description" : "Assist human and other animal victims of environmental disasters and forest fires.",
        "certification_code" : "0x563373",
        "amount" : 0.0,
        "status_amount" : "stored"
    }
}
```

<p> GET /causes </p>

Retorna uma lista das causas.

Response (Se a lista não estiver vazia)

```bash
{
   "status" : "Success",
   "message" : "Causes processed successfully.",
   "data" : {
        "cause_id" : 1,
        "cause_name" : "Man Against Fire",
        "description" : "Assist human and other animal victims of environmental disasters and forest fires.",
        "certification_code" : "0x563373",
        "amount" : 0.0,
        "status_amount" : "stored"
    }
}
```                                                                                                                                                 
<p> PUT /causes/{cause_id} </p>

Atualiza apenas o status de uma causa encontrada pelo id e se esta tiver um montante acima de 0.0 (regra de negócio estabelecida).

Response (Conforme regras de negócio acima)

```bash
{
   "status" : "Success",
   "message" : "Status updated successfully.",
   "data" : {
        "cause_id" : 1,
        "cause_name" : "Man Against Fire",
        "description" : "Assist human and other animal victims of environmental disasters and forest fires.",
        "certification_code" : "0x563373",
        "amount" : 183.2015,
        "status_amount" : "applied"
    }
}
```       
<p> DELETE /causes/{cause_id} </p>

Deleta uma causa pelo ID se esta tiver aplicado o montante recebido em doações na sua proposta.

Response (Conforme regra de negócio acima)

```bash
{
   "status" : "Success",
   "message" : "Cause deleted successfully.",
   "data" : {
        "cause_id" : 1,
        "cause_name" : "Man Against Fire",
        "description" : "Assist human and other animal victims of environmental disasters and forest fires.",
        "certification_code" : "0x563373",
        "amount" : 183.2015,
        "status_amount" : "applied"
    }
}
```

<h2 align="center" width="50%"> DONATIONS </h2>
  
<p> POST /donations </p>  

Realiza uma doação em ETH para uma causa existente e válida se o montante daquela causa ainda não tiver sido aplicado.

Response:

```bash
{
    "status": "Success",
    "message": "Donation created successfully!",
    "data": {
        "donation": {
            "donation_id": 1,
            "address_account": "0x648485",
            "cause_id": 1,
            "value": 0.05
        },
        "transaction_hash": "qzou2vsv17bdd93h6fh1639ohwz7k8ys21f6qe6n5mpsffz4v6dldwkj4kerxdv2"
    }
}
```
<p> GET /donations/{donation_id} </p>

Encontra uma doação pelo ID.

Response (Se encontrada):
```bash
{
    "status": "Success",
    "message": "Donation processed successfully!",
    "data": {
        "donation": {
            "donation_id": 1,
            "address_account": "0x648485",
            "cause_id": 1,
            "value": 0.05
        },
    }
}
```
<p> GET /donations </p>

Lista as doações criadas.

Response (Se a lista não estiver vazia):

```bash
{
    "status": "Success",
    "message": "Donations processed successfully!",
    "data": {
        "donation": {
            "donation_id": 1,
            "address_account": "0x648485",
            "cause_id": 1,
            "value": 0.05
        },
    }
}
```
<p> DELETE /donations/{donation_id} </p>

Deleta uma doação por ID, avisando sobre a manutenção da transação na rede Ethereum.

Response (Se encontrada):

```bash
{
    "status": "Success",
    "message": "Donation deleted successfully, but the value of the transactions remains in Ethereum.",
    "data": {
        "donation": {
            "donation_id": 1,
            "address_account": "0x648485",
            "cause_id": 1,
            "value": 0.05
        },
    }
}
```

<h1 align="center"> Autor </h1>

<p>Douglas Holanda</p>
                                                                                                                                                         

