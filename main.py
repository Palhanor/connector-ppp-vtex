# TODO: Create a function to proccess every endpoint
# TODO: Implement all the validations
#   The required fields must exist on the request payload (doc)
#   The required fields must exist on the response payload (doc)
#   The paymentId must refer to an actual payment inside the mock_db
#   Make changes on the stored payment as the non authrization routes are called

from fastapi import Request, FastAPI

app = FastAPI()

mocked_db = [

]

def paymentId_consistency(endpoint_paymentId, body_paymentId):
    return endpoint_paymentId == body_paymentId

# TODO: Implement the class with all the required information about the payment
class Payment:
    def __init__(self, payment):
        paymentId = payment["paymentId"]
        authorizationStatus = "undefined"

@app.get("/manifest")
async def manifest():
    return {
        "paymentMethods": [
            {
                "name": "Visa",
                "allowsSplit": "onCapture"
            },
            {
                "name": "Pix",
                "allowsSplit": "disabled"
            },
            {
                "name": "MasterCard",
                "allowsSplit": "onCapture"
            },
            {
                "name": "American Express",
                "allowsSplit": "onCapture"
            },
            {
                "name": "BankInvoice",
                "allowsSplit": "onAuthorize"
            },
            {
                "name": "Privatelabels",
                "allowsSplit": "disabled"
            },
            {
                "name": "Promissories",
                "allowsSplit": "disabled"
            }
        ]
    }


@app.post("/payments")
async def payments(request: Request):
    body = await request.json()
    paymentId = body.get("paymentId", None)
    # TODO: Create a function that gets the body andd the list of required informations and returns if something is missing
    if not paymentId:
        # TODO: Format the response with 400 status
        return "The paymentId value is required"  # Status 400
    # TODO: Format the response with the 200 (?) status
    return {
        "paymentId": paymentId,
        "status": "approved",
        "authorizationId": "AUT-E4B9C36034-ASYNC",
        "paymentUrl": "https://exemplo2.vtexpayments.com.br/api/pub/fake-payment-provider/payment-redirect/611966/payments/5B127F1E0C944EF9ACE264FEC1FC0E91",
        "nsu": "NSU-171BE62CB7-ASYNC",
        "tid": "TID-20E659E8E5-ASYNC",
        "acquirer": "TestPay",
        "code": "2000-ASYNC",
        "message": None,
        "delayToAutoSettle": 21600,
        "delayToAutoSettleAfterAntifraud": 1800,
        "delayToCancel": 21600
    }


@app.post("/payments/{id}/cancellations")
async def cancellations(request: Request, id: str):
    body = await request.json()
    paymentId = body["paymentId"]
    requestId = body["requestId"]
    if not paymentId_consistency(id, paymentId):
        # TODO: Format the response with 400 status
        return "The paymentId values are divergent"
    return {
        "paymentId": paymentId,
        "message": "Successfully cancelled",
        "code": None,
        "cancellationId": "1457BD07E6",
        "requestId": requestId
    }


@app.post("/payments/{id}/settlements")
async def settlements(request: Request, id: str):
    body = await request.json()
    paymentId = body["paymentId"]
    value = body["value"]
    requestId = body["requestId"]
    if not paymentId_consistency(id, paymentId):
        # TODO: Format the response with 400 status
        return "The paymentId values are divergent"
    return {
        "paymentId": paymentId,
        "settleId": "CEE16492C6",
        "value": value,
        "code": None,
        "message": None,
        "requestId": requestId
    }


@app.post("/payments/{id}/refunds")
async def refunds(request: Request, id: str):
    body = await request.json()
    paymentId = body["paymentId"]
    value = body["value"]
    requestId = body["requestId"]
    if not paymentId_consistency(id, paymentId):
        # TODO: Format the response with 400 status
        return "The paymentId values are divergent"
    return {
        "paymentId": paymentId,
        "refundId": None,
        "value": value,
        "code": "refund-manually",
        "message": "Refund should be done manually",
        "requestId": requestId
    }
