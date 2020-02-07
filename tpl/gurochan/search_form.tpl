<h2>Поиск</h2>
<form method="post" action="/search_result">
<table width="100%">
<tr>
<td align="right" width="100">
Конференция
</td>
<td>
<select class="field" name="echoarea">
%if echoarea:
<option value=""></option>
%else:
<option selected value=""></option>
%end
%for echo in echoareas:
%if echo[0] == echoarea:
<option selected value={{echo[0]}}>{{echo[0]}}</option>
%else:
<option value={{echo[0]}}>{{echo[0]}}</option>
%end
%end
</select>
</td>
</tr>
<tr>
<td align="right">
Текст
</td>
<td>
%if text:
<input class="field" name="text" placeholder="Введите текст" value="{{text}}">
%else:
<input class="field" name="text" placeholder="Введите текст">
%end
</table>
<br>
<center>
<input class="button" type="submit" value="Найти">
</center>
</form>