import unittest
from requisition import Requisition

class TestRequisition(unittest.TestCase):

    def setUp(self):
        Requisition.next_id=10001

    def create_request(self, price):
        request = Requisition(
            "17/11/2026", "FN19", "John Paul"
        )

        request.add_requisition([
            {"name": "Test Item", "price": price}
        ])

        request.approve_requisition()
        return request

    def test_below_500(self):
        request = self.create_request("499.99")
        self.assertEqual(request.status, "Approved")
        self.assertEqual(
            request.approval_reference, "FN19001"
        )

    def test_exactly_500(self):
        request=self.create_request("500.00")
        self.assertEqual(request.status, "Pending")

    def test_above_500(self):
        request=self.create_request("750.00")
        self.assertEqual(request.status, "Pending")

    def test_manager_approval(self):
        request=self.create_request("750.00")
        request.respond_requisition("Approved")

        self.assertEqual(request.status, "Approved")
        self.assertEqual(
            request.approval_reference, "FN19001"
        )

    def test_manager_rejection(self):
        request=self.create_request("750.00")
        request.respond_requisition("Not approved")
        self.assertEqual(request.status, "Not approved")
        self.assertIsNone(request.approval_reference)

    def test_empty_items(self):
        request=Requisition(
            "17/11/2026", "FN19", "John Paul"
        )

        with self.assertRaises(ValueError):
            request.add_requisition([])

    def test_completed_request_cannot_change(self):
        request=self.create_request("450.00")

        with self.assertRaises(ValueError):
            request.respond_requisition("Not approved")

    def test_statistics_after_rejection(self):
        first=self.create_request("450.00")
        second=self.create_request("750.00")

        second.respond_requisition("Not approved")

        stats=Requisition.requisition_statistics(
            [first, second]
        )

        self.assertEqual(stats["total"], 2)
        self.assertEqual(stats["approved"], 1)
        self.assertEqual(stats["pending"], 0)
        self.assertEqual(stats["not_approved"], 1)

if __name__=="__main__":
    unittest.main()