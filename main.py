# uvicorn main:app --reload

# TODO: Criar uma função para processar cada operação
# TODO: Validações ---
#   Os campos obrigatórios do payload da request são recebidos
#   O paymentId existe dentro do DB
#   O paymentId da rota é o mesmo do payload
#   Garantir que todos os dados obrigatórios estão sendo retornados
#   Garatnir que tudo é consistente com o paymentId em questão
#   Alterar o paymentId enquanto o processamento é realizado
#   Garantir que o valor no campo da resposta é o mesmo que no campo da requisição (ou alterado quando necessário, tipo o value)

from fastapi import Request, FastAPI

app = FastAPI()

db = [

]  # TODO: Criar uma classe transaction que vai sendo montada a medida que o fluxo é desenvolvido


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
    paymentId = body["paymentId"]
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
async def concellation(request: Request, id: str):
    body = await request.json()
    paymentId = body["paymentId"]
    requestId = body["requestId"]
    return {
        "paymentId": paymentId,
        "message": "Successfully cancelled",
        "code": None,
        "cancellationId": "1457BD07E6",
        "requestId": requestId
    }


@app.post("/payments/{id}/settlements")
async def settlement(request: Request, id: str):
    body = await request.json()
    paymentId = body["paymentId"]
    value = body["value"]
    requestId = body["requestId"]
    return {
        "paymentId": paymentId,
        "settleId": "CEE16492C6",
        "value": value,
        "code": None,
        "message": None,
        "requestId": requestId
    }


@app.post("/payments/{id}/refunds")
async def refund(request: Request, id: str):
    body = await request.json()
    paymentId = body["paymentId"]
    value = body["value"]
    requestId = body["requestId"]

    return {
        "paymentId": paymentId,
        "refundId": None,
        "value": value,
        "code": "refund-manually",
        "message": "Refund should be done manually",
        "requestId": requestId
    }
