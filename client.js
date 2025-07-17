const net = require('net');
const readline = require('readline');

const socketFile = '/tmp/socket_file.sock';

const client = new net.Socket();

// リクエストのテンプレート
const request = {
    jsonrpc: '2.0',
    method: "",
    params: [1,2],
    id: 1
};

// ユーザーからの入力処理
function readInput(question) {
    const rl = readline.createInterface({
        input: process.stdin,
        output: process.stdout,
    });

    return new Promise((resolve, reject) => {
        rl.question(question, answer => {
            rl.close();
            resolve(answer);
        });
    });
};



(async function main() {

    method = await readInput('method : ');
    params = await readInput('params : ');
    id = await readInput('id : ');

    request.method = method;
    request.params = params;
    request.id = id;

    console.log(request);

    client.connect(socketFile, () => {
        console.log('connected to server');

        // Javascriptオブジェクトをjson文字列に変換する。
        client.write(JSON.stringify(request));
    });

    client.on('data',(data) => {
        const response = JSON.parse(data);
        
        console.log(request.method, response.result);

        client.end();
    });

    client.on('close', () => {
        console.log('connection closed');
    });
})();