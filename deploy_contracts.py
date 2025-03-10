from xian_py.wallet import Wallet
from xian_py.xian import Xian
from dotenv import load_dotenv
from xian_py.transaction import get_nonce, create_tx, simulate_tx, broadcast_tx_sync
import os

load_dotenv()
#contract_name = 'con_ozark_currency_1000_v1'
#with open(f'./contracts/ozark/optimized/con_ozark.py', 'r') as file:
#    code = file.read()


wallet = Wallet(os.getenv('PRIVATE_KEY'))
xian = Xian(os.getenv('XIAN_NETWORK_URL'), wallet=wallet)
node_url = os.getenv('XIAN_NETWORK_URL')

# Prepare transaction payload
payload = {
    "chain_id": xian.get_chain_id(),
    "contract": "con_ozark_interface_fake_v2",
    "function": "deposit",
    "kwargs": {"commitment": "2670076134747319545324230009109098125221204711607719583042285768625025388659"},
    "nonce": get_nonce(node_url, wallet.public_key),
    "sender": wallet.public_key,
    "stamps_supplied": 0
}
# Simulate to get stamp cost
simulated = simulate_tx(node_url, payload)
print(f"Required stamps: {simulated['stamps_used']}")


exit(0)


contract_name = 'con_ozark_interface_fake_v2'
with open(f'./contracts/ozark/optimized/{contract_name}.py', 'r') as file:
    code = file.read()

# Deploy contract to network and pass arguments to it
arguments = {
    "denomination_value": 10,
    "token_contract_value": "currency"
}

submit = xian.submit_contract(
    contract_name,
    code,
    args=arguments,
    stamps=2000
)

print(f'success: {submit["success"]}')
print(f'tx_hash: {submit["tx_hash"]}')
print(f'view tx in explorer: https://explorer.xian.org/tx/{submit["tx_hash"]}')
