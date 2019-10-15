# send_joke

Fetch a random joke from a url as plain text and send it to a list of email
addresses through smtp.

## Usage

    $ python -O send_joke.py

## Configuration

Configurations are stored in the `config.json` file. The fields are:

    mail_server {
        address : string : the smtp server to use to send mail
        port : integer : the smtp port
        username : string : the login username
        password : string : the login password
    },
    joke_server {
        url : string : the address to fech a plain text joke
        headers : object : the http headers to send with the GET request
    },
    from_address : string : the email address that will appear as the sender
    subject_line : string : the subject line of the email


Some example headers would be:

    Accept: text/plian
    Accept-Charset: utf-8
    

The mailing list is stored in a plain text file `mail_list.txt` with one email
address per line.

## A list of recommended servers:

### https://icanhazdadjoke.com/

Note the web api documentation requests users to provide a custom `User-Agent`
string with the name and url/email of the user or application. This can be
provided as an entry in the `joke_server.headers` object.
