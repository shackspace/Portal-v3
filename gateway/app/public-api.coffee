log4js = require 'log4js'
log = log4js.getLogger('public-api');

status = require './status'

config = require '../config'
express = require 'express'
bodyparser = require 'body-parser'
cors = require 'cors'

app = express()
app.use log4js.connectLogger log, { level: log4js.levels.INFO }
app.use cors()

app.get '/status', (req, res) ->
	res.json status.get()

server = app.listen config.publicApiPort, config.publicApiHost, ->
	host = server.address().address
	port = server.address().port

	log.info 'Public API listening at http://%s:%s', host, port
