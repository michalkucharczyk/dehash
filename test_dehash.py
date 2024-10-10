import unittest
import re
from dehash import (
    add_specific_replacement, specific_replacements,
    filter_and_findall, replace_matches_in_place,
    generate_word, generate_short_hash, replace_hashes, append_word_to_dictionary
)

# How to run:
# python3 ./test_dehash.py TestScript.test_filter_and_findall
# python3 ./test_dehash.py TestScript

class TestScript(unittest.TestCase):
    def setUp(self):
        # Initialize some content and patterns for testing
        self.content = """Line 1: The quick brown fox jumps over the lazy dog.
        Line 2: [Relaychain] 🏆 Imported #1234 (0x1234…cdef → 0xabcd…5678)"""

    def test_filter_and_findall(self):
        (pattern, guard)= next(((pattern, guard) for (pattern, replacement_prefix, guard) in specific_replacements if guard == "Imported"), None)
        matches = filter_and_findall(self.content, guard, pattern)
        self.assertEqual(len(matches), 1)
        print(matches[0])
        self.assertEqual(matches[0], ('1234', '0xabcd…5678'))

    def test_replace_matches_in_place(self):
        def replacement_func(match):
            return 'REPLACED'
        content = "This is a test string with 0x1234…5678 and another 0x9abc…def0 and yet another 0x1234…5678."
        pattern = r'0x[0-9a-f]{4}…[0-9a-f]{4}'
        result = replace_matches_in_place(content, pattern, replacement_func)
        self.assertEqual(result, "This is a test string with REPLACED and another REPLACED and yet another REPLACED.")

    def test_generate_word(self):
        word = generate_word()
        self.assertTrue(len(word) <= 6)

    def test_generate_word2(self):
        word = generate_word()
        while len(word) < 8:
            word = generate_word()

    def test_generate_short_hash(self):
        long_hash = "0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"
        short_hash = generate_short_hash(long_hash)
        self.assertEqual(short_hash, "0x1234…cdef")

    def test_replace_hashes(self):
        modified_content, hash_to_word = replace_hashes(self.content, {})
        self.assertIn('RBLOCK1234', modified_content)
        self.assertTrue(any(re.match(r'0x[0-9a-f]{4}…[0-9a-f]{4}', k) for k in hash_to_word.keys()))


