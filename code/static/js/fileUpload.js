$(() => {
    let reportForm = $('#reportUploadForm'),
        fileInput = $('#reportFile'),
        fileInputEl = fileInput[0],
        fileError = $('#fileError'),
        successBox = $('#success');

    fileInput.on('change', () => {
        reportForm.submit();
    });

    reportForm.on('submit', (e) => {

        fileError.text('').hide();
        let formResult = reportForm.ajaxSubmit({
            url: reportForm.attr('action'),
            method: "POST"
        });
        fileInputEl.value = "";
        let xhr = formResult.data('jqxhr');
        xhr.done((response) => {
            successBox.fadeIn(1000).fadeOut(2000);
            $('#reportContent tbody').html(response);
        });
        xhr.fail((response) => {
            let json = response.responseJSON,
                error = 'Something went wrong. Please check your data and try again.';
            if (json) {
                error = json.csv_file;
            }
            fileError.text(error);
            fileError.show();
        });
        return false;
    })
});