
console.log('api.ts running');

interface Range {
    start: number;
    end: number;
}

interface Token {
    type: string;
    text: string;
    match: Range;
}

export type Data = Array<Token>
export type DataHandler = (object: Data) => void

export const post = (url: string) => {
    fetch('https://httpbin.org/post', {
        method: 'post',
        headers: {
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ a: 7, str: 'Some string: &=&' })
    }).then(res => res.json())
        .then(res => console.log(res));
};

export const get = (url: string, cb: DataHandler) => {
    fetch(url, {
        method: 'get',
        headers: {
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/json'
        },
    }).then(res => res.json())
        .then(res => {
            cb(res);
        });
};