class TestScriptBlockHashes(unittest.TestCase):
    def setUp(self):
        append_word_to_dictionary("DIPLEX")
        self.content = """
2024-06-11 21:52:15.129  INFO tokio-runtime-worker substrate: 🏆 Imported #1 (0xdf18…c4ac → 0x0626…a11a)    
2024-06-11 21:52:15.129  INFO tokio-runtime-worker txpool: maintain: txs:(0, 0) views:[1;[(1, 0, 0)]] event:NewBestBlock { hash: 0x0626c20236b05022c206363171118c7881fc8b0cd8d0b4f6d155f3dc6919a11a, tree_route: None }  took:122.731µs    
2024-06-11 21:52:18.007  INFO tokio-runtime-worker txpool: maintain: txs:(0, 0) views:[1;[(2, 0, 0)]] event:NewBestBlock { hash: 0x028dd13e51d2506717ccd5805ba01d55b5075638466a9fb9cc16b6b4812d8955, tree_route: None }  took:178.051µs    
2024-06-11 21:52:18.007  INFO tokio-runtime-worker substrate: 🏆 Imported #2 (0x0626…a11a → 0x028d…8955)    
2024-06-11 21:52:21.013  INFO tokio-runtime-worker txpool: maintain: txs:(0, 0) views:[1;[(3, 0, 0)]] event:NewBestBlock { hash: 0x76846df7d3378038af3ef3fe6a59f594a44f040b7b11e514426b9a6d8e83949b, tree_route: None }  took:132.931µs    
2024-06-11 21:52:21.013  INFO tokio-runtime-worker substrate: 🏆 Imported #3 (0x028d…8955 → 0x7684…949b)    
2024-06-11 21:52:22.551  INFO tokio-runtime-worker txpool: maintain: txs:(0, 0) views:[1;[(3, 0, 0)]] event:Finalized { hash: 0x0626c20236b05022c206363171118c7881fc8b0cd8d0b4f6d155f3dc6919a11a, tree_route: [] }  took:102.751µs    
2024-06-11 21:52:24.007  INFO tokio-runtime-worker txpool: maintain: txs:(0, 0) views:[1;[(4, 0, 0)]] event:NewBestBlock { hash: 0xf8d786dc0ceb6ccdec7ea346c97117cb2d7118f4c62ac467b867d3fadc55d1a7, tree_route: None }  took:146.711µs    
2024-06-11 21:52:24.007  INFO tokio-runtime-worker substrate: 🏆 Imported #4 (0x7684…949b → 0xf8d7…d1a7)    
2024-06-11 21:52:25.221  INFO tokio-runtime-worker txpool: maintain: txs:(0, 0) views:[1;[(4, 0, 0)]] event:Finalized { hash: 0x028dd13e51d2506717ccd5805ba01d55b5075638466a9fb9cc16b6b4812d8955, tree_route: [] }  took:93.141µs    
2024-06-11 21:52:27.007  INFO tokio-runtime-worker substrate: 🏆 Imported #5 (0xf8d7…d1a7 → 0xaa9f…ed5b)    
2024-06-11 21:52:27.084  INFO tokio-runtime-worker txpool: maintain: txs:(0, 4096) views:[1;[(5, 0, 4096)]] event:NewBestBlock { hash: 0xaa9ffe7ff51cfc925e92bc2187f1931c42f46a4dba430ce030c98d321f0bed5b, tree_route: None }  took:76.681533ms    
2024-06-11 21:52:27.890  INFO tokio-runtime-worker txpool: maintain: txs:(0, 4096) views:[1;[(5, 0, 4096)]] event:Finalized { hash: 0x76846df7d3378038af3ef3fe6a59f594a44f040b7b11e514426b9a6d8e83949b, tree_route: [] }  took:315.913µs    
2024-06-11 21:52:30.005  INFO tokio-runtime-worker substrate: 🏆 Imported #6 (0xaa9f…ed5b → 0x5148…5220)    
2024-06-11 21:52:30.085  INFO tokio-runtime-worker txpool: maintain: txs:(0, 4096) views:[1;[(6, 0, 4096)]] event:NewBestBlock { hash: 0x51482651fa7c523ed0c59bd1167179c3577c3ab044ac34c86cf62ec5d6a25220, tree_route: None }  took:80.883737ms    
2024-06-11 21:52:31.895  INFO tokio-runtime-worker txpool: maintain: txs:(0, 4096) views:[1;[(6, 0, 4096)]] event:Finalized { hash: 0xf8d786dc0ceb6ccdec7ea346c97117cb2d7118f4c62ac467b867d3fadc55d1a7, tree_route: [] }  took:290.783µs"""

    def test_replace(self):
        self.maxDiff = None
        expected = """
2024-06-11 21:52:15.129  INFO tokio-runtime-worker substrate: 🏆 Imported #1 (DIPLEX → BLOCK1)    
2024-06-11 21:52:15.129  INFO tokio-runtime-worker txpool: maintain: txs:(0, 0) views:[1;[(1, 0, 0)]] event:NewBestBlock { hash: BLOCK1, tree_route: None }  took:122.731µs    
2024-06-11 21:52:18.007  INFO tokio-runtime-worker txpool: maintain: txs:(0, 0) views:[1;[(2, 0, 0)]] event:NewBestBlock { hash: BLOCK2, tree_route: None }  took:178.051µs    
2024-06-11 21:52:18.007  INFO tokio-runtime-worker substrate: 🏆 Imported #2 (BLOCK1 → BLOCK2)    
2024-06-11 21:52:21.013  INFO tokio-runtime-worker txpool: maintain: txs:(0, 0) views:[1;[(3, 0, 0)]] event:NewBestBlock { hash: BLOCK3, tree_route: None }  took:132.931µs    
2024-06-11 21:52:21.013  INFO tokio-runtime-worker substrate: 🏆 Imported #3 (BLOCK2 → BLOCK3)    
2024-06-11 21:52:22.551  INFO tokio-runtime-worker txpool: maintain: txs:(0, 0) views:[1;[(3, 0, 0)]] event:Finalized { hash: BLOCK1, tree_route: [] }  took:102.751µs    
2024-06-11 21:52:24.007  INFO tokio-runtime-worker txpool: maintain: txs:(0, 0) views:[1;[(4, 0, 0)]] event:NewBestBlock { hash: BLOCK4, tree_route: None }  took:146.711µs    
2024-06-11 21:52:24.007  INFO tokio-runtime-worker substrate: 🏆 Imported #4 (BLOCK3 → BLOCK4)    
2024-06-11 21:52:25.221  INFO tokio-runtime-worker txpool: maintain: txs:(0, 0) views:[1;[(4, 0, 0)]] event:Finalized { hash: BLOCK2, tree_route: [] }  took:93.141µs    
2024-06-11 21:52:27.007  INFO tokio-runtime-worker substrate: 🏆 Imported #5 (BLOCK4 → BLOCK5)    
2024-06-11 21:52:27.084  INFO tokio-runtime-worker txpool: maintain: txs:(0, 4096) views:[1;[(5, 0, 4096)]] event:NewBestBlock { hash: BLOCK5, tree_route: None }  took:76.681533ms    
2024-06-11 21:52:27.890  INFO tokio-runtime-worker txpool: maintain: txs:(0, 4096) views:[1;[(5, 0, 4096)]] event:Finalized { hash: BLOCK3, tree_route: [] }  took:315.913µs    
2024-06-11 21:52:30.005  INFO tokio-runtime-worker substrate: 🏆 Imported #6 (BLOCK5 → BLOCK6)    
2024-06-11 21:52:30.085  INFO tokio-runtime-worker txpool: maintain: txs:(0, 4096) views:[1;[(6, 0, 4096)]] event:NewBestBlock { hash: BLOCK6, tree_route: None }  took:80.883737ms    
2024-06-11 21:52:31.895  INFO tokio-runtime-worker txpool: maintain: txs:(0, 4096) views:[1;[(6, 0, 4096)]] event:Finalized { hash: BLOCK4, tree_route: [] }  took:290.783µs"""
        modified_content, hash_to_word = replace_hashes(self.content, {})
        self.assertEqual(modified_content, expected)

