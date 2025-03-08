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
OZARK_CONTRACT = 'con_ozark'
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
        denomination = contract.quick_read('denomination')
        self.assertEqual(denomination, DENOMINATION)

        phi = get_contract_for_signer(PHI_CONTRACT, 'me')

        t0 = time.time()
        phi.approve(
            amount=denomination,
            to=OZARK_CONTRACT
        )
        print(f'Time to approve PHI: {time.time()-t0}')
        roots = contract.quick_read('roots_var')
        self.assertIsNone(roots[1])
        self.assertIsNotNone(roots[0])

        my_balance = phi.quick_read('balances', 'me')

        t0 = time.time()
        contract.deposit(
            commitment=str(int('0x1950ebe4d7216447872e8ede2bb68231db6efb3d7a7095fec917ea845817374f', 16)) 
        )
        print(f'Time to deposit PHI: {time.time()-t0}')

        my_balance_after = phi.quick_read('balances', 'me')
        self.assertEqual(my_balance_after, my_balance - denomination)
        

        roots = contract.quick_read('roots_var')
        self.assertIsNotNone(roots[1])
        self.assertIsNotNone(roots[0])

        print_merkle_tree_state(contract)

        contract = get_contract_for_signer(OZARK_CONTRACT, 'you')

        # Invalid proof
        self.assertRaises(
            AssertionError,
            contract.withdraw,
            a=[ '18288273192161579501559134970696155822958421006432149721281330353407118730128',
                        '17353588396131661126245745982587261375827295667438780513735339175642821258321',
                        '1',
                        ],
            b=[ [ '12125316320847185546562695625645182892500099839848079025080535996695216683118',
                        '4993025356303449615749918267052219918572354519587843071166840459213139693209' ],
                        [ '14158536489823746118403555147857164326362615910067794436256423605048234858053',
                        '8518835161344602633167560617564286697934143463831387733625072298536149883128' ],
                        ['0', '1']
                        ],
            c=[ '14388363169789310207600157865851192764635251728868908908016597348886727301005',
                        '7219883015026041181003762589573104239981463267036641872486652648210704250574',
                        '1'],
            root='19472974227534089877661842339747066589074924514634613071633204486088526229164',
            nullifier_hash=to_base10_str('2803dbac4530cf1c3d16a948a3122e1b1288bf56291848a9e433ad46771f50a1'),
            recipient=to_base10_str('1e240'),
            relayer=to_base10_str('0'),
            fee=to_base10_str('0'),
            refund=to_base10_str('0')
        )

        # Correct proof
        recipient = '3af8c271423e93586837f5c53b776bb231d062f477a474f57f3cfc24e8d776'
        proof_data = { 'pi_a':
        [ '13774734694806893345431794156356514571363079254825067879443184821206447822750',
            '5209428786776521202856824112990553528771784326411286192918798384107382954954',
            '1' ],
        'pi_b':
        [ [ '5173078677927959662734785177277144661908479282203617744477925437547277462997',
            '5008919259924401514229994859356982028735024574680767144772652733435392622987' ],
            [ '16237021846884756770715728474067652062799669637447076030779615223774369289462',
            '2712062232854900554770345916314277164381058075864652478551356549239494502978' ],
            [ '1', '0' ] ],
        'pi_c':
        [ '11709473128502841396551378248174338037383283271432381215788718530577500746586',
            '4008944338641772649658914022116044050220759783362908976331068335514955377268',
            '1' ],
        'publicSignals':
        [ '19472974227534089877661842339747066589074924514634613071633204486088526229164',
            '18099330611372391564551405916666174527872771719801289262717800528837024370849',
            recipient,
            '0',
            '0',
            '0' ] }

        a = proof_data['pi_a']
        b = proof_data['pi_b']
        c = proof_data['pi_c']

        inputs = proof_data['publicSignals']

        contract = get_contract_for_signer(OZARK_CONTRACT, 'you')
        recipient_balance = phi.quick_read('balances', recipient)
        self.assertIsNone(recipient_balance)

        t0 = time.time()
        contract.withdraw(
            a=a,
            b=b,
            c=c,
            root=inputs[0],
            nullifier_hash=inputs[1],
            recipient=inputs[2],
            relayer=inputs[3],
            fee=inputs[4],
            refund=inputs[5]
        )
        print(f'Time to withdraw PHI: {time.time()-t0}')

        # Check recipient's balance
        recipient_balance_after = phi.quick_read('balances', recipient)
        self.assertEqual(recipient_balance_after, denomination)

        # Double check my balance
        my_balance_after_after = phi.quick_read('balances', 'me')
        self.assertEqual(my_balance_after, my_balance_after_after)

        # Make sure cannot double withdraw
        self.assertRaises(
            AssertionError,
            contract.withdraw,
            a=a,
            b=b,
            c=c,
            root=inputs[0],
            nullifier_hash=inputs[1],
            recipient=inputs[2],
            relayer=inputs[3],
            fee=inputs[4],
            refund=inputs[5]
        )
        recipient_balance_after = phi.quick_read('balances', recipient)
        self.assertEqual(recipient_balance_after, denomination)

if __name__ == '__main__':
    unittest.main()