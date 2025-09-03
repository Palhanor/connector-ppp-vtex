# Connector Example

This Python project was created in order to exemplify how a connector integrate Payment Providers with the VTEX Platform, following all the requirements inside out Payment Provider Protocol (link).

The system is already deployed on Render, and can be accessed by the endpoint: https://connector-ppp-vtex.onrender.com/

If you have access to an VTEX Admin, you can run in on the Payment Provider Test Suite (link).

To do so, you can insert its endpoint inside the serviceUrl field, then select a payment method and the desired test flows.

Currently, the system already implements the following test flows:
- [x] Approved Flow
- [X] Canceled Flow
- [ ] Denied Flow
- [ ] Aproved Flow Async
- [ ] Denied Flow Async
- [ ] Bank Invoice
- [ ] Redirect

Also, you can run the system locally, if you want to: `uvicorn main:app --reload`