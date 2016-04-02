# remembers the state

class Status
	constructor: ->
		@_status = 'closed'
		@_keyholder = ''
		@_timestamp = Date.now()

	set: (status, keyholder) =>
		@_status = status
		@_keyholder = keyholder
		@_timestamp = Date.now()

	get: => {status: @_status, keyholder: @_keyholder, timestamp: @_timestamp}

module.exports = new Status()
