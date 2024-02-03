const acorn = require("acorn")

process.stdin.setEncoding('utf-8');

getStdin().then(input => {

    // the important part
    const parsedObj = acorn.parse(input, {ecmaVersion: 2020});
    const json = JSON.stringify(parsedObj);
    console.log(json);

}).catch(err => {
    console.error('Error:', err);
});

function getStdin() {
    return new Promise((resolve, reject) => {
        if (process.stdin.isTTY) {
            console.error('This program requires input to be piped to it.');
            process.exit(1);
        }
        let data = '';
        process.stdin.on('data', chunk => {
            data += chunk;
        });
        process.stdin.on('end', () => {
            resolve(data);
        });
        process.stdin.on('error', err => {
            reject(err);
        });
    });
}