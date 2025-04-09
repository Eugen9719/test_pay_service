from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class Msg(BaseModel):
    msg: str


class TokenPayload(BaseModel):
    sub: str


class WebhookRequest(BaseModel):
    transaction_id: str
    account_id: int
    user_id: int
    amount: int
    signature: str










