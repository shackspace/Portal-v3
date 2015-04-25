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
		if req.body.status in ['open', 'closed']
			status.set req.body.status, req.body.nick
		else
			log.warn 'invalid status:', req.body.status
	res.end()

server = app.listen config.portalApiPort, config.portalApiHost, ->
	host = server.address().address
	port = server.address().port

	log.info 'Example app listening at http://%s:%s', host, port
