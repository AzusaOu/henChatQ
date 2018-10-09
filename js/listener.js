// -- Click "Send"
$('#btn_send').click(function () {
	var ch = $('#sl_to').val();
	var msg = b64EncodeUnicode($('#s_send').val());
	var cmd = {
		'type': 0x02,
		'ch': ch,
		'stype': '-t',
		'msg': msg,
		'psk': $(`#psk_${ch}`)[0].innerHTML,
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
	var psk64 = b64EncodeUnicode($('#s_psk').val());
	var newChannel64 = b64EncodeUnicode(newChannel)
	var cmd = {
		'type': 0x03,
		'ch': newChannel64,
		'psk': psk64
	};
	ws.send(JSON.stringify(cmd));
	console.log(cmd)
	$('#channels').append(ui_channel(newChannel, psk64, true))
	$('#sl_to').append(`<option value="${newChannel64}" selected>${newChannel}</option>`);
}