# TODO: Implement the asyn flow to approved or denied transactions
# TODO: Create a function to proccess every endpoint
# TODO: Use the mocked_db in order to store the payments in memory
# TODO: Implement all the validations
#   The required fields must exist on the request payload (doc)
#   The required fields must exist on the response payload (doc)
#   The paymentId must refer to an actual payment inside the mock_db
#   Make changes on the stored payment as the non authrization routes are called

import os
import httpx
import asyncio
from dotenv import load_dotenv
from fastapi import FastAPI, Request, BackgroundTasks
from utils.utils import paymentId_consistency
# from entity.payment import Payment

app = FastAPI()

mocked_db = []

load_dotenv()
app_key = os.getenv("APP_KEY")
app_token = os.getenv("APP_TOKEN")

async def request_gateway(callbackUrl: str, payload: dict):
    await asyncio.sleep(10)
    async with httpx.AsyncClient() as client:
        # TODO: it is necessary to set the AppKey and AppToken as environment variables
        headers = {
            "X-VTEX-API-AppKey": app_key,
            "X-VTEX-API-AppToken": app_token
        }
        print("SENDING THE REQUEST TO VTEX GATEWAY")
        await client.post(callbackUrl, headers=headers, json=payload)

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
async def payments(request: Request, background_tasks: BackgroundTasks):
    body = await request.json()
    paymentId = body.get("paymentId", None)
    card = body.get("card", None)
    card_number = card.get("number", None)
    callbackUrl = body.get("callbackUrl", None)

    # TODO: Create a function that gets the body and the list of required informations and returns if something is missing
    if not paymentId:
        # TODO: Format the response with 400 status
        return {"error": "The paymentId value is required"}

    status_codes = {
        "4444333322221111": "approved",
        "4444333322221112": "denied",
    }
    status = status_codes.get(card_number, "undefined")
    async_flow = status == "undefined"

    if async_flow:
        final_status = {
            "4222222222222224": "approved",
            "4222222222222225": "denied",
        }
        final_payload = {
            "paymentId": paymentId,
            "status": final_status.get(card_number, "approved"),
            "authorizationId": "184520",
            "nsu": "21705348",
            "tid": "21705348",
            "acquirer": "pagmm",
            "code": "0000",
            "message": "Successfully approved transaction",
            "delayToAutoSettle": 1200,
            "delayToAutoSettleAfterAntifraud": 1200,
            "delayToCancel": 86400,
            "cardBrand": "Visa",
            "firstDigits": "534696",
            "lastDigits": "6921",
            "maxValue": 16.6
        }

        background_tasks.add_task(request_gateway, callbackUrl, final_payload)

    return {
        "paymentId": paymentId,
        "status": status,
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
