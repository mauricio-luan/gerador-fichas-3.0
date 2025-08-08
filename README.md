# Gerador de Fichas de Implantação 3.0

Sistema automatizado para geração de fichas de implantação a partir de dados do TomTicket.

## Descrição

Este projeto automatiza a criação de fichas de implantação em Excel, extraindo informações de clientes e chamados através da API do TomTicket. O sistema gera planilhas estilizadas com dados organizados e tokens para terminais.

## Funcionalidades

- Consulta automática de dados via API TomTicket
- Geração de planilhas Excel estilizadas
- Criação automática de tokens para terminais
- Organização automática de arquivos por cliente
- Interface com logo personalizada

## Pré-requisitos

- Python 3.7+
- Acesso à API do TomTicket
- Token de autenticação válido

## Instalação

1. **Clone o repositório:**

```bash
git clone https://github.com/mauricioluanss/gerador-fichas-3.0.git
cd gerador-fichas-3.0
```

2. **Instale as dependências:**

```bash
pip install -r requirements.txt
```

3. **Configure as variáveis de ambiente:**

```bash
# Copie o arquivo de exemplo
cp env.example .env

# Edite o arquivo .env com suas credenciais
```

## Configuração

### Arquivo .env

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```env
# Configurações da API TomTicket
API_URL=https://api.tomticket.com/v2.0/customer/details?customer_id=
API_TICKET_URL=https://api.tomticket.com/v2.0/ticket/detail?ticket_id=
API_TOKEN=seu_token_aqui
```

### Como obter o Token

1. Acesse o painel do TomTicket
2. Vá em Configurações > API
3. Gere um novo token de acesso
4. Copie o token para o arquivo `.env`

## Como usar

Código fonte

Para executar diretamente o código Python:

```bash
python src/main.py
```

### Fluxo de uso

1. Execute o programa
2. Digite o ID do chamado quando solicitado
3. Informe o número de terminais necessários
4. Aguarde a geração automática da planilha
5. A pasta será aberta automaticamente com o arquivo gerado

## Estrutura de arquivos

```
ficha-3.0/
├── src/
│   ├── main.py              # Arquivo principal
│   ├── gera_planilha.py     # Geração de planilhas
│   └── encontra_imagem.py   # Localização de imagens
├── .env                     # Configurações (não commitado)
├── requirements.txt        # Dependências Python

config_log.py   # arquivo configuração de logs
app.log         # arquivo de logs gerados
```

## Dados extraídos

O sistema extrai automaticamente:

**Dados do cliente:**

- Nome Fantasia
- Razão Social
- CNPJ
- Endereço completo
- Contato comercial
- Telefone
- E-mail

**Dados do chamado:**

- Número do protocolo
- Data de criação

**Tokens gerados:**

- Tokens únicos para cada terminal

## Saída

- Arquivo Excel estilizado com logo
- Organização automática por cliente
- Tokens formatados para uso nos terminais
- Dados organizados em planilha profissional

## Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## Autor

**Mauricio Luan** - 2025
