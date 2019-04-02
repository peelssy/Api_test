import unittest
import requests


class TestBooks(unittest.TestCase):


    @classmethod
    def setUpClass(cls):
        cls.base = "http://pulse-rest-testing.herokuapp.com/"
        cls.book_url = cls.base + "books/"

    def setUp(self):
        self.book_data = {"title": "Green Mile", "author": "Steven King"}

    def test_crud(self):
        resp_cre = requests.post(self.book_url, data=self.book_data)
        self.assertEqual(resp_cre.status_code, 201)
        resp_data = resp_cre.json()
        self.assertIn("id", resp_data)
        self.book_data["id"] = resp_data["id"]

        for key in resp_data:
            self.assertEqual(self.book_data[key], resp_data[key])

        resp_put = requests.put(self.book_url + str(self.book_data["id"]), data={"title": "8 Mile"})
        self.assertEqual(resp_put.status_code, 200)

        resp_del = requests.delete(self.book_url + str(self.book_data["id"]))
        self.assertEqual(resp_del.status_code, 204)
        resp = requests.get(self.book_url + str(self.book_data["id"]))
        self.assertEqual(resp.status_code, 404)

    def tearDown(self):
        resp = requests.get(self.book_url + str(self.book_data["id"]))
        if resp.status_code is not 404:
            requests.delete(self.book_url + str(self.book_data["id"]))


if __name__ == "__main__":
    unittest.main(verbosity=2)