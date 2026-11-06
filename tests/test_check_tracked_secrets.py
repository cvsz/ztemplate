"""Filename checks for accidentally tracked secret material."""

import unittest

from scripts.check_tracked_secrets import is_secret_path


class SecretFilenameTest(unittest.TestCase):
    def test_detects_common_secret_names_and_env_variants(self):
        for path in (
            ".env",
            ".env.production",
            "deploy/.env.local",
            "keys/id_rsa",
            "keys/id_ed25519",
            "certs/server.pem",
            "config/private.key",
        ):
            with self.subTest(path=path):
                self.assertTrue(is_secret_path(path))

    def test_allows_documented_environment_example(self):
        self.assertFalse(is_secret_path(".env.example"))
        self.assertFalse(is_secret_path("service/.env.example"))

    def test_ignores_unrelated_names(self):
        for path in ("README.md", "config/example.env", "deploy/env.production"):
            with self.subTest(path=path):
                self.assertFalse(is_secret_path(path))


if __name__ == "__main__":
    unittest.main()