class TestScriptBlockHashesForks(unittest.TestCase):
    def setUp(self):
        append_word_to_dictionary("DIPLEX")
        # Initialize some content and patterns for testing
        self.content = """
2024-06-11 21:53:30.006  INFO tokio-runtime-worker substrate: 🏆 Imported #20 (0xdb4b…bd58 → 0xde0c…c522)    
2024-06-11 21:53:33.005  INFO tokio-runtime-worker substrate: 🏆 Imported #21 (0xde0c…c522 → 0x0005…6914)    
2024-06-11 21:53:33.007  INFO tokio-runtime-worker substrate: 🏆 Imported #21 (0xde0c…c522 → 0xdcd3…b73c)    
        """

    def test_replace(self):
        self.maxDiff = None
        expected = """
2024-06-11 21:53:30.006  INFO tokio-runtime-worker substrate: 🏆 Imported #20 (DIPLEX → BLOCK20)    
2024-06-11 21:53:33.005  INFO tokio-runtime-worker substrate: 🏆 Imported #21 (BLOCK20 → BLOCK21)    
2024-06-11 21:53:33.007  INFO tokio-runtime-worker substrate: 🏆 Imported #21 (BLOCK20 → BLOCK21f01)    
        """
        modified_content, hash_to_word = replace_hashes(self.content, {})
        self.assertEqual(modified_content, expected)

