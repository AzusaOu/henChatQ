function msgPop (ch, user, time, content, verified=false, timeCheck=true) {
    var userColor = '#000000';
    var warning = '';
    if (verified) {
        userColor = '#339900';
    }
    if (!timeCheck) {
        warning = '*** ERROR TIMESTAMP ***<br>';
    }
    return `<table width="100%" border="1" cellspacing="0" bordercolor="#999999" bgcolor="#999999">
    <tr>
      <td><table width="100%" border="0">
        <tr bgcolor="#999999">
          <td colspan="2" nowrap>${ch}</td>
        </tr>
        <tr bgcolor="#CCCCCC">
          <td width="30%" nowrap style="color:${userColor}";>${user}</td>
          <td width="70%" nowrap>${time}</td>
        </tr>
        <tr align="left" valign="top" bgcolor="#FFFFFF">
          <td colspan="2">${warning + content}</td>
        </tr>
      </table></td>
    </tr>
  </table>`;
}