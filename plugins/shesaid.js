var twss = require('twss');


var argument = process.argv.splice(2)[0];
var shesaid = twss.is(argument);

console.log(shesaid);
