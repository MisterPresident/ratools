import getpass
from pathlib import Path

import requests
from keepassxc_browser import Connection, Identity
from tqdm import tqdm


def get_credentials(url, client_id='python-keepassxc-browser', state_file='.assoc'):
    state_file = Path(state_file)
    if state_file.exists():
        with state_file.open('r') as f:
            data = f.read()
        id = Identity.unserialize(client_id, data)
    else:
        id = Identity(client_id)

    c = Connection()
    c.connect()
    c.change_public_keys(id)

    if not c.test_associate(id):
        print('Not associated yet, associating now...')
        assert c.associate(id)
        data = id.serialize()
        with state_file.open('w') as f:
            f.write(data)
        del data

    try:
        l = c.get_logins(id, url=url)
        user = l[0]["login"]
        password = l[0]["password"]
    except:
        user = input("Username:")
        password = getpass.getpass()

    c.disconnect()
    return (user, password)


def get_requests_session():
    s = requests.Session()
    agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"
    s.headers.update({"user-agent": agent})
    return s


def list_index_selector(list, question="Please select an index. "):
    l = len(list)
    if l == 0:
        return None
    l_str = len(str(l))
    for i in range(l):
        str_format = "[{:" + str(l_str) + "d}] {}"
        print(str_format.format(i + 1, list[i]))

    while True:
        index = input(question + "1-" + str(l))
        try:
            index = int(index)
            if index < 1 or index > l:
                raise Exception()
            return index - 1
        except Exception:
            print("Invalid Input")


def download(response, out_file):
    total_size_in_bytes = int(response.headers.get('content-length', 0))
    block_size = 2 ** 12
    progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
    with open(out_file, 'wb') as file:
        for data in response.iter_content(block_size):
            progress_bar.update(len(data))
            file.write(data)
    progress_bar.close()
    if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
        print("ERROR, something went wrong")
