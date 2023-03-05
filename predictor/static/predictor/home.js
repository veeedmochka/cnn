$('#img-path').prepend(`${document.location.origin}/`)
$('a').attr('href', $('#img-path').text())

$('img').attr('src', $('#img-path').text())