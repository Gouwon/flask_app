#!/bin/sh

alias vstop='deactivate'
source ./flaskr/flaskr_venv/bin/activate
waitress-serve --call 'flaskr:create_app'

