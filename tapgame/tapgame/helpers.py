import datetime
from functools import cache
from time import sleep
import random

from loguru import logger
from sqlmodel import Session, create_engine, select

from .models.player import Player
from .models.settings import get_settings


m_adjectives = ['bublinkový', 'šikovný', 'lenivý', 'bystrý', 'chichotavý', 'srandovný', 'prskajúci', 'hrkajúci', 'lietajúci', 'hopsavý', 'vyškerený', 'okatý', 'pehatý', 'skákajúci']
m_nouns = ['slimáčik', 'veveričiak', 'krtko', 'oceánik', 'havko', 'kocúrik', 'hadík', 'tuleň', 'klokaník', 'medvedík', 'macko', 'myšiak']
f_adjectives = ['bublinková', 'šikovná', 'bystrá', 'lenivá', 'chichotavá', 'srandovná', 'prskajúca', 'hrkajúca', 'lietajúca', 'hopsavá', 'vyškerená', 'okatá', 'pehatá', 'skákajúca']
f_nouns = ['húsenica', 'dážďovka', 'veverička', 'mačička', 'medvedica', 'myška', 'sedmokrácka', 'púpava', 'konvalinka', 'slaninka']

def to_iso8601(dt=None)->str:
    if dt is None:
        dt = datetime.datetime.now(datetime.UTC)

    return f"{dt.replace(microsecond=0).isoformat()[:-6]}Z"


def countdown_timer(duration: int):
    while duration > 0:
        logger.debug(duration)
        sleep(1)
        duration -= 1

def get_player_name() -> str:
    if random.randint(1, 100) % 2 == 1:
        adj = random.choice(m_adjectives).capitalize()
        noun = random.choice(m_nouns).capitalize()
        return f'{adj} {noun}'
    else:
        adj = random.choice(f_adjectives).capitalize()
        noun = random.choice(f_nouns).capitalize()
        return f'{adj} {noun}'
    

@cache
def get_db_engine():
    return create_engine(get_settings().db_uri)


def get_top_players():
    with Session(get_db_engine()) as session:
        statement = select(Player).order_by(Player.score.desc()).limit(12)
        results = session.exec(statement).all()

    table = []
    for entry in results:
        table.append({
            "id": entry.id,
            "name": entry.name,
            "score": entry.score
        })

    return table