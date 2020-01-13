%from api import body_render
%include("tpl/{}/header.tpl".format(template))
<center>
<div id="content">
<div id="menu">
<h1>IDEC</h1>
<ul id="buttons">
<li><a href="/">Главная</a></li> |
<li><a href="/s/fetch">Синхронизация</a></li> |
<li><a href="/new">Новые сообщения</a></li> |
<li><a href="/settings">Настройки</a></li>
</ul>
</div><br>
<div id="sidebar">
<b>Конференции:</b>
<ul id="echolist">
%for echoarea in echoareas:
<li><a href="/{{echoarea[0]}}" title="{{echoarea[1]}}">{{echoarea[0]}}</a></li>
%end
</ul>
</div>
<div id="messages">
<h2>Новое сообщение в {{echo}}</h2>
<form method="post" action="/s/save_message">
<input name="echo" class="text_fiels" type="text" value="{{echo}}" hidden="1">
<input name="subj" class="text_field" type="text" placeholder="Тема сообщения"><br>
<textarea name="body" cols="80" rows="15" placeholder="Тест сообщения">{{body}}</textarea><br>
<center>
<input class="button" type="submit" value="Сохранить">
</center>
</form>
</div>
</center>
%include("tpl/{}/footer.tpl".format(template))