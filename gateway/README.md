# Portal Gateway

VM to reduce load on the portal hardware.

The portal pushes it's status to the gateway as http every x seconds or on special events.
The gateway has two NICs, one reachable by the portal, the other to the rest of the network.
On the first NIC the gateway provides a http api for the portal to push its status to.
On the second NIC the gateway provides a http api for querying the status of the portal.


## Portal-facing API

POST /push
{
	status: 'closed' or 'open',
	keyholder: nickname
}

### curl example

curl -XPOST -d '{"status":"open", "keyholder": "root"}' -H "Content-type: application/json" 'http://10.42.irgendwas:8088/push'

## Public-facing API

GET /status (from inside):

curl "http://portal.shack:8088/status" 

returns
{
	status: 'closed' or 'open',
	keyholder: nickname
}

## Installation

- Install node
- `npm install` in this directory
- copy config.coffee.dist to config.coffee and edit accordingly

## Execution

`npm start`
