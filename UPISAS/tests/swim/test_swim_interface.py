import sys
sys.path.append("/home/alejo/Documents/SAS/code/UPISAS")
import unittest
import time

from UPISAS import get_response_for_get_request, validate_schema
from UPISAS.exemplars.swim import SWIM
from UPISAS.strategies.empty_strategy import EmptyStrategy


class TestStrategy(unittest.TestCase):
    """
    Test cases for the Strategy class, using the DemoStrategy.
    Run by `python -m UPISAS.tests.demo.test_strategy` on the parent folder.
    """

    def setUp(self):
        #print("(1). setUp !!!!!!!!!!!!!!!!!")
        self.exemplar = SWIM(auto_start=True)
        self._start_server_and_wait_until_is_up()
        self.strategy = EmptyStrategy(self.exemplar)

    def tearDown(self):
        #print("(2). tearDown !!!!!!!!!!!!!!!!!")
        if self.exemplar and self.exemplar.exemplar_container:
            self.exemplar.stop_container()

    def test_get_adaptation_options_successfully(self):
        #print("!!!!!!!!!!!!!!!!! 3. test_get_adaptation_options_successfully!!!!!!!!!!!!!!!!!")
        self.strategy.get_adaptation_options(with_validation=False)
        self.assertIsNotNone(self.strategy.knowledge.adaptation_options)

    def test_monitor_successfully(self):
        #print("!!!!!!!!!!!!!!!!! 4. test_monitor_successfully !!!!!!!!!!!!!!!!!")
        successful = self.strategy.monitor(with_validation=False)
        self.assertTrue(successful)
        self.assertNotEqual(self.strategy.knowledge.monitored_data, dict())

    def test_execute_successfully(self):
        #print("!!!!!!!!!!!!!!!!! 5. test_execute_successfully !!!!!!!!!!!!!!!!!")
        successful = self.strategy.execute({"server_number": 2, "dimmer_factor": 0.5}, with_validation=False)
        self.assertTrue(successful)

    def test_adaptation_options_schema_endpoint_reachable(self):
        #print("!!!!!!!!!!!!!!!!! 6. test_adaptation_options_schema_endpoint_reachable !!!!!!!!!!!!!!!!!")
        self.strategy.get_adaptation_options_schema()
        self.assertIsNotNone(self.strategy.knowledge.adaptation_options_schema)

    def test_monitor_schema_endpoint_reachable(self):
        #print("!!!!!!!!!!!!!!!!! 7. test_monitor_schema_endpoint_reachable !!!!!!!!!!!!!!!!!")
        self.strategy.get_monitor_schema()
        self.assertIsNotNone(self.strategy.knowledge.monitor_schema)

    def test_execute_schema_endpoint_reachable(self):
        #print("!!!!!!!!!!!!!!!!! 8. test_execute_schema_endpoint_reachable !!!!!!!!!!!!!!!!!")
        self.strategy.get_execute_schema()
        self.assertIsNotNone(self.strategy.knowledge.execute_schema)

    def test_schema_of_adaptation_options(self):
        #print("!!!!!!!!!!!!!!!!! 9. test_schema_of_adaptation_options !!!!!!!!!!!!!!!!!")
        self.strategy.get_adaptation_options_schema()
        with self.assertLogs() as cm:
            self.strategy.get_adaptation_options()
            self.assertTrue("JSON object validated by JSON Schema" in ", ".join(cm.output))
        self.assertIsNotNone(self.strategy.knowledge.adaptation_options)

    def test_schema_of_monitor(self):
        #print("!!!!!!!!!!!!!!!!! 10. test_schema_of_monitor !!!!!!!!!!!!!!!!!")
        self.strategy.get_monitor_schema()
        with self.assertLogs() as cm:
            successful = self.strategy.monitor()
            self.assertTrue("JSON object validated by JSON Schema" in ", ".join(cm.output))
        self.assertTrue(successful)
        self.assertNotEqual(self.strategy.knowledge.monitored_data, dict())

    def test_schema_of_execute(self):
        #print("!!!!!!!!!!!!!!!!! 11. test_schema_of_execute !!!!!!!!!!!!!!!!!")
        self.strategy.get_execute_schema()
        with self.assertLogs() as cm:
            successful = self.strategy.execute({"server_number": 2, "dimmer_factor": 0.5})
            self.assertTrue("JSON object validated by JSON Schema" in ", ".join(cm.output))
        self.assertTrue(successful)

    def _start_server_and_wait_until_is_up(self, base_endpoint="http://localhost:3000"):
        #print("(12). _start_server_and_wait_until_is_up !!!!!!!!!!!!!!!!!")
        self.exemplar.start_run()
        while True:
            time.sleep(1)
            print("trying to connect...")
            response = get_response_for_get_request(base_endpoint)
            print(response.status_code)
            if response.status_code < 400:
                return
            
    def print_results(self):
        self.strategy.results()
 
  
  
if __name__ == '__main__':
    unittest.main()
    TestStrategy.print_results()


    # # Create a test suite
    # test_suite = unittest.TestLoader().loadTestsFromTestCase(TestStrategy)

    # # Create a test runner with detailed test result reporting
    # test_runner = unittest.TextTestRunner(resultclass=unittest.TextTestResult, verbosity=2)

    # # Run the tests and obtain the test result
    # test_result = test_runner.run(test_suite)

    # # Print additional information about the test run
    # print("\n==== Test Run Summary ====")
    # print("Number of tests run:", test_result.testsRun)
    # print("Number of errors:", len(test_result.errors))
    # print("Number of failures:", len(test_result.failures))
    # print("Number of skipped tests:", len(test_result.skipped))
    # print("Execution time (seconds):", test_result.totalTime)
 