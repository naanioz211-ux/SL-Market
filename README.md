# SL Market — bilowga mashruuca

SL Market waa multi-vendor marketplace loogu talagalay Somaliland iyo Soomaaliya:
hal Telegram bot, dukaamo badan, hal suuq, iyo admin dashboard.

## Waxa hadda shaqaynaya
- FastAPI web service
- PostgreSQL (ama SQLite tijaabo maxalli ah)
- Telegram `/start`
- Diiwaangelinta aasaasiga ah ee ganacsadaha
- Liiska alaabaha suuqa
- Admin dashboard oo muujinaya tirada ganacsatada, alaabaha iyo dalabaadka
- Health endpoint: `/health`

## Waxa aan weli lagu darin
Noocani waa aasaaska MVP, mana aha system ganacsi oo dhamaystiran. Alaab-gelinta buuxda, sawirrada, cart/checkout, dalabka, maamulka dalabka, subscriptions, lacag-bixinta Zaad/eDahab, admin authentication, rate limits, migrations, iyo tests waa marxaladaha xiga. Ha qaadan lacag macaamiil ilaa qaybahaas la dhammeeyo lana tijaabiyo.

## Dejinta Railway
1. Samee repository cusub oo GitHub ah, kuna upload garee dhammaan faylasha.
2. Railway ka dooro **New Project → Deploy from GitHub Repo**.
3. Ku dar PostgreSQL service gudaha Railway.
4. App service → Variables ku dar:
   - `BOT_TOKEN`: token-ka bot-ka aad ka samaysato @BotFather
   - `DATABASE_URL`: ku xidh variable-ka PostgreSQL ee Railway (badanaa `${{Postgres.DATABASE_URL}}`); haddii loo baahdo u beddel prefix-ka `postgresql://` code-ku wuu taageeraa.
   - `ADMIN_TELEGRAM_IDS`: Telegram user ID-ga admin-ka (looma adeegsan weli qaybaha admin-ka ee aasaaskan).
   - `APP_SECRET`: samee secret dheer oo random ah.
5. Deploy. Fur domain-ka Railway; `/health` waa inuu soo celiyo `{"status":"ok","service":"sl-market"}`.

## Amniga
- Ha ku qorin BOT_TOKEN gudaha GitHub.
- Ha ku soo dirin token-ka chat ama qof kale.
- Ku kaydi Railway Variables oo keliya.
- Dashboard-ka tirakoobka hadda public ayuu yahay; ka hor isticmaalka dhabta ah waa in admin login lagu xiraa.

## Teknoolajiyada
Python, FastAPI, python-telegram-bot, SQLAlchemy, PostgreSQL, Railway.
