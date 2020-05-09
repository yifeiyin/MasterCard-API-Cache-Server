from mastercardmerchantidentifier import MerchantIds as MCMerchantApi
import mastercardapicore as MCApiCore

import bottle
from bottle.ext import sqlite

import json

from config import Config

# http://bottlepy.org/docs/dev/
# https://developer.mastercard.com/documentation/merchant-identifier

# https://github.com/greggles/mcc-codes
# https://github.com/jleclanche/python-iso18245


app = bottle.Bottle()
app.config.update({
    'autojson': True,
})

plugin = sqlite.Plugin(dbfile=Config['db_file'])
app.install(plugin)


# Initialize MC
consumerKey = Config['consumerKey']
keyStorePath = Config['keyStorePath']
keyAlias = Config['keyAlias']
keyPassword = Config['keyPassword']
debug = Config['debug']
sandbox = Config['sandbox']

auth = MCApiCore.OAuthAuthentication(
    consumerKey, keyStorePath, keyAlias, keyPassword)
MCApiCore.Config.setAuthentication(auth)
MCApiCore.Config.setDebug(debug)
MCApiCore.Config.setSandbox(sandbox)


@app.route('/get/<query>')
def index(query, db):
    db.execute("CREATE TABLE IF NOT EXISTS main_table("
               "id INTEGER PRIMARY KEY AUTOINCREMENT,"
               "req STRING,"
               "res STRING,"
               "count INTEGER DEFAULT 1,"
               "created_at DATETIME DEFAULT (datetime('now'))"
               ");")
    db.execute("CREATE TABLE IF NOT EXISTS request_log("
               "id INTEGER PRIMARY KEY AUTOINCREMENT,"
               "req STRING,"
               "ip  STRING,"
               "res STRING,"
               "created_at DATETIME DEFAULT (datetime('now'))"
               ");")

    final_response = ''

    row = db.execute(
        'SELECT id, res FROM main_table where req = ?', (query,)
    ).fetchone()

    if row:
        print('Found existing data')
        final_response = json.loads(row['res'])
        db.execute(
            'UPDATE main_table SET count = count + 1 where id=?',
            (row['id'],)
        )
        logRequest(db, query, 'cached')

    else:
        print('Fetching from API')
        try:
            res = QueryMCMerchant(query)

        except RuntimeError as e:
            bottle.response.status = 400
            bottle.response.content_type = 'application/json'
            final_response = json.dumps(e.args[0], ensure_ascii=False)
            logRequest(db, query, final_response)

        else:
            final_response = res
            res = json.dumps(res, ensure_ascii=False)
            db.execute(
                'INSERT INTO main_table (req, res) VALUES (?, ?)',
                (query, res))
            logRequest(db, query, 'saved')

    return final_response


def logRequest(db, query, response_content):
    ip = bottle.request.get('REMOTE_ADDR')
    db.execute('INSERT INTO request_log(req, ip, res) VALUES (?,?,?)',
               (query, ip, response_content))


def QueryMCMerchant(id):
    try:
        request_map = MCApiCore.RequestMap()
        request_map.set("merchant_id", id)
        request_map.set("type", "ExactMatch")
        response = MCMerchantApi.query(request_map)
        merchants = response.get('returnedMerchants')

        raw = response.getObject()
        print('Raw response: ' + json.dumps(raw, ensure_ascii=False))

        match = None
        if merchants is not None and len(merchants) == 1:
            match = merchants[0]

        return {'match': match, 'raw': raw}

    except MCApiCore.APIException as e:
        status = e.getHttpStatus()
        message = e.getMessage()
        reason_code = e.getReasonCode()
        source = e.getSource()
        error = {'status': status, 'message': message,
                 'reason_code': reason_code, 'source': source}
        print('Error: ' + str(error))

        if reason_code in ['MISSING_REQUIRED_INPUT', 'INVALID_INPUT_VALUE', 'DESCRIPTOR_TOO_SMALL', 'TOO_MANY_MATCHES']:
            return {'error': reason_code, 'raw': error}
        else:
            raise RuntimeError(error)
        # reason_code:
        # MISSING_REQUIRED_INPUT
        # INVALID_INPUT_VALUE
        # DESCRIPTOR_TOO_SMALL
        # TOO_MANY_MATCHES
        # SERVICE_ERROR
        # VOLUME_THRESHOLD_EXCEEDED


def main():
    app.run(host='localhost', port=8080)

    # QueryMCMerchant('BEST BUY #123')
    # QueryMCMerchant('SKIPTHEDISHES Winnipeg MB')


if __name__ == "__main__":
    main()
