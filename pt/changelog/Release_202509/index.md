# Changelog – Release 2025.09  

Com o Release 2025.09, digna introduz uma nova **arquitetura modular** e lança **cinco módulos especializados** para Qualidade de Dados e Observabilidade.  
Esta versão também reforça a autenticação e melhora o tratamento de notificações em toda a plataforma.  

---

## Novos Recursos  

### Design Modular  
- digna agora segue uma **arquitetura modular**.  
- Clientes podem ativar apenas os módulos que precisam e adicionar mais conforme as necessidades crescem.  
- Funcionalidade anterior agora faz parte do **digna Data Anomalies**.  

### Novos Módulos  
- **digna Data Anomalies** – Detecção por IA de anomalias em volumes de dados, distribuições e valores ausentes.  
- **digna Data Analytics** – Avaliação de séries temporais de métricas de observabilidade para detectar tendências de longo prazo e volatilidade.  
- **digna Data Timeliness** – Monitoramento dos tempos esperados de chegada de dados, tanto baseado em IA quanto baseado em regras.  
- **digna Data Validation** – Verificações em nível de registro baseadas em regras para garantir conformidade com regras de negócio.  
- **digna Data Schema Tracker** – Detecção de alterações de esquema (modificações DDL) em bancos de dados monitorados.  

### MFA via OIDC  
- Suporte para **Autenticação Multifator (MFA)** com Single Sign-On via OIDC.  
- Fornece segurança de nível empresarial para todos os logins de usuários.  

### E-mails de Notificação por Módulo  
- As notificações agora são enviadas **por módulo**, facilitando separar alertas de Data Anomalies, Data Analytics e outros módulos.  

---

## Atualizações do CLI  

- **Novo comando: `inspect-cancel`** – Cancela inspeções por ID de requisição ou termina todas as requisições ativas.  
- **Novo comando: `check-config`** – Valida arquivos de configuração antes da inicialização.  
- **Novo comando: `remove-orphans`** – Limpa entradas de repositório órfãs.  
- **Comando `inspect` aprimorado** – Nova opção `--bypass-backend` (`-bb`) e códigos de retorno padronizados (`0 = OK, 1 = INFO, 2 = WARNING`).  


## Documentação  
- Novos guias:  
  - Guia de Integração Single Sign-On