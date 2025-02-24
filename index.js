const { createServer } = require('node:http');
const hostname = '127.0.0.1';
const port = 5433;

//Create Server
const server = createServer((req, res) => {
  res.statusCode = 200;
  res.setHeader('Content-Type', 'text/plain');
  res.end('Hello World');
});

//Server is listening to port 5433
server.listen(port, hostname, () => {
  console.log(`Server running at http://${hostname}:${port}/`);
});