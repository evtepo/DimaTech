import hashlib
import os
from uuid import UUID

from typer import Option, Typer


app = Typer()


@app.command("Get signature.")
def main(
    account_id: UUID = Option(..., "--account_id", "-a_id", help="User account ID."),
    amount: float = Option(..., "--amount", "-a", help="Transaction amount."),
    transaction_id: UUID = Option(..., "--transaction_id", "-t_id", help="Transaction ID."),
    user_id: UUID = Option(..., "--user_id", "-u_id", help="User profile ID."),
):
    secret_key = os.environ.get("SIGNATURE_SECRET_KEY")
    data_string = f"{account_id}{amount}{transaction_id}{user_id}{secret_key}"
    signature = hashlib.sha256(data_string.encode()).hexdigest()

    print(signature)


if __name__ == "__main__":
    app()

# Usage python .\check_signature.py --account_id 3fa85f64-5717-4562-b3fc-2c963f66afa6 --amount 10.0 --transaction_id 3fa85f64-5717-4562-b3fc-2c963f66afa6 --user_id 3fa85f64-5717-4562-b3fc-2c963f66afa6
