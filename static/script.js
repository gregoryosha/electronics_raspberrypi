fetch('/getdata/${index}')
    .then(function (response) {
        return response.text();
    }).then(function (text) {
        console.log('GET response text: ');
        console.log(text);
    });