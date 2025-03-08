from xian_py.wallet import Wallet
from xian_py.xian import Xian
from dotenv import load_dotenv
import os

load_dotenv()
#contract_name = 'con_ozark_currency_1000_v1'
#with open(f'./contracts/ozark/optimized/con_ozark.py', 'r') as file:
#    code = file.read()

contract_name = 'con_ozark_interface_fake'
with open(f'./contracts/ozark/optimized/{contract_name}.py', 'r') as file:
    code = file.read()

# Give your contract a name to be submitted as, must start with `con_`

wallet = Wallet(os.getenv('PRIVATE_KEY'))
xian = Xian(os.getenv('XIAN_NETWORK_URL'), wallet=wallet)

# Deploy contract to network and pass arguments to it
arguments = {
    "denomination_value": 1000,
    "token_contract_value": "currency"
}

submit = xian.submit_contract(
    contract_name,
    code,
    #args=arguments,
    stamps=2000
)

print(f'success: {submit["success"]}')
print(f'tx_hash: {submit["tx_hash"]}')
print(f'view tx in explorer: https://explorer.xian.org/tx/{submit["tx_hash"]}')
