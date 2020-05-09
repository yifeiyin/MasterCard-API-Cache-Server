
from mastercardmerchantidentifier import MerchantIds as MCMerchantApi
import mastercardapicore as MCApiCore

import bottle

app = bottle.default_app()
app.config.update({
    'autojson': True,
    'sqlite.db': './db_data',
})


# http://bottlepy.org/docs/dev/

@app.route('/get/<query>')
def index(query):
    response = {'a': 1}
    return {'query': query, 'response': response}


# app.run(host='localhost', port=8080)

def initializeMC():
    consumerKey = "u0RH-yXcgmL5KByfqEPvY2-Ytfg_jmcXxoM7BVKRda8fb9e0!fd5e62a074754d35897c9ea777e49c2e0000000000000000"
    keyStorePath = "./prod_key3-production.p12"
    keyAlias = "prod_key3"
    keyPassword = "keystorepassword!"

    # consumerKey = "your consumer key"
    # keyStorePath = "path to your .p12 private key file"
    # keyAlias = "keyalias"
    # keyPassword = "keystorepassword"

    auth = MCApiCore.OAuthAuthentication(
        consumerKey, keyStorePath, keyAlias, keyPassword)
    MCApiCore.Config.setAuthentication(auth)
    MCApiCore.Config.setDebug(False)
    MCApiCore.Config.setSandbox(False)


def QueryMCMerchant(id):
    try:
        mapObj = MCApiCore.RequestMap()
        mapObj.set("merchant_id", "DOLIUMPTYLTDWELSHPOOLWA")
        mapObj.set("type", "FuzzyMatch")
        response = MCMerchantApi.query(mapObj)
    except MCApiCore.APIException as e:
        status = e.getHttpStatus()
        message = e.getMessage()
        reason_code = e.getReasonCode()
        err("Source: %s", e.getSource()


def main():

    try:
        mapObj = MCApiCore.RequestMap()
        mapObj.set("merchant_id", "DOLIUMPTYLTDWELSHPOOLWA")
        mapObj.set("type", "FuzzyMatch")
        response = MCMerchantApi.query(mapObj)
        print(response)
        # out(response, "message")  # -->1 merchants found.
#         # -->UNIT 2 248 WELSHPOOL RD
#         out(response, "returnedMerchants[0].address.line1")
#         out(response, "returnedMerchants[0].address.city")  # -->WELSHPOOL
#         out(response, "returnedMerchants[0].address.postalCode")  # -->6106
#         # -->WA
#         out(response, "returnedMerchants[0].address.countrySubdivision.code")
#         # -->AUSTRALIA
#         out(response, "returnedMerchants[0].address.country.name")
#         out(response, "returnedMerchants[0].address.country.code")  # -->AUS
#         out(response, "returnedMerchants[0].phoneNumber")  # -->893582575
#         # -->5533 - AUTOMOTIVE PARTS ACCESSORIES STORES
#         out(response, "returnedMerchants[0].merchantCategory")
#         # -->DOLIUM PTY LTD
#         out(response, "returnedMerchants[0].merchantDbaName")
#         # -->DOLIUMPTYLTDWELSHPOOLWA
#         out(response, "returnedMerchants[0].descriptorText")
#         out(response, "returnedMerchants[0].comment")  # -->100
#         out(response, "returnedMerchants[0].locationId")  # -->288560095
#         out(response, "returnedMerchants[0].matchConfidenceScore")  # -->100
#         # This sample shows looping through returnedMerchants
#         print("This sample shows looping through returnedMerchants")
#         for item in response.get("returnedMerchants"):
#             out(item, "address")
#             out(item, "phoneNumber")
#             out(item, "merchantCategory")
#             out(item, "merchantDbaName")
#             out(item, "descriptorText")
#             out(item, "comment")
#             out(item, "locationId")
#             out(item, "matchConfidenceScore")

    except MCApiCore.APIException as e:
        err("HttpStatus: %s", e.getHttpStatus())
        err("Message: %s", e.getMessage())
        err("ReasonCode: %s", e.getReasonCode())
        err("Source: %s", e.getSource())


# def out(response, key):
#     print("%s--> %s" % (key, response.get(key)))


# def err(message, value):
#     print(message % (value))


# def errObj(response, key):
#     print("%s--> %s" % (key, response.get(key)))


if __name__ == "__main__":
    main()
