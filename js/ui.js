function ui_msgPop (ch, user, time, content, verified=false, timeCheck=true, background='#CCCCCC') {
  var userColor = '#000000';
  var warning = '';
  if (verified) {
    userColor = '#339900';
  }
  if (!timeCheck) {
    warning = '*** ERROR TIMESTAMP ***<br>';
  }
  return `<table width="60%" border="1" cellspacing="1" bordercolor="#999999" bgcolor="#999999">
    <tr>
      <td bgcolor="${background}"><table width="100%" border="0">
        <tr bgcolor="${background}">
          <td colspan="2" nowrap><span class="pop_channel">${ch}</span></td>
        </tr>
        <tr bgcolor="${background}">
          <td width="25%" nowrap style="color:${userColor}";><span class="pop_sender">${user}</span></td>
          <td width="75%" nowrap><span class="pop_time">${time}</span></td>
        </tr>
        <tr align="left" valign="top" bgcolor="#FFFFFF">
          <td colspan="2"><span class="pop_content">${warning + content}</span></td>
        </tr>
      </table></td>
    </tr>
  </table>
  <br>`;
}

function ui_channel (ch, psk, checked=false) {
  ch64 = b64EncodeUnicode(ch)
  return `<table width="100%" border="1" cellspacing="0" bordercolor="#999999">
  <tr><td>
  <table width="100%" cellspacing="1" border="0" bgcolor="#F0F0F0" id="box_${ch64}">
  <tr>
    <td width="100%">${ch}<div id=psk_${ch64} style="display:none">${psk}</div></td>
    <td width="5%" rowspan="2" nowrap>Listen
    <input type="checkbox" id="ch_${ch64}" value="checkbox" onclick="javascript:_channel_clicked('${ch64}')"></td>
  </tr>
  </table></td>
  </tr>
  </table>`;
}

function _channel_clicked (ch64) {
  if ($(`#ch_${ch64}`)[0].checked) {
    chShow[ch64] = $(`#psk_${ch64}`).val();
    $(`#box_${ch64}`)[0].bgColor = '#00FF66';
  } else {
    delete(chShow[ch64])
    $(`#box_${ch64}`)[0].bgColor = '#F0F0F0';
  }
}