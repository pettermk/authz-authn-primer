# author-authn-primer
This is a primer on learning different authentication and authorization scenarios
when building web apps that connect to Azure AD.

# Prerequisites
## On your machine
To carry out all operations gone through in this workshop, we need to install the following
software.

- Docker desktop: Install from company portal
- Ubuntu (or other linux) from app store. Follow [this](https://learn.microsoft.com/en-us/windows/wsl/setup/environment)
- Azure cli: Follow [this](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli-linux?pivots=apt)

## Application registration and enterprise application in Entra ID
To obtain an application registration, fill out the form in ServiceNow. It is located at 

> ServiceNow -> Request catalog -> Azure AD - application registration

| Field | Value |
| ----- | ----- |
| New or existing application | New |
| App registration name | Name of app or use case |
| App owners | Entra ID users who will own the app |
| Justification | Elaborate on app or use case |
| Application type information | My own Azure developed application |
| Certificates and/or secret configuration | Yes |

The other fields can be left as default. After a day or two you should have the app reg and 
enterprise application set up for you, with a client secret sent to your email.


## Change app reg and enterprise application owner

The form only allows us to select regular users, while application registration should only
be owner by admin users. Let's fix this.

```bash
# Find the app reg id 
az ad app list --display-name "<app reg name>" --query "[].appId" --output tsv

# Find your admin user ID
az ad user show --id admin.<user name>@akerbp.com --query id --output tsv

# Add your admin user as owner to the app reg
az ad app owner add --id <app reg id> --owner-object-id <admin user id>

````

Attempts to do the final step of assigning the correct owner to the enterprise application
have failed. There is no Azure CLI command to do this, and using the graph API fails in 
mysterious ways.

A ticket to IT help is currently the only way to do this.

# Verify app works without authentication
## Setup environment file 
To successfully run the app, a few environment variables need to be in place. These are the 
client ID, client secret and a cookie secret. To start filling these out, copy the template
to a real `.env` file

```bash
cp .env-template .env
```

### Create cookie secret
All cookies are encrypted using a secret key. To prevent the possibility of reading and tampering
with the cookie, this secret needs to be unique. There are several ways to do so and they are 
documented [here](https://oauth2-proxy.github.io/oauth2-proxy/configuration/overview/#generating-a-cookie-secret).
One easy way is to type in the terminal

```bash
dd if=/dev/urandom bs=32 count=1 2>/dev/null | base64 | tr -d -- '\n' | tr -- '+/' '-_' ; echo
```

Then the resulting string can be put into the `.env` file.

### Oauth2 properties
The app we requested earlier came with a client secret, it should be sent to you by email. The 
client ID can be found using the Azure CLI,

```bash
az ad app list --display-name <app-registration-name> --query "[].appId" --output tsv
```

Now type those values into their respective variables in the `.env` file.

### Run the app

Now that we have filled out our environment file, we can run the application. To run the application 
and verify that your local development environment is correctly set up, run 

```bash
docker-compose up
```

The app is now running, and visiting `http://localhost:8080/public` should result in the application being 
visible. This endpoint is configured in the oauth2-proxy configuration to not require authentication, using 
the `skip_auth_routes` configuration.

## Setting up routes using authentication
### Try it
The webapp has an endpoint called `http://localhost:8080/behind_proxy`, and it requires authentication.
Try visiting this page.

This should result in an error. The reason is that we have not configured a _callback URL_ yet.

### The callback URL

To understand the callback URL, lets rewind a few steps and learn some of the key elements of how
the authentication proxy works.

When hitting our protected endpoint, the oauth2-proxy roughly follows the following sequence, depending
on whether or not the user is already authenticated.

```mermaid
sequenceDiagram
    actor User
    box purple Application
    participant AuthenticationProxy
    participant App
    end
    box yellow Identity provider
    participant EntraID
    end
    

    User->>AuthenticationProxy: Request
    alt Authenticated
    AuthenticationProxy->> App: You are authenticated
    App->> User: Application served
    end
    alt Not authenticated
    AuthenticationProxy->> EntraID: You are not authenticated, redirect
    EntraID->> AuthenticationProxy: Authentication complete, callback
    AuthenticationProxy->> App: You are authenticated
    App->> User: Application served
    end
```

In the sequence where the user is not authenticated, they are redirected to the identity provider,
and once the user is authenticated they will be issed a set of credentials proving who they are 
(ID token) and what accesses they have (Access token). These credentials are passed to what we 
designate as the _redirect URL_, or _callback URL_ as it is often also called.

Entra ID will only be permitted to pass the credentials to a predefined set of URLs. In our case, 
our authentication proxy is running on `http://localhost:8080` and this URL needs to be added to 
the set of permitted redirect URIs.


