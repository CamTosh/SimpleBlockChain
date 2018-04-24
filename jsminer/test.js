const http = require('http');
const crypto = require('crypto');
const random = require("random-js");

const rand = (() => {
	return Math.floor(Math.random() * Math.floor(1));
})

const hashToStr = ((data) => {
	return crypto.createHash('sha256').update(data.toString()).digest("hex");
})

const submitWork = ((work) => {

	const options = {
	  hostname: 'localhost',
	  port: 1337,
	  path: '/work',
	  method: 'POST',
	  headers: {
	    'Content-Type': 'application/json',
	  }
	};

	const req = http.request(options, (res) => {
	  res.on('data', (chunk) => {
	    console.log(`BODY: ${chunk}`);
	  });
	});

	req.write(JSON.stringify(work));
	req.end();
})

const doWork = ((lastBlock, timestamp, pool, nonce, difficulty, string_difficulty, minerate) => {
	while (hashToStr(lastBlock + timestamp + pool + nonce).substr(0, difficulty) != string_difficulty) {
		let time = new Date()

		if (rand() <= minerate) {
			nonce += 1
			console.log(nonce, "Hashrate: ", Math.abs(new Date() - time), "mh/s")
		}
	}
	let work = {
		"last_block": lastBlock,
		"nonce": nonce,
		"pool": pool,
		"timestamp": timestamp ,
		"difficulty": difficulty,
		"minerate": minerate,
	}
	console.log("Block Found: ", work.nonce)

	return work
})

http.get("http://localhost:1337/work", res => {
	res.setEncoding("utf8");
	let work = "";
	res.on("data", data => {
		work += data;
	});
	res.on("end", () => {
		work = JSON.parse(work)
		var result = doWork(work.last_block, work.timestamp, work.pool, work.nonce, work.difficulty, work.string_difficulty, work.minerate)
		
		var newWork = {
			last_block: result.last_block,
			nonce: result.nonce,
			pool: result.pool,
			timestamp: result.timestamp,
			difficulty: result.difficulty,
			minerate: result.minerate,
		}

		submitWork(result)

	});
});
