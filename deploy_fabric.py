import os
import requests

def get_access_token():
    url = f"https://login.microsoftonline.com/{os.environ['AZURE_TENANT_ID']}/oauth2/v2.0/token"
    payload = {
        'grant_type': 'client_credentials',
        'client_id': os.environ['AZURE_CLIENT_ID'],
        'client_secret': os.environ['AZURE_CLIENT_SECRET'],
        'scope': 'https://graph.microsoft.com/.default'
    }
    r = requests.post(url, data=payload)
    return r.json()['access_token']

def deploy_to_workspace(workspace_id, token):
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    # Example: deploy a Lakehouse or Report (you’ll need to customize this)
    url = f'https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/artifacts'
    payload = {
        "sourcePath": "./Fabric_item",
        "overwrite": True
    }
    r = requests.post(url, headers=headers, json=payload)
    print(f"Deploy to workspace {workspace_id}: {r.status_code} - {r.text}")

if __name__ == "__main__":
    token = get_access_token()
    deploy_to_workspace(os.environ['FABRIC_WORKSPACE_UAT'], token)

    if os.environ.get('DEPLOY_TO_PRO') == 'true':
        deploy_to_workspace(os.environ['FABRIC_WORKSPACE_PRO'], token)
