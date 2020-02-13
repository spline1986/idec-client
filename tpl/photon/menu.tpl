<ul id="buttons">
%if page == 0:
<li>Главная</li> |
%else:
<li><a href="/">Главная</a></li> |
%end
<li><a href="/s/fetch">Синхронизация</a></li> |
%if page == 1:
<li>Новые сообщения</li> |
%else:
<li><a href="/new">Новые сообщения</a></li> |
%end
%if page == 2:
<li>Отправить файл</li> |
%else:
<li><a href="/send_file">Отправить файл</a></li> |
%end
%if page == 3:
<li>Поиск</li> |
%else:
<li><a href="/search">Поиск</a></li> |
%end
%if page == 4:
<li>Настройки</li>
%else:
<li><a href="/settings">Настройки</a></li>
%end
</ul>