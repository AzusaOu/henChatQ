var CLIENT_VER = '180818';

var DEFAULT_SERVER = 'ws://localhost:43210';

var ws;		// Websocket

newSession(DEFAULT_SERVER)

function getCookie(key) {
	var arr, reg = new RegExp("(^| )"+key+"=([^;]*)(;|$)");
	if (arr = document.cookie.match(reg)) {
		return unescape(arr[2]);
	} else {
		return null;
	}
}

function randomStr(length, symbol=true) {
	var gen = '';
	if (symbol) {
		var charLib = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!#$%&*?@~-';
	} else {
		var charLib = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ';
	}
	
	for (var i=0; i<length; i++) {
		index = Math.round(Math.random() * (charLib.length - 1));
		gen += charLib[index];
	}
	return gen;
}

// ==============================
// online = true: online mode
// online = false: offline mode
// ==============================
function formStatusSet(online) {
	$('#s_pvk').prop('disabled', online);
	$('#s_pbk').prop('disabled', true);
	// $('#s_to').prop('disabled', !online);
	$('#s_send').prop('disabled', !online);
	$('#btn_auto').prop('disabled', online);
	$('#btn_enter').prop('disabled', online);
	$('#btn_encrypt').prop('disabled', !online);
	$('#btn_close').prop('disabled', !online);
	$('#btn_send').prop('disabled', !online);
	$('#fileSelector').prop('disabled', !online);
}
// ===========================================


// ================================================================
// Create a new websocket server, including all events:
// ws.onopen()
// ws.onmessage()
// ws.onclose()
// ws.onerror()
// ================================================================
function newSession(server) {

	// -- Connect to Web Socket
	ws = new WebSocket(server);

	// -- Set event handlers
	ws.onopen = function() {
		showMsg(`Server opened. Client ver: ${CLIENT_VER}`);
		// document.cookie = `server=${$('#s_server').val()}`;
		document.cookie = `pvk=${$('#s_pvk').val()}`;
		var now = new Date();

		// -- Send login request
		loginInfo = {
			type: 0x00,
		}
		ws.send(JSON.stringify(loginInfo));
	};
		
	ws.onmessage = function(e) {
		// -- e.data contains received string.
		var getMsg = JSON.parse(e.data);
		// console.log(getMsg);

		// -- Server reply "login"
		if (getMsg.type === 0x00) {
			console.log(`Server ver: ${getMsg.msg}`);
		}

		else if (getMsg.type === 0x01) {
			showMsg(`${getMsg.msg}.`);
		}
	};

	ws.onclose = function() {
		showMsg("Server closed.");
		formStatusSet(false);
		encryptMode = false;
		publicKeyCache = '@';
	};

	ws.onerror = function(e) {
		showMsg("Server error.", "red");
		formStatusSet(false);
	};
}


// ================================================================
// Output something in log region. There are 2 typical situations:
// 1. msg is plain text: text will be shown directly;
// 2. msg is json object: text will be handled first.
// And encrypt mode status can influence the handling process.
// ================================================================
function showMsg(msg, color="black") {
	// msg here is in struct of json

	// ===============================
	// Search "XSS attack" for detail
	// ===============================
	function xssAvoid(rawStr){
		return rawStr.replace(/</g, '&lt').replace(/>/g, '&gt');
	}

	var log = $('#log');
	var notice = true;

	if (typeof(msg) === 'object') {
		var now = new Date(parseInt(msg.time));
		strFrom = (function () {
			if (msg.from.indexOf('->') === -1) {
				return `<a href="javascript:addReceiverFromSession('${msg.from}')">${msg.from}</a>`;
			} else {
				return msg.from;
			}
		})();

		// -- Not in encrypt mode or the message is from the user
		if (encryptMode === false || color === 'green') {
			var strHead = `${now.toString()}<br>[${strFrom}]<br>`;
			showText = `${strHead}<font color="${color}">${xssAvoid(msg.msg).split('\n').join('<br>')}</font><br>`;
		
		// -- In encrypt mode
		} else {
			var strHead = `${now.toString()}<br>[🔒${msg.from}]<br>`;
			showText = `${strHead}<font color="${color}">${xssAvoid(rsaDecrypt(msg.msg, selfPrivateKey)).split('\n').join('<br>')}</font><br>`;
		}

		// -- Message with image
		if (msg['img'] != undefined) {

			// -- Whole file (without spliting)
			if (msg['rest'] === undefined) {

				if (encryptMode === false || color === 'green') {
					showText += `<img src="${msg.img}" width="200"><br>`;
				} else {
					showText += `<img src="${rsaDecrypt(msg.img, selfPrivateKey, true)}" width="200"><br>`;
				}
				showText += '<br>';
				log.prepend(showText);

			// -- Sliced file
			} else {

				if (buffer[msg.sign] == undefined) {
					showMsg(`Receiving an image from<br>${msg.from}<br><progress id="${msg.sign}" value="${msg.size[0]/msg.size[1]}">0%</progress>`, 'gray');
					buffer[msg.sign] = rsaDecrypt(msg.img, selfPrivateKey, encryptMode);
				} else {
					buffer[msg.sign] += rsaDecrypt(msg.img, selfPrivateKey, encryptMode);
					$(`#${msg.sign}`).val(msg.size[0]/msg.size[1]);
					notice = false;
				}

				// -- Transfer finished
				if (msg['rest'] <= 0) {
					showText += `<img src="${buffer[msg.sign]}" width="200"><br>`;
					showText += '<br>';
					log.prepend(showText);
					delete(buffer[msg.sign]);					// Clean buffer
				}
			}

		// -- Text message
		} else {
			showText += '<br>';
			log.prepend(showText);
		}

		// -- Show the notification
		if(document.hidden && Notification.permission === "granted" && notice) {
			var notification = new Notification('henChat', {
				body: 'New message comes!',
			});

			notification.onclick = function() {
				window.focus();
			};
		}

	// -- msg is plain text
	} else {
		log.prepend(`<font color="${color}">${msg}<br><br></font>`);
	}
}


// ================================================================
// Check the extension of selected file. Available extensions are 
// defined on the head
// ================================================================
function fileExtCheck(fileInputLable, extNames) {
			
	var fname = fileInputLable.value;
	if (!fname) {
		return false
	}
	var fext = fname.slice(-4).toLowerCase();
	if (extNames.indexOf(fext) != -1) {
		return true;
	} else {
		return false;
	}
}

// ===== Init ======================================
formStatusSet(false);
$('#s_pvk').val(getCookie('pvk'));
var fileSelector = document.getElementById('fileSelector');
// =================================================
