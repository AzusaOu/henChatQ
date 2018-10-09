function ui_msgPop (ch, user, time, content, verified=false, timeCheck=true) {
  var userColor = '#000000';
  var warning = '';
  if (verified) {
    userColor = '#339900';
  }
  if (!timeCheck) {
    warning = '*** ERROR TIMESTAMP ***<br>';
  }
  return `<table width="80%" border="1" cellspacing="1" bordercolor="#999999" bgcolor="#999999">
    <tr>
      <td bgcolor="#CCCCCC"><table width="100%" border="0">
        <tr bgcolor="#CCCCCC">
          <td colspan="2" nowrap><span class="pop_channel">${ch}</span></td>
        </tr>
        <tr bgcolor="#CCCCCC">
          <td width="25%" nowrap style="color:${userColor}";><span class="pop_sender">${user}</span></td>
          <td width="75%" nowrap><span class="pop_time">${time}</span></td>
        </tr>
        <tr align="left" valign="top" bgcolor="#FFFFFF">
          <td colspan="2"><span class="pop_content">${warning + content}</span></td>
        </tr>
      </table></td>
    </tr>
  </table><br>`;
}

function ui_channel (ch, psk, checked=false) {
  return `<table width="100%" border="1" cellspacing="0" bordercolor="#999999">
  <tr><td>
  <table width="100%" cellspacing="1" border="0" bgcolor="#F0F0F0" id="box_${ch}">
  <tr>
    <td width="100%">${ch}</td>
    <td width="5%" rowspan="2" nowrap>Listen
    <input type="checkbox" id="ch_${ch}" value="checkbox" onclick="javascript:_channel_clicked('${ch}')"></td>
  </tr>
  </table></td>
  </tr>
  </table>`;
}

function _channel_clicked (ch) {
  if ($(`#ch_${ch}`)[0].checked) {
    listeningOn.push(ch);
    $(`#box_${ch}`)[0].bgColor = '#00FF66';
  } else {
    listeningOn.splice(listeningOn.indexOf(ch), 1);
    $(`#box_${ch}`)[0].bgColor = '#F0F0F0';
  }
}