class TestScriptHashes(unittest.TestCase):
    def setUp(self):
        append_word_to_dictionary("AAAA")
        append_word_to_dictionary("BBBB")
        append_word_to_dictionary("CCCC")
        append_word_to_dictionary("DDDD")
        self.content = """
2024-06-11 21:52:26.047 DEBUG tokio-runtime-worker txpool: [0x5064528fea22246df948814b11da057079fc02268a6321172392e36319ff652d] ValidatedPool::submit_at
2024-06-11 21:52:26.047 DEBUG tokio-runtime-worker txpool: [0xd4418332fbea4124a743395aebfc4000829a7bdcd7afac0016b1c03106c56960] ValidatedPool::submit_at
2024-06-11 21:52:26.047 DEBUG tokio-runtime-worker txpool: [0x5869c9a4f7bace630f90928e50dc27653a2fd996abcd9e57a6b9af8642ea21d2] ValidatedPool::submit_at
2024-06-11 21:52:26.048 DEBUG tokio-runtime-worker txpool: [0xf9b677735803998fcce33eca325008f884a69dd036f0b5c1dcd8fb65bacb8cba] ValidatedPool::submit_at
2024-06-11 21:52:26.047 DEBUG tokio-runtime-worker txpool: [0x5869…21d2] Lorem ipsum dol
2024-06-11 21:52:26.048 DEBUG tokio-runtime-worker txpool: [0xf9b6…8cba] Lorem ipsum dol
2024-06-11 21:52:26.047 DEBUG tokio-runtime-worker txpool: [0x5064…652d] Lorem ipsum dol
2024-06-11 21:52:26.047 DEBUG tokio-runtime-worker txpool: [0xd441…6960] Lorem ipsum dol
2024-06-11 21:52:26.604  INFO tokio-runtime-worker sc_basic_authorship::basic_authorship: 🎁 Prepared block for proposing at ...  [0x5064…652d, 0xd441…6960, 0x5869…21d2, 0xf9b6…8cba]"
        """

    def test_replace(self):
        self.maxDiff = None
        expected = """
2024-06-11 21:52:26.047 DEBUG tokio-runtime-worker txpool: [DDDD] ValidatedPool::submit_at
2024-06-11 21:52:26.047 DEBUG tokio-runtime-worker txpool: [CCCC] ValidatedPool::submit_at
2024-06-11 21:52:26.047 DEBUG tokio-runtime-worker txpool: [BBBB] ValidatedPool::submit_at
2024-06-11 21:52:26.048 DEBUG tokio-runtime-worker txpool: [AAAA] ValidatedPool::submit_at
2024-06-11 21:52:26.047 DEBUG tokio-runtime-worker txpool: [BBBB] Lorem ipsum dol
2024-06-11 21:52:26.048 DEBUG tokio-runtime-worker txpool: [AAAA] Lorem ipsum dol
2024-06-11 21:52:26.047 DEBUG tokio-runtime-worker txpool: [DDDD] Lorem ipsum dol
2024-06-11 21:52:26.047 DEBUG tokio-runtime-worker txpool: [CCCC] Lorem ipsum dol
2024-06-11 21:52:26.604  INFO tokio-runtime-worker sc_basic_authorship::basic_authorship: 🎁 Prepared block for proposing at ...  [DDDD, CCCC, BBBB, AAAA]"
        """
        modified_content, hash_to_word = replace_hashes(self.content, {})
        self.assertEqual(modified_content, expected)


