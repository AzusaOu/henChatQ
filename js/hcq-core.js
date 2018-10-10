var CLIENT_VER = '181010-Beta';

var DEFAULT_SERVER = 'ws://localhost:43210';

var ws;		// Websocket

var listeningOn = {};

var user;

newSession(DEFAULT_SERVER);

// ==============================
// online = true: online mode
// online = false: offline mode
// ==============================
function formStatusSet(online) {
	$('#btn_encrypt').prop('disabled', true);
	$('#fileSelector').prop('disabled', true);
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
			console.log(`Server host: ${getMsg.server}`);
			chListening = getMsg.chs
			user = getMsg.user;
			// console.log(chListening)
			for (ch in chListening) {
				ch_p = b64DecodeUnicode(ch);
				$('#channels').append(ui_channel(ch_p, chListening[ch]));
				$('#sl_to').append(`<option value="${ch}" selected>${ch_p}</option>`);
			}
		}

		else if (getMsg.type === 0x01 && (getMsg.ch in listeningOn)) {
			showMsg(getMsg);
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
		// var now = new Date(parseInt(msg.time));
		var now = new Date();
		// -- Text message
	
		if (msg.from === user) {
			// console.log('Self msg');
			showText = ui_msgPop(
				b64DecodeUnicode(msg.ch),
				xssAvoid(msg.from),
				now.toString(),
				xssAvoid(b64DecodeUnicode(msg.msg)),
				msg.verified,
				msg.timeCheck,
				'#efefef'
			);
		} else {
			showText = ui_msgPop(
				b64DecodeUnicode(msg.ch),
				xssAvoid(msg.from),
				now.toString(),
				xssAvoid(b64DecodeUnicode(msg.msg)),
				msg.verified,
				msg.timeCheck
			);
		}
		log.prepend(showText);

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


// // ================================================================
// // Check the extension of selected file. Available extensions are 
// // defined on the head
// // ================================================================
// function fileExtCheck(fileInputLable, extNames) {
			
// 	var fname = fileInputLable.value;
// 	if (!fname) {
// 		return false
// 	}
// 	var fext = fname.slice(-4).toLowerCase();
// 	if (extNames.indexOf(fext) != -1) {
// 		return true;
// 	} else {
// 		return false;
// 	}
// }

// ===== Init ======================================
formStatusSet(false);
// $('#s_pvk').val(getCookie('pvk'));
var fileSelector = document.getElementById('fileSelector');
// =================================================
