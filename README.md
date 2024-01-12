# nowlistening-mastodon

Bateu nostalgia dos tempos de MSN Messenger e seu recurso _Now Listening_? Adicione a música em reprodução no seu Last.fm nos metadados do seu perfil no Mastodon. 😀

![Perfil no Mastodon com um dos campos mostrando a música sendo reproduzida no momento](https://cdn.masto.host/ursalzone/media_attachments/files/111/723/697/028/390/046/original/578023da15af4d51.png)

Tenho a intenção de transformar isso num sistema web que possa ser usado por outras pessoas, em que seja possível ao usuário autorizar o meu app a modificar os metadados de seu perfil, mas no momento é apenas um teste de como obter a música em reprodução via Last.fm e de como modificar um perfil de usuário no Mastodon.

## Como usar esse script

O script `update.py` precisa acessar as seguintes variáveis de ambiente:

- `LAST_API_KEY`: API Key de uma [aplicação no Last.fm](https://www.last.fm/api)
- `LAST_USER`: seu usuário no Last.fm
- `MAST_ACC_TOKEN`: um _access token_ de um [app no Mastodon](https://docs.joinmastodon.org/client/token/).
    - Gere seu token preenchendo o campo 3 [neste link](https://token.bolha.one/?client_name=Mastodon%20Now%20Playing&scopes=read:accounts%20write:accounts).
- `INSTANCE_URL`: a URL da instância em que o app foi criado

Ao executar `update.py` uma única vez, ele usará a API do Last.fm para determinar se o usuário está reproduzindo uma música no momento. Se estiver, adiciona ou atualiza um metadado `Ouvindo agora 🔊` na conta do usuário com o token em `MAST_ACC_TOKEN`.

Para manter `Ouvindo agora 🔊` atualizado conforme você escuta um álbum ou playlist, execute `update.py` periodicamente (usando, por exemplo, um agendador como o `cron`).

> Caso sua instância seja modificada e suporte mais de 4 campos na bio do perfil, o script não irá funcionar pra você (por limitação do `mastodon.py`).

## Execução automática

Para manter o script rodando a cada dois minutos para saber se você está ouvindo música, use um `systemd-timer`.

Primeiro, salve o seguinte código em `/etc/systemd/system/mastofm.service`:

``` ini
[Unit]
Description=Mastodon Now Playing
After=network-online.target
Wants=mastofm.timer

[Service]
Type=simple
Environment="PYTHONUNBUFFERED=1"
Environment="LAST_API_KEY=<insira_aqui>"
Environment="LAST_USER=<insira_aqui>"
Environment="MAST_ACC_TOKEN=<insira_aqui>"
Environment="INSTANCE_URL=<insira_aqui>"
DynamicUser=yes
Restart=always
RestartSec=1 
WorkingDirectory=/opt/mastofm
ExecStart=/usr/bin/python3 /opt/mastofm/update.py
KillSignal=SIGINT

[Install]
WantedBy=multi-user.target
```

Agora, salve o seguinte código em `/etc/systemd/system/mastofm.timer`:

``` ini
[Unit]
Description=Timer do Mastodon Now Playing

[Timer]
Unit=mastofm.service
OnCalendar=*:0/2
Persistent=true
AccuracySec=1us

[Install]
WantedBy=timers.target
```

Por fim, faça o _timer_ ser executado e passe a iniciar com o sistema:

``` bash
systemctl daemon-reload
systemctl enable --now mastofm.timer
```

O _timer_ será executado a cada dois minutos e, se você estiver ouvindo alguma coisa, o nome da música aparecerá em seu perfil. Lembre de alterar `/opt/mastofm/` pelo caminho da pasta onde o arquivo `update.py` está.

## Usando com o Docker

Gere uma imagem Docker com o arquivo `Dockerfile` e suba o script após editar o arquivo `docker-compose.yml`, ambos adicionados ao repositório. Para que a imagem do contêiner Docker seja gerada, execute o seguinte comando:

``` bash
docker build -t mastofm:latest .
```

Depois de editar o arquivo `docker-compose.yml`, suba o contêiner com o comando: `docker-compose up -d`.

## To Do

Para virar um serviço web que o usuário possa simplesmente autorizar a atualizar sua conta falta... quase tudo. 😅

- [x] testar uso da API do Last.fm e do Mastodon
- [ ] implementar fluxo OAuth para autorização num app
- [ ] definir como e onde armazenar os tokens e logins (do Last.fm) de usuários
- [ ] implementar a criação de apps Mastodon nas instâncias
- [ ] definir como e onde armazenar as informações sobre apps.
