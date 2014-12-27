var express = require('express');
var router = express.Router();
var bodyParser = require('body-parser');

router.use(bodyParser.json());

router.use('/register', function(req, res, next) {
	if (req.ip == '127.0.0.1') {
		res.send("hello register")
	}
	else {
		res.status(403).end()
	}

});

router.post('/login', function(req, res) {
	console.log('The req is:' + JSON.stringify(req.body))
	res.status(200).end()
});

/* GET users listing. */
router.get('/', function(req, res) {
  res.send('respond with a resource');
});

module.exports = router;
