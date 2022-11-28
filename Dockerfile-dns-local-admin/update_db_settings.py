#!/usr/bin/env python

import logging
import os

from powerdnsadmin import create_app
from powerdnsadmin.models.setting import Setting
from powerdnsadmin.models.user import User

if __name__ == '__main__':
    app = create_app()
    app.logger.setLevel(logging.INFO)
    with app.app_context():
        Setting().set('pdns_api_url', os.environ.get('ADMIN_PDNS_API_URL', 'http://authoritative:8081/'))
        Setting().set('pdns_api_key', os.environ.get('ADMIN_PDNS_API_KEY', 'pdns'))
        Setting().set('pdns_version', os.environ.get('ADMIN_PDNS_VERSION', '4.2.1'))
        Setting().set('signup_enabled', os.environ.get('ADMIN_SIGNUP_ENABLED', 'no').lower() == 'yes')

        firstname = os.environ.get('ADMIN_USER_FIRSTNAME', 'Administrator')
        lastname = os.environ.get('ADMIN_USER_LASTNAME', 'User')
        password = os.environ.get('ADMIN_USER_PASSWORD', 'admin')
        email = os.environ.get('ADMIN_USER_EMAIL', 'admin@example.org')

        user = User(username='admin', plain_text_password=password, email=email, firstname=firstname, lastname=lastname)
        if not user.create_local_user()['status']:
            user.update_local_user()
