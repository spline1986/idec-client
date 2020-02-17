%include("tpl/{}/header.tpl".format(template))

<center>
<div id="content">
<div id="menu">
<h1>IDEC</h1>
%include("tpl/{}/menu.tpl".format(template), page=2)
</div><br>
%include("tpl/{}/sidebar.tpl".format(template), echoareas=echoareas, fechoareas=fechoareas)
<div id="messages">
<form method="post" action="/s/send_file" enctype="multipart/form-data">
<h2>Отправка файла</h2>
<table width="100%">
<tr>
<td align="right" width="20%">
Фйловая конференция
</td>
<td>
<select class="field" name="fechoarea">
%for fechoarea in fechoareas:
<option value="{{fechoarea[0]}}">{{fechoarea[0]}}</option>
%end
</select>
</td>
</tr>
<tr>
<td align="right" width="20%">
Файл
</td>
<td>
<input class="field" type="file" name="file">
</td>
</tr>
<tr>
<td align="right">
Описание
</td>
<td>
<input class="field" type="text" name="description">
</td>
</table>
<br>
<center>
<input class="button" type="submit" value="Отправить">
</center>
</form>
</div>
</div>
</center>

%include("tpl/{}/footer.tpl".format(template))