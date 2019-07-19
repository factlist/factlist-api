const config = require('config');
const request = require('axios');

const getPreviewLink = async url => {
  const api = config.service.embedly.api;
	const key = config.service.embedly.key;
	const response = await request.get(`${api}?key=${key}&url=${url}`);
	return response.data;
};

module.exports = getPreviewLink;
