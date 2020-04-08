from config import Config


class TestConfig:
    def test_logo_exist(self):
        logo = Config.LOGO
        assert logo

    def test_catchphrase_exist(self):
        catchphrase = Config.CATCHPHRASE
        assert catchphrase

    def test_author_exist(self):
        author = Config.AUTHOR
        assert author

    def test_social_links_exist(self):
        social_links = Config.SOCIAL_LINKS
        assert social_links
