# MastoFM: Mastodon + LastFM

Bateu nostalgia dos tempos de MSN Messenger e seu recurso _ouvindo agora_? Adicione a música em reprodução do seu LastFM nos metadados do seu perfil no Mastodon.

![Perfil no Mastodon com um dos campos mostrando a música sendo reproduzida no momento](https://pub.bolha.one/mastodon/img/perfil.png)

## Como usar esse script

Baixe um arquivo ZIP com o conteúdo deste repositório ou clone-o e instale as dependências:

``` bash
git clone https://code.bolha.one/bolha/mastofm.git
apt update
apt install python3 python3-pip

cd mastofm
pip3 install -r requirements.txt
```

Agora vamos configurar o funcionamento do arquivo `update.py`, que precisa acessar as seguintes variáveis de ambiente:

- `LAST_API_KEY`: API Key de uma [aplicação no LastFM](https://www.last.fm/api)
- `LAST_USER`: seu usuário no LastFM
- `MAST_ACC_TOKEN`: um token de acesso de um [app no Mastodon](https://docs.joinmastodon.org/client/token/).
- `INSTANCE_URL`: a URL da instância em que o app foi criado

> Gere seu token de acesso facilmente preenchendo o campo 3 [neste link](https://token.bolha.one/?client_name=MastoFM&scopes=read:accounts%20write:accounts).

Salve as variáveis de ambiente acima em um arquivo `.env` na mesma pasta do MastoFM.

Ao executar `update.py` uma única vez, ele usará a API do LastFM para determinar se o usuário está reproduzindo uma música no momento. Se estiver, adiciona ou atualiza um metadado `Ouvindo agora 🔊` na conta do usuário do Mastodon usando o token de acesso.

> Caso sua instância seja modificada e suporte mais de 4 campos extras na bio do perfil, o script não irá funcionar pra você (por limitação do `mastodon.py`). Será necessário deixar no máximo três campos preenchidos para o quarto campo ser usado pelo MastoFM.

Para manter `Ouvindo agora 🔊` atualizado conforme você escuta um álbum ou playlist, execute `update.py` periodicamente (usando, por exemplo, um agendador como o `cron`) ou usar a imagem Docker.

## Execução automática

Para manter o script rodando a cada dois minutos para saber se você está ouvindo música, use um `systemd-timer`. Caso use a imagem Docker, isto não é necessário.

Primeiro, salve o seguinte código em `/etc/systemd/system/mastofm.service`:

``` ini
[Unit]
Description=MastoFM
After=network-online.target
Wants=mastofm.timer

[Service]
Type=simple
Environment="PYTHONUNBUFFERED=1"
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
Description=Timer do MastoFM

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

O _timer_ rodará a cada dois minutos e, se você estiver ouvindo alguma coisa, o nome da música aparecerá em seu perfil. Lembre de alterar `/opt/mastofm/` pelo caminho da pasta onde o arquivo `update.py` está.

## Usando com o Docker

Você pode dispensar serviços do `systemd` e dockerizar a execução do bot. Para isso, use a imagem `mastofm:latest` de nosso repositório.

``` bash
docker run -d                               \
    -e PYTHONUNBUFFERED=true                \
    -e LAST_API_KEY=ABCDXYZ                 \
    -e LAST_USER=johnsnow                   \
    -e MAST_ACC_TOKEN=ABCDXYZ               \
    -e INSTANCE_URL=https://botsin.space    \
    -e TZ=America/Recife                    \
    --name mastofm                          \
    --restart unless-stopped                \
    code.bolha.one/bolha/mastofm:latest
```

Informe as variáveis de ambiente `LAST_API_KEY`, `LAST_USER`, `MAST_ACC_TOKEN` e `INSTANCE_URL` como você faria no arquivo `.env`. Se preferir, edite e use o arquivo `docker-compose.yml` com o Portainer Stacks ou o `docker-compose up -d`.

## Créditos

Este repositório é baseado no [Mastodon Now Listening](https://github.com/gmgall/nowlistening-mastodon), de [Guilherme Gall](https://ursal.zone/@gmgall). Aqui basicamente pegamos o código dele e fizemos as adaptações para incluí-lo num contêiner Docker ou `systemd-timer`.

No futuro, o autor original transformará o script num web app para facilitar a instalação e uso.

Este programa está licenciado sob a `MIT`.
