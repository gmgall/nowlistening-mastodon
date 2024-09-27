import os, pylast, logging, schedule, time, sys
from pprint import pprint
from mastodon import Mastodon
from dotenv import load_dotenv
load_dotenv()

# Configurações de log
logging.basicConfig(
        format="[%(asctime)s] [%(levelname)s] %(message)s",
        datefmt="%d/%m/%Y %H:%M:%S",
        level=logging.ERROR
    )

# Configurações de integração
LAST_API_KEY   = os.getenv("LAST_API_KEY")
MAST_ACC_TOKEN = os.getenv("MAST_ACC_TOKEN")
INSTANCE_URL   = os.getenv("INSTANCE_URL")

# Verifica o que está sendo ouvido
def now_listening_str():
    network = pylast.LastFMNetwork(api_key=LAST_API_KEY)
    user = pylast.User(os.getenv("LAST_USER"), network)
    now_playing = user.get_now_playing()
    if not now_playing: return None
    track_name = now_playing.get_title()
    artist_name = now_playing.get_artist().get_name()
    return track_name + ' • ' + artist_name

# Inclui o que está sendo ouvido nos campos extras
def update_fields():
    mastodon = Mastodon(access_token=MAST_ACC_TOKEN, api_base_url=INSTANCE_URL)
    profile_fields = mastodon.account_verify_credentials()['source']['fields']
    has_now_listening_field = False
    for row in profile_fields:
        del row['verified_at']
        if row['name'] == 'Ouvindo agora':
            has_now_listening_field = True
            row['value'] = now_listening_str()

    if not has_now_listening_field:
        profile_fields.append({ 'name': 'Ouvindo agora', 'value': now_listening_str()})
    new_profile_fields = [row for row in profile_fields if row['value'] is not None]
    new_profile_tuples = [tuple(row.values()) for row in new_profile_fields]
    result = mastodon.account_update_credentials(fields = new_profile_tuples)
    return result

# Classe que oculta o output de prints subordinados a ela
class HiddenPrints:
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout

# Trabalho que executa o código principal do bot
def run():
    logging.info(now_listening_str())
    with HiddenPrints():
        pprint(update_fields())

# Informa que a execução está operacional
logging.info("O bot está em funcionamento.\n")
# Executa os trabalhos no início da execução, antes dos agendamentos
run()

# Agenda a execução do trabalho acima
schedule.every(2).minutes.do(run)

# Loop para verificar agendamentos e executá-los
while True:
    logging.info("Verificando agendamentos")
    schedule.run_pending()
    time.sleep(60)