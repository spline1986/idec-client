%from api import body_render
%include("tpl/{}/header.tpl".format(config["template"]))
<center>
<div id="content">
<div id="menu">
<h1>IDEC</h1>
%include("tpl/{}/menu.tpl".format(config["template"]), page=4)
</div><br>
<h2>Настройки</h2>
<form method="post" action="/s/save_settings">
<table width="100%">
<tr>
<td align="right" width="150">
Адрес сервера
</td>
<td>
<input class="field" type="text" name="node" value={{config["node"]}}>
</td>
</tr>
<tr>
<td align="right" width="150">
Строка авторизации
</td>
<td>
<input class="field" type="password" name="auth" value={{config["auth"]}}>
</td>
</tr>
<tr>
<td align="right" width="150">
Шаблон
</td>
<td>
<select class="field" name="template">
%for template in templates:
%if config["template"] == template:
<option selected>{{template}}</option>
%else:
<option>{{template}}</option>
%end
%end
</select>
</td>
</tr>
<tr>
<td  align="center" colspan="2">
Конференции
</td>
</tr>
<tr>
<td colspan="2">
<table width="100%">
<tr>
<td width="30%" valign="top">
<textarea name="nodeechoareas" hidden="1">
%for echoarea in remote_echolist:
{{echoarea[0]}}:{{echoarea[2]}}
%end
</textarea>
<textarea type="field" name="echoareas" rows="25">
%for echoarea in config["echoareas"]:
{{echoarea[0]}}:{{echoarea[1]}}
%end
</textarea>
<input type="checkbox" name="nodeecholist" value="1">Сохранить список сервера
</td>
<td valign="top">
<table width="100%">
%for line in remote_echolist:
%dsc = ":".join(line[2:])
<tr>
<td>{{line[0]}}</td>
<td>{{line[1]}}</td>
<td>{{dsc}}</td>
</tr>
%end
</table>
</td>
</tr>
</table>
</td>
</tr>
<tr>
<td  align="center" colspan="2">
Файловые конференции
</td>
</tr>
<tr>
<td width="30%" valign="top">
<textarea name="nodefechoareas" hidden="1">
%for fechoarea in remote_fecholist:
{{fechoarea[0]}}:{{fechoarea[2]}}
%end
</textarea>
<textarea type="field" name="fechoareas" rows="25">
%for fechoarea in config["fechoareas"]:
{{fechoarea[0]}}:{{fechoarea[1]}}
%end
</textarea>
<input type="checkbox" name="nodefecholist" value="1">Сохранить список сервера
</td>
<td valign="top">
<table width="100%">
%for line in remote_fecholist:
%dsc = ":".join(line[2:])
<tr>
<td>{{line[0]}}</td>
<td>{{line[1]}}</td>
<td>{{dsc}}</td>
</tr>
%end
</table>
</td>
</tr>
</table>
</td>
</tr>
</table>
<br>
<center>
<input class="button" type="submit" value="Сохранить">
</center>
</form>
</div>
</center>
%include("tpl/{}/footer.tpl".format(config["template"]))