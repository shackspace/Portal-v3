# remembers the state

class Status
	constructor: ->
		@_status = 'closed'
		@_keyholder = ''

	set: (status, keyholder) =>
		@_status = status
		@_keyholder = keyholder

	get: => {status: @_status, keyholder: @_keyholder}

module.exports = new Status()