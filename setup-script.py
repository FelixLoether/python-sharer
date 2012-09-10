import argparse
import json
import requests
import urlparse


def step(instructions, func=None, wait=True):
    val = None

    for line in instructions.split('\n'):
        print line.strip()

    if func:
        val = func()

    if wait:
        raw_input('Press enter when you are done.')

    return val


def setup_twitter():
    step(
        '''
        Step 1
        ------
        Create a Twitter app at https://dev.twitter.com/apps/new.
        '''
    )
    step(
        '''
        Step 2
        ------
        Go to the Settings tab and change access under Application Type
        to Read and Write.
        '''
    )
    step(
        '''
        Step 3
        ------
        Go back to the Details tab and click on the Create my Access Token
        button.
        '''
    )
    step(
        '''
        Done!
        -----
        Your application's details tab now has all the required keys:
        - consumer key
        - consumer secret
        - access token
        - access token secret
        ''',
        wait=False
    )


def setup_facebook():
    def get_app_info():
        return (
            raw_input('Enter your app id: '),
            raw_input('Enter your app secret: ')
        )

    def get_code():
        url = raw_input(
            'Enter the URL you were redirected to after granting the '
            'permissions: '
        )
        url = urlparse.urlparse(url)
        query = urlparse.parse_qs(url.query)
        return query['code'][0]

    def exchange_code_for_token():
        response = requests.get(
            'https://graph.facebook.com/oauth/access_token'
            '?client_id=%s'
            '&redirect_uri=http://localhost/'
            '&client_secret=%s'
            '&code=%s' % (
                app_id,
                app_secret,
                code
            )
        )
        if response.status_code != 200:
            print response.content
            raise Exception(response.content)
        data = urlparse.parse_qs(response.content)
        return data['access_token'][0]

    def obtain_long_lived_token():
        response = requests.get(
            'https://graph.facebook.com/oauth/access_token'
            '?client_id=%s'
            '&client_secret=%s'
            '&grant_type=fb_exchange_token'
            '&fb_exchange_token=%s' % (
                app_id,
                app_secret,
                access_token
            )
        )
        if response.status_code != 200:
            print response.content
            raise Exception(response.content)
        data = urlparse.parse_qs(response.content)
        return data['access_token'][0]

    def fetch_page_access_token():
        response = requests.get(
            'https://graph.facebook.com/me/accounts?access_token=%s'
            % access_token
        )
        if response.status_code != 200:
            print response.content
            raise Exception(response.content)
        data = json.loads(response.content)
        for page in data['data']:
            if page['id'] == page_id:
                return page['access_token']

    step(
        '''
        Step 1
        ------
        Create a Facebook app at https://developers.facebook.com/apps.
        Make the app domain http://localhost/.
        Select Website with Facebook Login.
        Enter http://localhost/ as the site URL.
        '''
    )
    step(
        '''
        Step 2
        ------
        Create a Facebook Page at https://www.facebook.com/pages/create.php.
        '''
    )
    app_id, app_secret = step(
        '''
        Step 3
        ------
        ''',
        func=get_app_info,
        wait=False
    )
    url = (
        'https://www.facebook.com/dialog/oauth'
        '?client_id=%s'
        '&redirect_uri=http://localhost/'
        '&scope=manage_pages,publish_stream'
        '&state=ieo4wft' % app_id
    )
    step(
        '''
        Step 4
        ------
        Go to %s
        ''' % url
    )
    code = step(
        '''
        Step 5
        ------
        ''',
        func=get_code,
        wait=False
    )
    access_token = step(
        '''
        Step 6
        ------
        Exchanging code for access token...
        ''',
        func=exchange_code_for_token,
        wait=False
    )
    access_token = step(
        '''
        Step 7
        ------
        Obtaining long-lived access token...
        ''',
        func=obtain_long_lived_token,
        wait=False
    )
    page_id = step(
        '''
        Step 8
        ------
        ''',
        func=lambda: raw_input('Enter page id: '),
        wait=False
    )
    page_access_token = step(
        '''
        Step 9
        ------
        Fetching page access token...
        ''',
        func=fetch_page_access_token,
        wait=False
    )
    step(
        '''
        Done!
        -----
        Here is the information you need:
        - page id: %s
        - page access token: %s
        '''
        % (
            page_id,
            page_access_token
        ),
        wait=False
    )


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Get required keys for python-sharer'
    )
    parser.add_argument(
        'sharer',
        choices=[
            'twitter',
            'facebook',
        ],
        help='The service you want to get keys for.'
    )
    args = parser.parse_args()

    funcs = {
        'twitter': setup_twitter,
        'facebook': setup_facebook,
    }
    funcs[args.sharer]()
