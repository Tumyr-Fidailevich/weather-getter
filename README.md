# weather-getter
1. Геометку города по его названию можно получить с помощью geocoding-api. Информацию о погоде получаем с помощью openweathermap, который использует широту и долготу для определения геопозиции.
      1) Сначала будем посылать запрос с указанием кода страны ru.
      2) Если в указанной стране не удалось найти такой город, будем выводить первый возможный response api по указанному городу.
      3) Если вообще не удалось найти хотя бы какой то город, будем выводить сообщение об этом.
2. Для получения текущего местоположения можно пользоваться библиотекой geocoder. С помощью нее можно определить местоположение пользователя по его ip адресу. Нам необходимо получать ширину и долготу.
3. Так как мы не собираемся хранить очень много данных, для простоты, можно хранить их в json в отдельном файле в проекте. Sql бд здесь будет избыточна как мне кажется.
4. Консольное приложение, в котором будут доступны 4 команды:
      1) -r {city_name} / {current_position} для получения позиции по имени города и по текущему месторасположению. При отсутствии тела запроса используется текущая геометка.
      2) -l {last_requests} для получения последних last_requests запросов. При отсутствии тела запроса будет выводиться последний запрос.
      3) -c очистить последние запросы. Дополнительная валидация - вы точно уверены? {Yes/No}.
      4) -q выход из приложения без тела запроса.
      5) Остальные запросы считаются невалидными и игнорируются.
5. Пока не могу написать конкретную логику обработки запросов, это будет ясно уже на этапе разработки.
