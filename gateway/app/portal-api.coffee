log4js = require 'log4js'
log = log4js.getLogger('portal-api');

status = require './status'

config = require '../config'
express = require 'express'
bodyparser = require 'body-parser'

app = express()
app.use log4js.connectLogger log, { level: log4js.levels.INFO }
app.use(bodyparser.json())

app.post '/push', (req, res) ->
	if req.body?.status?
		log.info 'portal reports', req.body.status
		if req.body.status is 'open'
			status.set 'open', req.body.keyholder
		if req.body.status is 'closed'
			status.set 'closed'
		else
			log.warn 'invalid status:', req.body.status
	res.end()

server = app.listen config.portalApiPort, config.portalApiHost, ->
	host = server.address().address
	port = server.address().port

	log.info 'Portal API listening at http://%s:%s', host, port
