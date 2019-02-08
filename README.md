# send_joke

Fetch a random joke from https://icanhazdadjoke.com/ and send it to a list of
email addresses through smtp.

## Usage

    $ python -O send_joke.py

## Configuration

Configurations are stored in the `config.yml` file. The fields are:

	server:
	    address:
	    port:
	    user:
	    password:
	joke:
	    url: https://icanhazdadjoke.com/
	    headers:
	        Accept: text/plain
	mail:
	    email:from_user@example.com
	    subject:
	    to:
	        - user@example.com

