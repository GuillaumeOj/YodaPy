[![Travis Status][travis-status]][travis]
[![Mergify Status][mergify-status]][mergify]

[travis]:https://api.travis-ci.com/GuillaumeOj/YodaPy.svg?branch=master&status=failed
[travis-status]:https://api.travis-ci.com/GuillaumeOj/YodaPy.svg?branch=master&status=failed

[mergify]: https://mergify.io
[mergify-status]: https://img.shields.io/endpoint.svg?url=https://gh.mergify.io/badges/GuillaumeOj/YodaPy&style=flat

Online version available here => https://yoda-py.herokuapp.com/

# Contents page
- [I. What is YodaPy?](#i-what-is-yodapy)
- [II. How to install?](#ii-how-to-install)
- [III. How to use?](#iii-how-to-use)
- [IV. To do list](#iv-to-do-list)
- [V. Technologies and ressources](#v-technologies-and-ressources)

# I. What is YodaPy?
[⇧ *Top*](#contents-page)

Luke Skywalker is a young padawan who wants to know anything about the universe. So he asked Yoda each time he wants to know the adress of the [Dernier bar](http://dernierbar.com/).
Yoda answer by giving him the exact adress and a pin on a map. But Yoda is chatty, so he often tell a story about the place.

YodaPy is a project for the Python path from [OpenClassrooms](https://openclassrooms.com/fr/paths/68-developpeur-dapplication-python).

# II. How to install?
[⇧ *Top*](#contents-page)

Clone this current repository on your computer. Run :
```
git clone git@github.com:GuillaumeOj/YodaPy.git
or
git clone https://github.com/GuillaumeOj/YodaPy.git
```

## Virtual environement

### Virtualenv method

Create a virtual environement in your directory:
```
virtualenv -p python3 env
```
or for PowerShell:
```powershell
virtualenv -p $env:python3 env
```

Activate your virtual environement:
```
source env/bin/activate
```
or for PowerShell:
```powershell
.env/scripts/activate.ps1
```

Install `requirements.txt`:
```
pip install -r requirements.txt
```

### Pipenv method

Install the virtual environement by typing:
```
pipenv install
```

Run the virtual environement in the current shell by typing:
```
pipenv shell
```

## .env

For working, the application need a .env file in root with:
```
GEO_TOKEN={type_your_mapbox_token_here}
PUBLIC_GEO_TOKEN={type_your_mapbox_public_token_here}
```

## Run the app

Run the app by typing:
```
flask run
```

Go to `http://127.0.0.1:5000/` and start using the app.

In the future, you just have to run the previous command without the argument

Enjoy the app !

# III. How to use?
[⇧ *Top*](#contents-page)

An online version is available here => https://yoda-py.herokuapp.com/

To use the application it's really simple. Juste ask Yoda to find a place.

/!\ Only work in french /!\

# IV. To do list
[⇧ *Top*](#contents-page)

See my [Trello](https://trello.com/b/P17ksldE/yodapy)

# V. Technologies and ressources
[⇧ *Top*](#contents-page)

This application use various technologies and ressources.

- Main language  => [Python 3.8](https://www.python.org/)
- Framework => [Flask](https://palletsprojects.com/p/flask/)
- Front => [HTML5](https://html.spec.whatwg.org/) / [CSS3](https://www.w3.org/Style/CSS/) / [Vanilla JS](http://vanilla-js.com/)
- HTTP server => [Gunicorn](https://gunicorn.org/)
- Logo => [Icons 8](https://icons8.com/)
- Icons => [Nerd Fonts](https://github.com/ryanoasis/nerd-fonts)
- Map provider => [MapBox](https://www.mapbox.com/)
