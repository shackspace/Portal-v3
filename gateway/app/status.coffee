# remembers the state

class Status
	constructor: ->
		@_status = 'closed'
		@_nick = ''

	set: (status, nick) =>
		@_status = status
		@_nick = nick

module.exports = new Status()