class TestScriptDictionary(unittest.TestCase):
    def setUp(self):
        self.content = """
2024-06-11 21:52:26.047 DEBUG tokio-runtime-worker txpool: [0x5064528fea22246df948814b11da057079fc02268a6321172392e36319ff652d] ValidatedPool::submit_at
2024-06-11 21:52:26.047 DEBUG tokio-runtime-worker txpool: [0xd4418332fbea4124a743395aebfc4000829a7bdcd7afac0016b1c03106c56960] ValidatedPool::submit_at
2024-06-11 21:52:26.047 DEBUG tokio-runtime-worker txpool: [0x5869c9a4f7bace630f90928e50dc27653a2fd996abcd9e57a6b9af8642ea21d2] ValidatedPool::submit_at
2024-06-11 21:52:26.048 DEBUG tokio-runtime-worker txpool: [0xf9b677735803998fcce33eca325008f884a69dd036f0b5c1dcd8fb65bacb8cba] ValidatedPool::submit_at
2024-06-11 21:52:26.047 DEBUG tokio-runtime-worker txpool: [0x5869…21d2] Lorem ipsum dol
2024-06-11 21:52:26.048 DEBUG tokio-runtime-worker txpool: [0xf9b6…8cba] Lorem ipsum dol
2024-06-11 21:52:26.047 DEBUG tokio-runtime-worker txpool: [0x5064…652d] Lorem ipsum dol
2024-06-11 21:52:26.047 DEBUG tokio-runtime-worker txpool: [0xd441…6960] Lorem ipsum dol
2024-06-11 21:52:26.604  INFO tokio-runtime-worker sc_basic_authorship::basic_authorship: 🎁 Prepared block for proposing at ...  [0x5064…652d, 0xd441…6960, 0x5869…21d2, 0xf9b6…8cba]"
        """

    def test_replace(self):
        self.maxDiff = None
        expected = """
2024-06-11 21:52:26.047 DEBUG tokio-runtime-worker txpool: [DDDD] ValidatedPool::submit_at
2024-06-11 21:52:26.047 DEBUG tokio-runtime-worker txpool: [CCCC] ValidatedPool::submit_at
2024-06-11 21:52:26.047 DEBUG tokio-runtime-worker txpool: [BBBB] ValidatedPool::submit_at
2024-06-11 21:52:26.048 DEBUG tokio-runtime-worker txpool: [AAAA] ValidatedPool::submit_at
2024-06-11 21:52:26.047 DEBUG tokio-runtime-worker txpool: [BBBB] Lorem ipsum dol
2024-06-11 21:52:26.048 DEBUG tokio-runtime-worker txpool: [AAAA] Lorem ipsum dol
2024-06-11 21:52:26.047 DEBUG tokio-runtime-worker txpool: [DDDD] Lorem ipsum dol
2024-06-11 21:52:26.047 DEBUG tokio-runtime-worker txpool: [CCCC] Lorem ipsum dol
2024-06-11 21:52:26.604  INFO tokio-runtime-worker sc_basic_authorship::basic_authorship: 🎁 Prepared block for proposing at ...  [DDDD, CCCC, BBBB, AAAA]"
        """
        initial_hash_to_word = {}

        initial_hash_to_word["0x5869…21d2"] = "BBBB"
        initial_hash_to_word["0xf9b6…8cba"] = "AAAA"
        initial_hash_to_word["0x5064…652d"] = "DDDD"
        initial_hash_to_word["0xd441…6960"] = "CCCC"

        modified_content, hash_to_word = replace_hashes(self.content, initial_hash_to_word)
        self.assertEqual(modified_content, expected)



