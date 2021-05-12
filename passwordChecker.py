import requests,hashlib,sys

def request_api_data(query_char):
    url = 'https://api.pwnedpasswords.com/range/' + query_char
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f'Error fecthing: {res.status_code}, check the API and try again')
    return res

def get_passwords_leaks_counts(hashes, hash_to_check):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h,count in hashes:
        if hash_to_check in h:
            return count
    return 0
        
def pwned_api_check(password):
    #check password if it exists in API response
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5_char,tail = sha1password[:5], sha1password[5:]
    response = request_api_data(first5_char)
    print(f'{first5_char} ----------------- {tail} and the response is: {response}')
    return get_passwords_leaks_counts(response,tail)
    

def main(args):
    for password in args:
        count = pwned_api_check(password)
        if count:
            print(f'{password} was found {count} times. You should probably change your password')
        else:
            print(f'{password} was not found')
    return 'done'
            


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
