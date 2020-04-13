import os

current_dir = os.path.abspath(os.path.dirname(__file__))


class Config:
    LOGO = 'https://img.icons8.com/color/130/000000/baby-yoda.png'
    BOT_NAME = 'YodaPy'
    CATCHPHRASE = 'Sur YodaPy le bienvenue tu es !'
    AUTHOR = 'Guillaume OJARDIAS'

    # To find out which class to use for social links, please see the link below
    # https://www.nerdfonts.com/cheat-sheet
    SOCIAL_LINKS = [
        {
            'profile': True,
            'url': 'https://www.linkedin.com/in/guillaume-ojardias-91a46643/',
            'class': 'nf-fa-linkedin_square',
        },
        {
            'profile': False,
            'url': 'https://github.com/GuillaumeOj',
            'class': 'nf-fa-github',
        },
        {
            'profile': False,
            'url': 'https://twitter.com/GuillaumeOj',
            'class': 'nf-fa-twitter_square',
        },
    ]
    PROFILE_LINK = next(link['url'] for link in SOCIAL_LINKS if link['profile'])

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'This-is-my-secret-key'
