api-wrapper-helper
==================

[![Build Status](https://travis-ci.org/naiyt/api-wrapper-helper.svg)](https://travis-ci.org/naiyt/api-wrapper-helper)

Essentially just a `requests` wrapper used to make creating API wrappers a bit simpler. As is, it doesn't give you that much over just using `requests`, though (and I should probably write it to inherit from requests instead, so that you get access to all of the `requests` methods directly if needed). Adding OAuth support in directly could make things helpful, I think.

Example:

	from apihelper import Api
	token = 'Your Github access token'
	github_api = Api('https://api.github.com', headers= {
		'Authorization': 'token {}'.format(token)}
	)
	print(github_api.get('/user').json())
Test