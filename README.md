# nowlistening-mastodon

Bateu nostalgia dos tempos de MSN Messenger e seu recurso _Now Listening_? Adicione a música em reprodução no seu Last.fm nos metadados do seu perfil no Mastodon. 😀

![Perfil no Mastodon com um dos campos mostrando a música sendo reproduzida no momento](https://cdn.masto.host/ursalzone/media_attachments/files/111/723/697/028/390/046/original/578023da15af4d51.png)

Tenho a intenção de transformar isso num sistema web que possa ser usado por outras pessoas, em que seja possível ao usuário autorizar o meu app a modificar os metadados de seu perfil, mas no momento é apenas um teste de como obter a música em reprodução via Last.fm e de como modificar um perfil de usuário no Mastodon.

## Como usar esse script

O script `update.py` precisa acessar as seguintes variáveis de ambiente:

* `LAST_API_KEY`: API Key de uma [aplicação no Last.fm](https://www.last.fm/api)
* `LAST_USER`: seu usuário no Last.fm
* `MAST_ACC_TOKEN`: um _access token_ de um [app no Mastodon](https://docs.joinmastodon.org/client/token/)
* `INSTANCE_URL`: a URL da instância em que o app foi criado

Ao executar `update.py` uma única vez, ele usará a API do Last.fm para determinar se o usuário está reproduzindo uma música no momento. Se estiver, adiciona ou atualiza um metadado `Ouvindo agora 🔊` na conta do usuário com o token em `MAST_ACC_TOKEN`.

Para manter `Ouvindo agora 🔊` atualizado conforme você escuta um álbum ou playlist, execute `update.py` periodicamente (usando, por exemplo, um agendador como o `cron`).

## To Do

Para virar um serviço web que o usuário possa simplesmente autorizar a atualizar sua conta falta... quase tudo. 😅

- [x] testar uso da API do Last.fm e do Mastodon
- [ ] implementar fluxo OAuth para autorização num app
- [ ] definir como e onde armazenar os tokens e logins (do Last.fm) de usuários
- [ ] implementar a criação de apps Mastodon nas instâncias
- [ ] definir como e onde armazenar as informações sobre apps.
