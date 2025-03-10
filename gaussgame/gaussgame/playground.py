import datetime
from tapgame.helpers import to_iso8601

now = datetime.datetime.now(datetime.UTC)
dt = to_iso8601(now)
print(dt)