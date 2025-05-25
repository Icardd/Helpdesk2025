----------------- PASSO A PASSO PARA VISUALIZAÇÃO DO NOSSO PROJETO -----------------

A forma ideal de funcionamento do projeto é totalmente remota, sendo hospedado em plataformas gratuitas.  
Durante a ExpoTech 2025, o projeto foi disponibilizado por meio de um QR Code que direciona para o link:  
https://helpdesk2025.onrender.com/ (este dominio entra em descanso após 15 minutos por ser uma alternativa gratuita,
então pode ser que na primeira tentativa o site carregue um pouco)

A aplicação foi hospedada e personalizada para funcionar no site Render, e o banco de dados foi hospedado no Railway.

----------------- ALTERNATIVA LOCAL PARA UTILIZAR O PROJETO -----------------

Para executar o projeto localmente, será necessário instalar algumas dependências. Para isso, utilizamos o Terminal para rodar os comandos e o MySQL Workbench para gerenciar o banco de dados.

1. PRÉ-REQUISITOS:
   - Python instalado (versão 3.8 ou superior)
   - Um terminal (pode ser o CMD, Terminal do Linux ou até mesmo o do Visual Studio Code)
   - ATENÇÃO: Em alguns casos, a versão do sistema fornecida para alunos/usuários pode restringir a instalação de dependências. Nesses casos, será necessário utilizar uma versão com privilégios de administrador.

2. INSTALAÇÃO DAS DEPENDÊNCIAS:
   Abra o terminal e execute o comando:
   pip install -r requirements.txt

3. CONFIGURAÇÃO DO BANCO DE DADOS:
   Verifique o arquivo config.py e ajuste as configurações de host, usuário, senha e nome do banco.
   Por padrão, utilizamos:
   'mysql+pymysql://root:toor@localhost/helpdesk'
   Esse padrão é compatível com os sistemas utilizados na UNIFECAF.

4. EXECUÇÃO DA QUERY DE CRIAÇÃO DO BANCO:
   Execute o script SQL disponível no arquivo "bd-sistema de gestão de chamados.sql" utilizando o MySQL Workbench.
   Isso criará as tabelas e preencherá os dados previamente configurados.

5. EXECUÇÃO DO PROJETO:
   Agora, com tudo pronto, execute o comando abaixo no terminal:
   python run.py
   O sistema levará alguns instantes para carregar e apresentará um IP.
   Esse endereço pode ser acessado no navegador para visualizar o funcionamento do projeto.

OBSERVAÇÕES 
Para que ficasse mais intuitivo na apresentação do projeto algumas configurações foram feitas nas contas, todos os usuários criados com a palavra-chave "admin" no endereço de email fictício.
tem acesso ao modelo de "Técnico", onde estão as opções de gestão de chamados.

LOGINS INSERIDOS POR PADRÃO NO PROJETO
---permissão de usuário---
Matheus@gmail.com matheus1234
alan@gmail.com alan1234
osmar@gmail.com osmar1234
Arthur@gmail.com Arthur1234
osvaldo@gmail.com osvaldo1234
mario@gmail.com mario1234
vitor@gmail.com vitor1234
---permissão de técnico---
adminisabela@gmail.com isabela1234
admingustavo@gmail.com gustavo1234
adminigor@gmail.com igor1234
