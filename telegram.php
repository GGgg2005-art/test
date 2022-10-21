<?php

/* https://api.telegram.org/bot5778649036:AAFi9Rz4llhNZfh9z2M_CU7CDMRTUpyH1MI/getUpdates,
где, XXXXXXXXXXXXXXXXXXXXXXX - токен вашего бота, полученный ранее */

$name = $_POST['user_name'];
$phone = $_POST['user_adress'];
$token = "5778649036:AAFi9Rz4llhNZfh9z2M_CU7CDMRTUpyH1MI";
$chat_id = "-847033612";
$arr = array(
  'Имя пользователя: ' => $name,
  'Адрес: ' => $phone
);

foreach($arr as $key => $value) {
  $txt .= "<b>".$key."</b> ".$value."%0A";
};

$sendToTelegram = fopen("https://api.telegram.org/bot{$token}/sendMessage?chat_id={$chat_id}&parse_mode=html&text={$txt}","r");

if ($sendToTelegram) {
  header('Location: thank-you.html');
} else {
  echo "Error";
}
?>