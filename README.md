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

# Find the enterprise app id 
az ad sp list --display-name "<app reg name>" --query "[].appId" --output tsv

# Add your admin user as owner to the enterprise app
az ad sp owner add --id <enterprise app id> --owner_object_id <admin user id>
````

