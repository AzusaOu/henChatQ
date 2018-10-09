// ===== Button Events =============================

// // -- Click "ETE"
// $('#btn_encrypt').click(function () {

// 	var receiver = '';
// 	for (c of contacts) {
// 		if ($(`#${c}`).prop('checked')) {
// 			receiver = c;
// 		}
// 	}
// 	if (receiver === '') {
// 		alert('There is no receiver in the list...');
// 		return -1;
// 	}

// 	$('#s_to').prop('disabled', true);					// Forbid multi-receiver
// 	$('#btn_encrypt').prop('disabled', true);			// Forbid ETE button
// 	$('#btn_send').prop('disabled', true);				// Temporary block ETE button
// 	$(`#${receiver}`).prop('checked', true);						// Fix receiver as the 1st receiver
// 	$(`#${receiver}`).prop('disabled', true);

// 	var now = new Date();
// 	var keyExchangeRequest = {
// 		from: $('#s_pbk').val(),
// 		to: [receiver],
// 		type: 'msg',
// 		msg: selfPublicKey,
// 		key: 'true',
// 		token: sToken,
// 		time: now.getTime().toString()
// 	}

// 	ws.send(JSON.stringify(keyExchangeRequest));
// 	while (publicKeyCache != '@');						// Wait for public key from receiver
// 	$('#btn_send').prop('disabled', false);				// Send button recovery

// 	encryptMode = true;
// });


// -- Click "Send"
$('#btn_send').click(function () {
	var ch = b64EncodeUnicode($('#sl_to').val());
	var msg = b64EncodeUnicode($('#s_send').val());
	var cmd = {
		'type': 0x02,
		'ch': ch,
		'stype': '-t',
		'msg': msg,
		'psk': 'henChatQ',
		'qos': 0
	};
	ws.send(JSON.stringify(cmd));
});
			 
// ===== Key Events ===============================

// -- Press "Ctrl+Enter" to send
prevKey = '';
document.onkeydown = function (e) {
	if (e.key === 'Enter' && prevKey === 'Control') {
		$('#btn_send').click();
	}
	if (e.key != prevKey) {
		prevKey = e.key;
	}
}

// ===== Add Contacts ===============================
function addChannel() {
	var newChannel = $('#s_newChannel').val();
	if (newChannel === '') {
		return -1;
	}
	$('#receiverChoice').prepend(`<input type="checkbox" id="${newChannel}" checked="checked"/>${newChannel}<br>`);
	$('#s_newChannel').val('');
	var cmd = {
		'type': 0x03,
		'ch': b64EncodeUnicode(newChannel),
		'psk': b64EncodeUnicode($('#s_psk').val())
	};
	ws.send(JSON.stringify(cmd));
	console.log(cmd)
	$('#channels').append(ui_channel(newChannel, $('#s_psk').val(), true))
	$('#sl_to').append(`<option value="${newChannel}" selected>${newChannel}</option>`);
}