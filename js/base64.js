// https://blog.csdn.net/xieamy/article/details/78846732
// All the "=" are transformed to "_"

function b64EncodeUnicode(str) {
    return (btoa(encodeURIComponent(str).replace(/%([0-9A-F]{2})/g, function(match, p1) {
            return (String.fromCharCode('0x' + p1));
        }))).replace(/=/g, '_');
}

function b64DecodeUnicode(str) {
	str = str.replace(/_/g, '=');
    return decodeURIComponent(atob(str).split('').map(function(c) {
        return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
    }).join(''));
}