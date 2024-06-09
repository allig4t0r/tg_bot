Most interesting files:

*tg_bot.py* — main

*handlers.py* — all the handlers

*admin.py* — some additional methods for handlers

*db.py and outline.py* — context managers for local sqlite3 db and outline server respectively

Needed env variables (no quotes for values):

  BOT_MODE=PROD  
  BOT_TOKEN_PROD  
  OUTLINE_API_URL  
  OUTLINE_CERT

For backup:

YDISK_CLIENT_ID  
YDISK_CLIENT_SECRET  
YDISK_CLIENT_TOKEN


How to run:

docker run -d \
  --name tg_bot --restart always --net host \
  --label 'com.centurylinklabs.watchtower.enable=true' \
  --env-file .env \
  --mount type=bind,source=/opt/tg_bot,target=/opt/tg_bot \
  ghcr.io/allig4t0r/tg_bot:latest