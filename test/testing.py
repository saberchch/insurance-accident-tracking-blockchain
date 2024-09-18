import unittest
from test.blockchain import app

class TestBlockchainE2E(unittest.TestCase):

    def test_e2e_block_creation(self):
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = "your_secret_key_here"

        with app.test_client() as client:
            # Simulate genesis block creation
            response = client.post('/create_genesis_block', 
                                   data=dict(initial_year=2024, 
                                             initial_month=1, 
                                             num_accidents=10))
            self.assertEqual(response.status_code, 302)  # Redirect indicates success

            # Check that the genesis block was created
            with client.session_transaction() as session:
                blockchain = session.get("blockchain")
                self.assertIsNotNone(blockchain)
                self.assertEqual(len(blockchain['chain']), 1)  # Check that genesis block is created

            # Simulate adding more accidents
            response = client.post('/add_accidents', 
                                   data=dict(year=2024, month=2, num_accidents=15))
            self.assertEqual(response.status_code, 302)  # Redirect indicates success

            # Check that the new block was added
            with client.session_transaction() as session:
                blockchain = session.get("blockchain")
                self.assertIsNotNone(blockchain)
                self.assertEqual(len(blockchain['chain']), 2)  # Check that a new block was added

if __name__ == "__main__":
    unittest.main(verbosity=2)
