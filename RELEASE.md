# Como Criar uma Release

Este documento explica como criar uma nova release do Gerador de Fichas que automaticamente gerará o executável e o disponibilizará para download.

## Pré-requisitos

- Ter permissões de escrita no repositório
- Git instalado localmente
- Ter o código pronto para release

## Processo de Release

### 1. Prepare o código

Certifique-se de que todas as alterações desejadas estão commitadas e pusheadas para o branch `main`:

```bash
git add .
git commit -m "Mensagem descrevendo as mudanças"
git push origin main
```

### 2. Crie e envie uma tag de versão

As releases são acionadas automaticamente quando você cria uma tag seguindo o padrão semântico `v*.*.*` (exemplo: `v3.1.0`, `v3.2.0`, etc.):

```bash
# Crie a tag localmente (exemplo para versão 3.2.0)
git tag v3.2.0

# Envie a tag para o GitHub
git push origin v3.2.0
```

### 3. Acompanhe o processo de build

1. Acesse a aba [Actions](https://github.com/mauricio-luan/gerador-fichas-3.0/actions) do repositório
2. Você verá um workflow "Build and Release" em execução
3. O processo leva alguns minutos para:
   - Configurar o ambiente Windows
   - Instalar Python e dependências
   - Compilar o executável com PyInstaller
   - Criar o arquivo .zip com todos os arquivos necessários
   - Criar a release no GitHub

### 4. Verifique a release

Após a conclusão do workflow:

1. Acesse a aba [Releases](https://github.com/mauricio-luan/gerador-fichas-3.0/releases)
2. Você verá a nova release com:
   - O arquivo `.zip` contendo o executável e arquivos de configuração
   - Notas de release automáticas com instruções de uso
   - Data e informações sobre a versão

## Versionamento Semântico

Recomenda-se seguir o [versionamento semântico](https://semver.org/lang/pt-BR/):

- **MAJOR** (X.0.0): Mudanças incompatíveis na API
- **MINOR** (3.X.0): Novas funcionalidades mantendo compatibilidade
- **PATCH** (3.1.X): Correções de bugs mantendo compatibilidade

Exemplos:
- `v3.1.0` → `v3.2.0`: Nova funcionalidade adicionada
- `v3.1.0` → `v3.1.1`: Correção de bug
- `v3.1.0` → `v4.0.0`: Mudança que quebra compatibilidade

## Solução de Problemas

### A release não foi criada automaticamente

- Verifique se a tag segue o padrão `v*.*.*` (com o "v" no início)
- Confirme que a tag foi enviada para o GitHub com `git push origin <tag>`
- Verifique os logs na aba Actions para ver se houve algum erro

### O build falhou

- Acesse a aba Actions e clique no workflow com falha
- Verifique os logs de erro
- Problemas comuns:
  - Dependências faltando no `requirements.txt`
  - Erros no código Python
  - Problemas na especificação do PyInstaller (`main.spec`)

### Como deletar uma release/tag com erro

```bash
# Deletar tag localmente
git tag -d v3.2.0

# Deletar tag remotamente
git push origin :refs/tags/v3.2.0

# Depois delete a release manualmente na interface do GitHub
```

## Automatização

O workflow está configurado em `.github/workflows/release.yml` e é acionado automaticamente quando:
- Uma tag no formato `v*.*.*` é enviada para o GitHub

Não é necessário executar nenhum comando manual para build ou criação da release após enviar a tag.
