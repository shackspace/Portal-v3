log4js = require 'log4js'
log = log4js.getLogger('portal-api');

status = require './status'

config = require '../config'
express = require 'express'
bodyparser = require 'body-parser'

app = express()
app.use log4js.connectLogger log, { level: log4js.levels.INFO }
app.use(bodyparser.json())

mqtt = require 'mqtt'
mq = mqtt.connect 'mqtt://mqtt.shack', { will: { topic: 'portal/gateway/status', payload: 'offline', retain: true } } 

mq.on 'connect', () ->
  mq.publish 'portal/gateway/lwt','online', { retain: true }

app.post '/push', (req, res) ->
	if req.body?.status?
		log.info 'portal reports', req.body.status
		if req.body.status in ['open', 'closed']
			status.set req.body.status, req.body.keyholder
			mq.publish 'portal/gateway/status',req.body.status, { retain: true }
			mq.publish 'portal/gateway/keyholder',req.body.keyholder, { retain: true }
		else
			log.warn 'invalid status:', req.body.status
	res.end()

server = app.listen config.portalApiPort, config.portalApiHost, ->
	host = server.address().address
	port = server.address().port

	log.info 'Portal API listening at http://%s:%s', host, port
