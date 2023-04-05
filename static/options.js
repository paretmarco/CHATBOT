$(document).ready(function () {
    loadOptions('user_personality', 'userpersonality.txt');
    loadOptions('task', 'tasks.txt');
    loadOptions('format', 'formats.txt');
});

function loadOptions(elementId, fileName) {
    $.ajax({
        url: 'http://127.0.0.1:5002/static/' + fileName,
        dataType: 'text',
        success: function (data) {
            var optionsArray = data.split('\n');
            console.log('Loaded options:', optionsArray);
            var optionsHtml = '';
            for (var i = 0; i < optionsArray.length; i++) {
                var isChecked = '';
                if (i === 0 && (elementId === 'user_personality' || elementId === 'task')) {
                    isChecked = 'checked';
                }
                optionsHtml += '<input type="checkbox" id="' + elementId + '_' + i + '" name="' + elementId + '" value="' + optionsArray[i] + '" ' + isChecked + '>';
                optionsHtml += '<label for="' + elementId + '_' + i + '">' + optionsArray[i] + '</label><br>';
            }
            $('#' + elementId).html(optionsHtml);
        }
    });
}
