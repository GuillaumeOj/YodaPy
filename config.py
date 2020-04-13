import os

current_dir = os.path.abspath(os.path.dirname(__file__))


class Config:
    LOGO = 'https://img.icons8.com/color/150/000000/baby-yoda.png'
    CATCHPHRASE = 'Sur YodaPy le bienvenue tu es !'
    AUTHOR = 'Guillaume OJARDIAS'
    SOCIAL_LINKS = [
        {'name': 'Linkedin',
         'url': 'https://www.linkedin.com/in/guillaume-ojardias-91a46643/'},
        {'name': 'Github',
         'url': 'https://github.com/GuillaumeOj'}
    ]
    PROFILE_LINK = next(link['url'] for link in SOCIAL_LINKS
                        if link['name'] == 'Linkedin')

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'This-is-my-secret-key'
