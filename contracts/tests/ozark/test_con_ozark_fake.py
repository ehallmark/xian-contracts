#tests/test_contract.py
import unittest
import os
from contracting.client import ContractingClient
from os.path import dirname, abspath, join
import time

client = ContractingClient()

module_dir = join(dirname(dirname(dirname(abspath(__file__)))), 'ozark')

VERIFIER_CONTRACT_OPT = 'con_verifier_optimized'
VERIFIER_CONTRACT_PAIRING = 'con_verifier_opt_pairing_mini'
CTS_CONTRACT = 'con_mimc_cts'
OZARK_CONTRACT = 'con_ozark_interface_fake_v2'
PHI_CONTRACT = 'con_phi_lst001'
DENOMINATION = 100_000

t0 = time.time()

with open(join(dirname(module_dir), 'core', f'{PHI_CONTRACT}.py'), 'r') as f:
    code = f.read()
    client.submit(code, name=PHI_CONTRACT, signer='me')

print(f'Time to submit PHI_CONTRACT: {time.time()-t0}')

t1 = time.time()
with open(os.path.join(module_dir, 'optimized', f'{VERIFIER_CONTRACT_PAIRING}.py'), 'r') as f:
    code = f.read()
    client.submit(code, name=VERIFIER_CONTRACT_PAIRING, signer='me')

print(f'Time to submit VERIFIER_CONTRACT_PAIRING: {time.time()-t1}')

t1 = time.time()
with open(os.path.join(module_dir, 'optimized', f'{VERIFIER_CONTRACT_OPT}.py'), 'r') as f:
    code = f.read()
    client.submit(code, name=VERIFIER_CONTRACT_OPT, signer='me')

print(f'Time to submit VERIFIER_CONTRACT_OPT: {time.time()-t1}')

t1 = time.time()
with open(os.path.join(module_dir, 'optimized', f'{CTS_CONTRACT}.py'), 'r') as f:
    code = f.read()
    client.submit(code, name=CTS_CONTRACT, signer='me')

print(f'Time to submit CTS_CONTRACT: {time.time()-t1}')

t1 = time.time()
with open(os.path.join(module_dir, 'optimized', f'{OZARK_CONTRACT}.py'), 'r') as f:
    code = f.read()
    client.submit(code, name=OZARK_CONTRACT, signer='me', constructor_args={'token_contract_value': PHI_CONTRACT})

print(f'Time to submit OZARK_CONTRACT: {time.time()-t1}')

print(f'Time to submit contracts: {time.time()-t0}')


def get_contract_for_signer(contract: str, signer: str):
    client.signer = signer
    contract = client.get_contract(contract)
    return contract


def print_merkle_tree_state(contract):
    roots = contract.quick_read('roots_var')
    zeros = contract.quick_read('zeros_var')
    filled_subtrees = contract.quick_read('filled_subtrees_var')
    next_index = contract.quick_read('next_index')
    current_root_index = contract.quick_read('current_root_index')
    
    print(f'roots: {roots}')
    print(f'zeros: {zeros}')
    print(f'filled_subtrees: {filled_subtrees}')
    print(f'next_index: {next_index}')
    print(f'current_root_index: {current_root_index}')

def to_base10_str(i: str) -> str:
    return str(int(i, 16))

class MyTestCase(unittest.TestCase):
    def test_e2e(self):
        contract = get_contract_for_signer(OZARK_CONTRACT, 'me')

        print_merkle_tree_state(contract)

        phi = get_contract_for_signer(PHI_CONTRACT, 'me')

        roots = contract.quick_read('roots_var')
        self.assertIsNone(roots[1])
        self.assertIsNotNone(roots[0])

        t0 = time.time()
        contract.deposit(
            commitment=str(int('0x1950ebe4d7216447872e8ede2bb68231db6efb3d7a7095fec917ea845817374f', 16)) 
        )
        print(f'Time to deposit PHI: {time.time()-t0}')

        roots = contract.quick_read('roots_var')
        self.assertIsNotNone(roots[1])
        self.assertIsNotNone(roots[0])

        print_merkle_tree_state(contract)

if __name__ == '__main__':
    unittest.main()