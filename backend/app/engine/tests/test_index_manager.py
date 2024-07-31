import sys
import unittest
from parameterized import parameterized
from index_manager import IndexManager

sys.path.append("backend")


class TestSemanticSearch(unittest.TestCase):

    @classmethod
    def set_up_class(cls):
        cls.index_manager = IndexManager()
        cls.data_dict_name = "orders"
        cls.index_manager.create_or_load_index(cls.data_dict_name)

    def assert_count_equal_with_one_extra(self, result_table_names, expected_output):
        self.assert_greater_equal(set(result_table_names), set(expected_output))
        self.assert_less_equal(len(result_table_names) - len(expected_output), 1)

    @parameterized.expand(
        [
            (
                "all information about products that belong to an order placed by a user whose first name is alex",
                ["orders", "products", "order_items", "users", "categories"],
            ),
            (
                "give me the email of the user whose name starts with the letter a",
                ["users"],
            ),
            (
                "the surname of users who paid for all their orders with PayPal",
                ["users", "orders"],
            ),
            ("the total amount of each order", ["products", "orders", "order_items"]),
            (
                "total cost of orders placed by users with PayPal",
                ["orders", "products", "order_items"],
            ),
        ]
    )
    def test_semantic_search_first_battery(self, input_value, expected_output):
        tuples = self.index_manager.get_relevant_tuples(
            self.index_manager.get_tuples(input_value, activate_log=False),
            activate_log=False,
        )
        result_table_names = [tuple["table_name"] for tuple in tuples]
        self.assert_count_equal_with_one_extra(result_table_names, expected_output)
        # Per un controllo più preciso
        # self.assertCountEqual(result_table_names, expected_output)

    @parameterized.expand(
        [
            (
                "all information on users who paid for their orders with PayPal",
                ["users", "orders"],
            ),
            ("the username of all users", ["users"]),
            ("the total price of each order", ["products", "orders", "order_items"]),
            (
                "all information about products that belong to an order placed by alex71",
                ["orders", "products", "order_items", "categories"],
            ),
            (
                "total cost of orders placed by users with PayPal",
                ["orders", "products", "order_items"],
            ),
        ]
    )
    def test_semantic_search_second_battery(self, input_value, expected_output):
        tuples = self.index_manager.get_relevant_tuples(
            self.index_manager.get_tuples(input_value, activate_log=False),
            activate_log=False,
        )
        result_table_names = [tuple["table_name"] for tuple in tuples]
        self.assert_count_equal_with_one_extra(result_table_names, expected_output)
        # Per un controllo più preciso
        # self.assertCountEqual(result_table_names, expected_output)

    @parameterized.expand(
        [
            (
                "all information on products that belong to the food category and that refer to an order placed by a user whose name is alex",
                ["orders", "products", "order_items", "users", "categories"],
            ),
            (
                "the name of the users who purchased three quantities of the same product yesterday",
                ["orders", "users", "products", "order_items"],
            ),
        ]
    )
    def test_semantic_search_third_battery(self, input_value, expected_output):
        tuples = self.index_manager.get_relevant_tuples(
            self.index_manager.get_tuples(input_value, activate_log=False),
            activate_log=False,
        )
        result_table_names = [tuple["table_name"] for tuple in tuples]
        self.assert_count_equal_with_one_extra(result_table_names, expected_output)
        # Per un controllo più preciso
        # self.assertCountEqual(result_table_names, expected_output)


if __name__ == "__main__":
    unittest.main()