class TestScriptRelayParachain(unittest.TestCase):
    def setUp(self):
        append_word_to_dictionary("RUST")
        append_word_to_dictionary("CORE")
        # Initialize some content and patterns for testing
        self.content = """
2024-06-18 20:26:48.029  INFO tokio-runtime-worker substrate: [Parachain] 🏆 Imported #1409 (0xa226…cbbe → 0x0a62…eefd)
2024-06-18 20:26:54.019  INFO tokio-runtime-worker substrate: [Relaychain] 🏆 Imported #1523 (0x51d5…a879 → 0x5f8e…907e)
2024-06-18 20:26:54.027  INFO tokio-runtime-worker substrate: [Parachain] 🏆 Imported #1410 (0x0a62…eefd → 0xfdec…2cd7)
2024-06-18 20:27:00.019  INFO tokio-runtime-worker substrate: [Relaychain] 🏆 Imported #1524 (0x5f8e…907e → 0xa4d0…495c)
2024-06-18 20:27:00.032  INFO tokio-runtime-worker substrate: [Parachain] 🏆 Imported #1411 (0xfdec…2cd7 → 0x7be2…0f2f)
2024-06-18 20:27:06.017  INFO tokio-runtime-worker substrate: [Relaychain] 🏆 Imported #1525 (0xa4d0…495c → 0xd14a…572a)
2024-06-18 20:27:06.021  INFO tokio-runtime-worker substrate: [Relaychain] 🆕 Imported #1525 (0xa4d0…495c → 0xab85…fd04)
2024-06-18 20:27:06.026  INFO tokio-runtime-worker substrate: [Parachain] 🏆 Imported #1412 (0x7be2…0f2f → 0xf548…b9ae)
2024-06-18 20:27:06.037  INFO tokio-runtime-worker substrate: [Parachain] 🆕 Imported #1412 (0x7be2…0f2f → 0xf04c…9fb6)
2024-06-18 20:27:12.017  INFO tokio-runtime-worker substrate: [Relaychain] 🏆 Imported #1526 (0xd14a…572a → 0x6a67…f503)
        """

    def test_replace(self):
        self.maxDiff = None
        expected = """
2024-06-18 20:26:48.029  INFO tokio-runtime-worker substrate: [Parachain] 🏆 Imported #1409 (CORE → BLOCK1409)
2024-06-18 20:26:54.019  INFO tokio-runtime-worker substrate: [Relaychain] 🏆 Imported #1523 (RUST → RBLOCK1523)
2024-06-18 20:26:54.027  INFO tokio-runtime-worker substrate: [Parachain] 🏆 Imported #1410 (BLOCK1409 → BLOCK1410)
2024-06-18 20:27:00.019  INFO tokio-runtime-worker substrate: [Relaychain] 🏆 Imported #1524 (RBLOCK1523 → RBLOCK1524)
2024-06-18 20:27:00.032  INFO tokio-runtime-worker substrate: [Parachain] 🏆 Imported #1411 (BLOCK1410 → BLOCK1411)
2024-06-18 20:27:06.017  INFO tokio-runtime-worker substrate: [Relaychain] 🏆 Imported #1525 (RBLOCK1524 → RBLOCK1525)
2024-06-18 20:27:06.021  INFO tokio-runtime-worker substrate: [Relaychain] 🆕 Imported #1525 (RBLOCK1524 → RBLOCK1525f01)
2024-06-18 20:27:06.026  INFO tokio-runtime-worker substrate: [Parachain] 🏆 Imported #1412 (BLOCK1411 → BLOCK1412)
2024-06-18 20:27:06.037  INFO tokio-runtime-worker substrate: [Parachain] 🆕 Imported #1412 (BLOCK1411 → BLOCK1412f01)
2024-06-18 20:27:12.017  INFO tokio-runtime-worker substrate: [Relaychain] 🏆 Imported #1526 (RBLOCK1525 → RBLOCK1526)
        """
        modified_content, hash_to_word = replace_hashes(self.content, {})
        self.assertEqual(modified_content, expected)

class TestSpecificReplacement(unittest.TestCase):
    def test_add_specific_replacement(self):
        epattern = r".*Importex #(\d+) \(0x[0-9a-f]{4}…[0-9a-f]{4} → (0x[0-9a-f]{4}…[0-9a-f]{4})\)"
        ereplacement = "XBLOCK"
        eguard = "Importex"
        add_specific_replacement(epattern, ereplacement, eguard)
        (pattern, replacement_prefix, guard)= next(((pattern, replacement_prefix, guard) for (pattern, replacement_prefix, guard) in specific_replacements if guard == "Importex"), None)
        self.assertEqual((epattern, ereplacement, eguard), (pattern, replacement_prefix, guard))
        some_content = """Line 1: The quick brown fox jumps over the lazy dog.
        Line 2: [Relaychain] 🏆 Importex #1234 (0x1234…cdef → 0xabcd…5678)"""
        modified_content, hash_to_word = replace_hashes(some_content, {})
        self.assertIn('XBLOCK1234', modified_content)

if __name__ == '__main__':
    unittest.main()
