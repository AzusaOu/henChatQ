function msgPop (ch, user, time, content, verified=false, timeCheck=true) {
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

function channel (ch, psk) {
  return `<table width="100%" border="0" bgcolor="#F0F0F0">
  <tr>
    <td width="100%">${ch}</td>
    <td width="5%" rowspan="2" nowrap>Listen
    <input type="checkbox" id="ch_${ch}" value="checkbox"></td>
  </tr>
  <tr>
    <td>PSK: ${psk}}</td>
  </tr>
  </table>`;
}