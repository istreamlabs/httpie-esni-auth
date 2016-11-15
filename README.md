# ESNI Auth Plugin for HTTPie

An [HTTPie](https://httpie.org/) auth plugin to support ESNI (aka SCTE-224) request signing. This allows you to use the `http` utility to easily make signed requests against a compliant server which checks for request signatures.

## Usage

First, install HTTPie and the plugin:

```sh
# By default on Mac, you'll need to grab `pip` first. This is a one-time task
# you run on a new Mac then immediately forget about!
sudo easy_install pip

# Now install HTTPie and our plugin
sudo pip install httpie httpie-esni-auth
```

Then you can start making requests!

```sh
# Local testing against an example ESNI Service on port 8080
http -A esni -a 'user:pass' post :8080/example/audience/test

# Set an old date header that should fail
http -A esni -a 'user:pass' post :8080/example/audience/test Date:'Mon, 16 Mar 2015 22:32:15 GMT'

# Upload file to a production host
http -A esni -a 'user:pass' post https://example.com/example/audience/test Content-Type:application/xml <audience.xml
```

### Options

In order to see the request going out, use the standard `-v` option to HTTPie. Aside from that, there are some configurable values you can set in environment variables:

Name              | Description
----------------- | -----------
VERBOSE           | Extra output from the signer, if set
ESNI_SCOPE        | Sets the auth scope, default is `esni`
ESNI_SERVICE_NAME | Sets the service name, default is `esni`

Example:

```sh
VERBOSE=1 http -A esni -a 'user:pass' post :8080/...
```

## License

Copyright 2017 iStreamPlanet Co., LLC

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
