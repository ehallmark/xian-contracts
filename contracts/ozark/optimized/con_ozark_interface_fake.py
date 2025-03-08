# con_ozark_interface_fake

@export
def deposit(commitment: str):
    process_deposit(ctx.caller)


def process_deposit(caller: str):
    pass

@export
def withdraw(a: list, b: list, c: list, root: str, nullifier_hash: str, recipient: str, relayer: str = '0',
             fee: str = '0', refund: str = '0'):
    process_withdraw(recipient, relayer, int(fee, 10), int(refund, 10))


def process_withdraw(recipient: str, relayer: str, fee: int, refund: int):
    pass