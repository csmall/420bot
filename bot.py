
import time

from mastodon import Mastodon
from four_twenty import FourTwenty

BOT_NAME='testbot'
BASE_URL='https://social.dropbear.xyz'

import sys

def parse_args():
    import argparse

    parser = argparse.ArgumentParser(description="420 bot.")
    parser.add_argument('--register', nargs=2, metavar=('login', 'password'))

    return parser.parse_args()


def register(args, clientcred_file, usercred_file):
    Mastodon.create_app(BOT_NAME, to_file=clientcred_file,
            api_base_url=BASE_URL)

    mastodon = Mastodon(
            client_id = clientcred_file,
            api_base_url = BASE_URL)

    (login, password) = args.register
    try:
        mastodon.log_in( login, password,
                to_file = usercred_file)
    except Exception as login_err:
        print('Unable to login new bot: {0}'.format(login_err))

    print('Bot is registered successfully')

def run_bot(mastodon):
    four_twenty = FourTwenty()
    four_twenty.autofill_offsets()

    mastodon.toot('Hey, I\'m awake again!')
    while True:
        wait_time = four_twenty.wait_time()
        next_offset = four_twenty.next_offset()
        print('Sleeping for {0} seconds...'.format(wait_time))
        time.sleep(wait_time)
        message = 'It is now 4:20pm in {0}!\n#420'.\
                format(', '.join(four_twenty.timezones(next_offset)))
        print(message)
        mastodon.toot(message)

def main():
    clientcred_file=BOT_NAME+'_clientcred.secret'
    usercred_file=BOT_NAME+'_usercred.secret'

    args = parse_args()

    if args.register:
        register(args, clientcred_file, usercred_file)
        sys.exit(0)

    mastodon = Mastodon(
            client_id = clientcred_file,
            access_token = usercred_file,
            api_base_url = BASE_URL)

    instance = mastodon.instance()
    print('Successfully logged into instance "{0}".'.format(instance.title))
    run_bot(mastodon)

if __name__ == '__main__':
    main()
