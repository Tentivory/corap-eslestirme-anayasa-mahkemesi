#!/usr/bin/env python3
"""Mahkeme kendi kendini temyiz eder. Gecmezse corap sucludur, test degil."""

import unittest

from corap_mahkemesi import HUKUMLER, yargila


class TestMahkeme(unittest.TestCase):
    def test_esas_no_kararli(self):
        a = yargila("kirmizi noktali", tohum=7)
        b = yargila("kirmizi noktali", tohum=7)
        self.assertEqual(a.esas_no, b.esas_no)
        self.assertEqual(a.hukum, b.hukum)

    def test_hukum_listede(self):
        karar = yargila("delikli ofis corabi", tohum=1)
        self.assertIn(karar.hukum, HUKUMLER)

    def test_bos_corap_kimlik_alir(self):
        karar = yargila("   ")
        self.assertIn("belirsiz", karar.corap)


if __name__ == "__main__":
    unittest.main()
